#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile
from typing import Any

_GAME_PROBE = r'''
import {
  FixtureStationZeroV3AgentProvider,
  StationZeroV3PlayService,
  StationZeroV3Store,
} from "./src/station-zero-v3/index.ts";

class NamedProvider {
  constructor(id) {
    this.providerId = id;
    this.inner = new FixtureStationZeroV3AgentProvider();
  }
  async decide(context) {
    const decision = await this.inner.decide(context);
    return { ...decision, providerId: this.providerId };
  }
}
const factory = (id) => () => new NamedProvider(id);
const db = process.env.ORDIVON_W5A_GAME_DB;
const runId = "run:w5a:active-controller";
if (!db) throw new Error("missing ORDIVON_W5A_GAME_DB");

const store1 = new StationZeroV3Store(db);
let first;
try {
  const service = new StationZeroV3PlayService(store1, {
    providerFactory: factory("provider:w5a:alpha"),
  });
  service.initialize({ runId, seed: "w5a-active-controller" });
  first = await service.generatePreview(runId);
  await service.commitPreview(runId, first.preview.previewId);
} finally {
  store1.close();
}

const store2 = new StationZeroV3Store(db);
try {
  const service = new StationZeroV3PlayService(store2, {
    providerFactory: factory("provider:w5a:mallory"),
  });
  service.resume(runId);
  const second = await service.generatePreview(runId);
  const firstByActor = Object.fromEntries(
    first.preview.agentDecisions.map((decision) => [decision.actorId, decision.providerId]),
  );
  const secondByActor = Object.fromEntries(
    second.preview.agentDecisions.map((decision) => [decision.actorId, decision.providerId]),
  );
  const common = Object.keys(firstByActor).filter((actorId) => actorId in secondByActor).sort();
  if (common.length === 0) throw new Error("no active Actor survived into second planning");
  const changed = common.filter((actorId) => firstByActor[actorId] !== secondByActor[actorId]);
  if (changed.length === 0) throw new Error("provider identity did not change for a surviving Actor");
  console.log(JSON.stringify({
    status: "passed",
    runId,
    commonActiveActors: common,
    changedActors: changed,
    firstProviderIds: firstByActor,
    secondProviderIds: secondByActor,
    durableContinuitySubjectAdmissionObserved: false,
    conclusion: "provider-attribution-is-not-continuity-subject-embodiment",
  }));
} finally {
  store2.close();
}
'''


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


def run(game_root: Path) -> dict[str, Any]:
    if not (game_root / ".git").exists() and not (game_root / ".git").is_file():
        raise RuntimeError(f"Game root is not a Git worktree: {game_root}")
    with tempfile.TemporaryDirectory(prefix="ordivon-world-w5a-game-") as directory:
        db_path = Path(directory) / "game.sqlite3"
        completed = subprocess.run(
            ["/usr/bin/node", "--input-type=module", "-e", _GAME_PROBE],
            cwd=game_root,
            env={**os.environ, "ORDIVON_W5A_GAME_DB": str(db_path)},
            text=True,
            check=False,
            capture_output=True,
            timeout=60,
        )
        if completed.returncode != 0:
            raise RuntimeError(
                "Game active-controller probe failed: "
                + (completed.stderr or completed.stdout)[-4000:]
            )
        lines = [line for line in completed.stdout.splitlines() if line.strip()]
        if not lines:
            raise RuntimeError("Game active-controller probe returned no JSON")
        value = json.loads(lines[-1])
        if not isinstance(value, dict) or value.get("status") != "passed":
            raise RuntimeError("Game active-controller probe result is invalid")
        return {
            "schemaVersion": 1,
            "kind": "ordivon.world.w5a-game-active-controller-falsifier",
            **value,
            "revisions": {
                "game": _git_revision(game_root),
                "world": _git_revision(Path.cwd()),
            },
            "disposition": {
                "activeActorProven": True,
                "providerAttributionProven": True,
                "continuitySubjectEmbodimentProven": False,
                "providerIdentityMayStandInForAgentIdentity": False,
                "productionContractPromotion": False,
            },
        }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="W5-A probe showing active Game controller attribution is not Agent embodiment"
    )
    parser.add_argument("--game-root", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run(args.game_root)
    encoded = json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n"
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
