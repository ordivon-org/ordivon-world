#!/usr/bin/env python3
from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
from typing import Any

from ordivon_host import EventKind, HostExtensionPort, HostKernel, HostStorage

from ordivon_world.entity_migration import (
    EntityDepartureReceipt,
    EntityMigrationBundle,
    HostEntityMigrationJournal,
)
from ordivon_world.entity_wire import EntityMigrationWireDestination
from ordivon_world.schemas import validate_contract

SOURCE_WORLD = "run:entity-production:local-v1"
DESTINATION_WORLD = "security-world:entity-production:local-v1"
MIGRATION_ID = "migration:entity-production:local-v1"
ENTITY_ID = "medic-reyes"
TASK_ID = "task:entity-production:local-v1"

_GAME_CREATE = r"""
import { StationZeroV3EntityDeparture, StationZeroV3Store, StationZeroV3TurnService } from "./src/station-zero-v3/index.ts";
const dbPath = process.env.ORDIVON_GAME_DB;
const runId = process.env.ORDIVON_SOURCE_WORLD;
const migrationId = process.env.ORDIVON_MIGRATION_ID;
const destinationWorldId = process.env.ORDIVON_DESTINATION_WORLD;
if (!dbPath || !runId || !migrationId || !destinationWorldId) throw new Error("missing acceptance environment");
const actors = { rescue: "medic-reyes", pirate: "pirate-captain-veyra", swarm: "hive-alpha" };
const store = new StationZeroV3Store(dbPath);
try {
  store.createRun({ runId, seed: "entity-production-local-v1" });
  const service = new StationZeroV3TurnService(store);
  const planning = service.openPlanning(runId);
  for (const factionId of ["rescue", "pirate", "swarm"]) {
    const actorId = actors[factionId];
    service.submitPlan(runId, planning.planningId, {
      planId: `plan:entity-production:${factionId}`,
      factionId,
      expectedWorldRevision: planning.worldRevision,
      expectedTurn: planning.turn,
      standingOrderRevision: planning.standingOrderRevision,
      commanderActions: [],
      actorIntents: [factionId === "rescue" ? {
        intentId: "intent:entity-production:extract",
        actorId,
        factionId,
        expectedWorldRevision: planning.worldRevision,
        expectedTurn: planning.turn,
        kind: "extract",
        extractionId: "extraction:entity-production",
      } : {
        intentId: `intent:entity-production:${factionId}:wait`,
        actorId,
        factionId,
        expectedWorldRevision: planning.worldRevision,
        expectedTurn: planning.turn,
        kind: "wait",
      }],
      committedBy: factionId === "rescue" ? "player:entity-production" : `agent:${factionId}`,
    });
  }
  service.execute(runId, planning.planningId);
  const turn = store.latestTurnReceipt(runId);
  if (!turn) throw new Error("missing retained Turn Receipt");
  const fact = turn.record.resolution.facts.find((candidate) =>
    candidate.kind === "actor_life_state_changed" &&
    candidate.actorId === "medic-reyes" &&
    candidate.after === "extracted");
  if (!fact) throw new Error("missing extracted Actor fact");
  const departure = new StationZeroV3EntityDeparture(store);
  const receipt = departure.authorize(runId, {
    migrationId,
    destinationWorldId,
    entityId: "medic-reyes",
    turnBatchId: turn.turnBatchId,
    factId: fact.factId,
  });
  console.log(JSON.stringify({ receipt, stateDigest: turn.stateDigest, lifeState: turn.state.actors["medic-reyes"].lifeState }));
} finally {
  store.close();
}
"""

_GAME_REREAD = r"""
import { StationZeroV3EntityDeparture, StationZeroV3Store } from "./src/station-zero-v3/index.ts";
const dbPath = process.env.ORDIVON_GAME_DB;
const runId = process.env.ORDIVON_SOURCE_WORLD;
const migrationId = process.env.ORDIVON_MIGRATION_ID;
if (!dbPath || !runId || !migrationId) throw new Error("missing acceptance environment");
const store = new StationZeroV3Store(dbPath);
try {
  const receipt = new StationZeroV3EntityDeparture(store).receipt(runId, migrationId);
  const turn = store.latestTurnReceipt(runId);
  if (!receipt || !turn) throw new Error("fresh Game process cannot recover departure authority");
  console.log(JSON.stringify({ receipt, stateDigest: turn.stateDigest, lifeState: turn.state.actors["medic-reyes"].lifeState }));
} finally {
  store.close();
}
"""

_SECURITY_CLEANUP = r"""
import json
from pathlib import Path
import sys
from ordivon_security.evaluation.world_entity import WorldEntityKvmConfig, WorldEntityKvmDestination
from ordivon_security.providers.windows_kvm import WindowsKvmMachineConfig
request = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
state_root = Path(sys.argv[2])
base_manifest = Path(sys.argv[3])
destination_world = sys.argv[4]
source_world = sys.argv[5]
machine = WindowsKvmMachineConfig(
    state_root=state_root,
    base_manifest_path=base_manifest,
    qemu_path=Path("/usr/bin/qemu-system-x86_64"),
    qemu_img_path=Path("/usr/bin/qemu-img"),
    swtpm_path=Path("/usr/bin/swtpm"),
    setpriv_path=Path("/usr/bin/setpriv"),
    firmware_code_path=Path("/usr/share/edk2/x64/OVMF_CODE.4m.fd"),
    run_user="qemu",
    run_group="qemu",
    memory_mib=768,
    vcpu_count=1,
    qmp_ready_timeout_seconds=60,
    shutdown_grace_seconds=15,
)
destination = WorldEntityKvmDestination(
    WorldEntityKvmConfig(
        machine=machine,
        destination_world_id=destination_world,
        allowed_source_world_ids=(source_world,),
    )
)
plan = request["plan"]
plan_digest = request["planDigest"]
state = destination._observe_existing_state(plan, plan_digest)
binding = destination._binding(plan, plan_digest)
closure = destination.machine_provider.destroy_state(
    instance_id=state["instanceId"],
    generation=state["generation"],
    state=state,
    ledger_extra=destination._ledger_extra(binding),
)
print(json.dumps({"clean": closure.clean, **closure.details}, sort_keys=True))
"""


def _json_process(
    arguments: list[str],
    *,
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
    input_value: dict[str, Any] | None = None,
    timeout: int = 120,
) -> dict[str, Any]:
    completed = subprocess.run(
        arguments,
        cwd=cwd,
        env=env,
        input=None if input_value is None else json.dumps(input_value, separators=(",", ":")),
        text=True,
        check=False,
        capture_output=True,
        timeout=timeout,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            f"command failed ({completed.returncode}): {' '.join(arguments)}\n"
            + (completed.stderr or completed.stdout)[-4000:]
        )
    lines = [line for line in completed.stdout.splitlines() if line.strip()]
    if not lines:
        raise RuntimeError(f"command returned no JSON: {' '.join(arguments)}")
    value = json.loads(lines[-1])
    if not isinstance(value, dict):
        raise RuntimeError("command JSON result is not an object")
    return value


def _git_revision(root: Path) -> str:
    completed = subprocess.run(
        ["/usr/bin/git", "rev-parse", "HEAD"],
        cwd=root,
        text=True,
        check=True,
        capture_output=True,
        timeout=10,
    )
    return completed.stdout.strip()


def _game_environment(db_path: Path) -> dict[str, str]:
    import os

    return {
        **os.environ,
        "ORDIVON_GAME_DB": str(db_path),
        "ORDIVON_SOURCE_WORLD": SOURCE_WORLD,
        "ORDIVON_MIGRATION_ID": MIGRATION_ID,
        "ORDIVON_DESTINATION_WORLD": DESTINATION_WORLD,
    }


class SecurityCliTransport:
    def __init__(
        self,
        *,
        uv: Path,
        security_root: Path,
        state_root: Path,
        base_manifest: Path,
    ) -> None:
        self.uv = uv
        self.security_root = security_root
        self.state_root = state_root
        self.base_manifest = base_manifest
        self.calls = 0
        self.last_request: dict[str, Any] | None = None

    def exchange(self, request: dict[str, Any]) -> dict[str, Any]:
        self.calls += 1
        self.last_request = request
        return _json_process(
            [
                str(self.uv),
                "run",
                "--project",
                str(self.security_root),
                "python",
                "-m",
                "ordivon_security.cli_world_entity",
                "--state-root",
                str(self.state_root),
                "--base-manifest",
                str(self.base_manifest),
                "--destination-world-id",
                DESTINATION_WORLD,
                "--allow-source-world",
                SOURCE_WORLD,
                "--memory-mib",
                "768",
            ],
            input_value=request,
            timeout=180,
        )


def _cleanup_security(
    *,
    uv: Path,
    security_root: Path,
    state_root: Path,
    base_manifest: Path,
    request: dict[str, Any],
    temporary_root: Path,
) -> dict[str, Any]:
    request_path = temporary_root / "security-materialize-request.json"
    request_path.write_text(json.dumps(request, sort_keys=True), encoding="utf-8")
    return _json_process(
        [
            str(uv),
            "run",
            "--project",
            str(security_root),
            "python",
            "-c",
            _SECURITY_CLEANUP,
            str(request_path),
            str(state_root),
            str(base_manifest),
            DESTINATION_WORLD,
            SOURCE_WORLD,
        ],
        timeout=120,
    )


def run_acceptance(args: argparse.Namespace) -> dict[str, Any]:
    for root, label in (
        (args.game_root, "Game root"),
        (args.security_root, "Security root"),
    ):
        if not (root / ".git").exists() and not (root / ".git").is_file():
            raise RuntimeError(f"{label} is not a Git worktree: {root}")
    if args.security_state_root.exists():
        raise RuntimeError(f"refusing existing Security state root: {args.security_state_root}")

    with tempfile.TemporaryDirectory(prefix="ordivon-world-entity-production-") as directory:
        temporary_root = Path(directory)
        game_db = temporary_root / "game.sqlite3"
        game_env = _game_environment(game_db)
        created = _json_process(
            ["node", "--input-type=module", "-e", _GAME_CREATE],
            cwd=args.game_root,
            env=game_env,
            timeout=60,
        )
        reread = _json_process(
            ["node", "--input-type=module", "-e", _GAME_REREAD],
            cwd=args.game_root,
            env=game_env,
            timeout=60,
        )
        if created != reread:
            raise RuntimeError("fresh Game process did not recover the exact departure authority")
        raw_departure = created.get("receipt")
        if not isinstance(raw_departure, dict):
            raise RuntimeError("Game did not return an Entity Departure receipt")
        validate_contract("entity-departure-receipt", raw_departure)
        departure = EntityDepartureReceipt.from_dict(raw_departure)
        if (
            departure.migration_id != MIGRATION_ID
            or departure.entity_id != ENTITY_ID
            or departure.source_world_id != SOURCE_WORLD
            or departure.destination_world_id != DESTINATION_WORLD
            or departure.authority.mechanism != "station-zero-v3-verified-extraction.v1"
            or created.get("lifeState") != "extracted"
        ):
            raise RuntimeError("Game departure authority does not bind the production trajectory")

        continuity = {
            "schemaVersion": 1,
            "kind": "ordivon.agent-continuity-envelope",
            "entityId": ENTITY_ID,
            "identityRef": "agent-identity:entity-production:local-v1",
            "cognitionRef": "agent-context:entity-production:local-v1",
            "sourceLocalAuthorityCopied": False,
        }
        bundle = EntityMigrationBundle.create_departed(
            source_departure=departure,
            continuity_payload=continuity,
        )
        transport = SecurityCliTransport(
            uv=args.uv,
            security_root=args.security_root,
            state_root=args.security_state_root,
            base_manifest=args.base_manifest,
        )
        destination = EntityMigrationWireDestination(transport)

        host_root = temporary_root / "host"
        clock = itertools.count(100_000).__next__
        with HostStorage(host_root) as storage:
            kernel = HostKernel(
                storage,
                clock_ms=clock,
                owner_id="host:entity-production:first",
            )
            task = kernel.create_task(
                event_id="event:entity-production:create",
                kind=EventKind.TASK_CREATED,
                task_id=TASK_ID,
                goal_id="goal:entity-production",
                payload={"scenario": "game-world-security-entity-production"},
                frontier=("node:entity-production",),
            ).projection
            journal = HostEntityMigrationJournal(HostExtensionPort(storage, kernel))
            prepared = journal.prepare(task.task_id, bundle)
            materialized = journal.materialize(task.task_id, destination)
            if prepared.status != "prepared" or materialized.status != "materialized":
                raise RuntimeError("Host did not reach prepared then materialized")
            if materialized.receipt is None:
                raise RuntimeError("Host materialized without retaining the destination receipt")
            receipt_value = materialized.receipt

        calls_after_first = transport.calls
        with HostStorage(host_root) as storage:
            fresh_kernel = HostKernel(
                storage,
                clock_ms=clock,
                owner_id="host:entity-production:fresh",
            )
            fresh_journal = HostEntityMigrationJournal(
                HostExtensionPort(storage, fresh_kernel)
            )
            repeated = fresh_journal.materialize(TASK_ID, destination)
            if repeated.status != "materialized" or repeated.receipt != receipt_value:
                raise RuntimeError("fresh Host did not retain the exact Entity materialization")
            if transport.calls != calls_after_first:
                raise RuntimeError("fresh Host redispatched an already materialized Entity")

        if transport.last_request is None:
            raise RuntimeError("Security transport did not retain the materialize request")
        destination_evidence = receipt_value.destination_evidence
        if (
            destination_evidence.get("materializationRole") != "entity-continuity-carrier"
            or destination_evidence.get("guestClaimAuthority") != "not-used"
            or destination_evidence.get("networkDevicePresent") is not False
            or destination_evidence.get("sourceAuthorityAuthentication")
            != "caller-trust-boundary"
        ):
            raise RuntimeError("Security destination evidence differs from the admitted profile")

        cleanup = _cleanup_security(
            uv=args.uv,
            security_root=args.security_root,
            state_root=args.security_state_root,
            base_manifest=args.base_manifest,
            request=transport.last_request,
            temporary_root=temporary_root,
        )
        if cleanup.get("clean") is not True:
            raise RuntimeError("Security Entity carrier cleanup did not reach zero residuals")

        return {
            "schemaVersion": 1,
            "kind": "ordivon.world.entity-production-acceptance",
            "status": "passed",
            "revisions": {
                "game": _git_revision(args.game_root),
                "world": _git_revision(Path.cwd()),
                "security": _git_revision(args.security_root),
            },
            "source": {
                "worldId": SOURCE_WORLD,
                "entityId": ENTITY_ID,
                "migrationId": MIGRATION_ID,
                "authorityId": departure.authority.authority_id,
                "authorityMechanism": departure.authority.mechanism,
                "ownerFreshProcessReread": True,
                "lifeState": created.get("lifeState"),
                "stateDigest": created.get("stateDigest"),
            },
            "world": {
                "hostPrepared": True,
                "hostMaterialized": True,
                "freshHostRetainedReceipt": True,
                "destinationExchangeCalls": transport.calls,
                "blindRedispatch": False,
            },
            "destination": {
                "worldId": DESTINATION_WORLD,
                "materializationId": receipt_value.materialization_id,
                "materializationDigest": receipt_value.materialization_digest,
                "materializationRole": destination_evidence.get("materializationRole"),
                "networkDevicePresent": destination_evidence.get("networkDevicePresent"),
                "guestClaimAuthority": destination_evidence.get("guestClaimAuthority"),
                "sourceAuthorityAuthentication": destination_evidence.get(
                    "sourceAuthorityAuthentication"
                ),
                "cleanupClean": cleanup.get("clean"),
            },
            "trustProfile": {
                "name": "trusted-local-owner-originated-caller",
                "gameOwnerOriginatedAndReread": True,
                "untrustedRelayAuthentication": False,
                "worldAuthorityTranslation": False,
                "globalWorldPki": False,
            },
            "limitations": [
                "The local caller trust boundary is part of this accepted deployment profile.",
                "The acceptance does not authenticate Game authority through an untrusted relay.",
                "The opaque continuity payload is transported but not interpreted by the Guest.",
                "The historical materialization receipt does not prove current Presence after exit.",
            ],
        }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Physical Game → World → Security Entity production acceptance"
    )
    parser.add_argument("--game-root", type=Path, required=True)
    parser.add_argument("--security-root", type=Path, required=True)
    parser.add_argument("--base-manifest", type=Path, required=True)
    parser.add_argument("--security-state-root", type=Path, required=True)
    parser.add_argument("--uv", type=Path, default=Path("/root/.local/bin/uv"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result: dict[str, Any] | None = None
    try:
        result = run_acceptance(args)
        if args.output is not None:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(
                json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n",
                encoding="utf-8",
            )
        print(json.dumps(result, sort_keys=True, separators=(",", ":")))
        return 0
    finally:
        if args.security_state_root.exists():
            shutil.rmtree(args.security_state_root, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
