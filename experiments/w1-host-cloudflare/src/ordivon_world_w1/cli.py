from __future__ import annotations

import argparse
import hashlib
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys

from anc_canonical import canonical_digest

from .experiment import TrialArm, TrialConfig, dispatch_phase, resume_phase
from .probe import run_link_probe
from .provider import SignedEdgeClient


def _repository_root() -> Path:
    return Path(__file__).resolve().parents[4]


def _arm(value: str) -> TrialArm:
    try:
        return TrialArm(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError(str(error)) from error


def _read_probe(path: str | Path) -> dict[str, object]:
    value = json.loads(Path(path).read_text())
    if not isinstance(value, dict):
        raise ValueError("probe source must be a JSON object")
    return dict(value)


def _client(args: argparse.Namespace) -> SignedEdgeClient:
    return SignedEdgeClient(
        repository_root=args.repository_root,
        config_path=args.config,
    )


def command_dispatch(args: argparse.Namespace) -> int:
    config = TrialConfig(args.arm, args.trial_id, Path(args.trial_root))
    result = dispatch_phase(config, provider=_client(args), probe_source=_read_probe(args.probe_source))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


def command_resume(args: argparse.Namespace) -> int:
    config = TrialConfig(args.arm, args.trial_id, Path(args.trial_root))
    result = resume_phase(config, provider=_client(args))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["phase"] == "completed" else 1


def command_pair_live(args: argparse.Namespace) -> int:
    output = Path(args.output_root).resolve()
    if output.exists() and any(output.iterdir()):
        raise RuntimeError("pair-live output root must be absent or empty; resume arms explicitly to avoid redispatch")
    output.mkdir(parents=True, exist_ok=True)
    experiment_id = args.experiment_id or datetime.now(timezone.utc).strftime("w1-%Y%m%dT%H%M%SZ")
    probe_root = output / "shared-probe"
    raw_probe, _ = run_link_probe(
        repository_root=args.repository_root,
        evidence_root=probe_root,
        network=args.network,
        route=args.route,
    )
    probe_source = probe_root / "probe-source.json"
    reports: dict[str, object] = {}
    for arm in (TrialArm.DIRECT, TrialArm.CORRELATION):
        trial_id = f"{experiment_id}-{arm.value}"
        trial_root = output / arm.value
        common = [
            "--arm",
            arm.value,
            "--trial-id",
            trial_id,
            "--trial-root",
            str(trial_root),
            "--repository-root",
            str(args.repository_root),
        ]
        if args.config is not None:
            common.extend(["--config", str(args.config)])
        subprocess.run(
            [
                sys.executable,
                "-m",
                "ordivon_world_w1.cli",
                "dispatch",
                *common,
                "--probe-source",
                str(probe_source),
            ],
            check=True,
        )
        subprocess.run(
            [sys.executable, "-m", "ordivon_world_w1.cli", "resume", *common],
            check=True,
        )
        reports[arm.value] = json.loads((trial_root / "evidence/final-report.json").read_text())
    direct = reports[TrialArm.DIRECT.value]
    correlation = reports[TrialArm.CORRELATION.value]
    assert isinstance(direct, dict) and isinstance(correlation, dict)
    pair = {
        "schemaVersion": 1,
        "kind": "ordivon.world.w1.pair-report",
        "experimentId": experiment_id,
        "probe": {
            "sourceSha256": hashlib.sha256(
                json.dumps(raw_probe, sort_keys=True, separators=(",", ":")).encode("utf-8")
            ).hexdigest(),
            "projectionDigest": canonical_digest(
                json.loads(
                    (output / TrialArm.DIRECT.value / "evidence/probe-projection.json").read_text()
                )
            ),
            "sourcePath": "shared-probe/probe-source.json",
        },
        "arms": reports,
        "bothCompletedExactlyOnce": bool(
            direct.get("exactlyOnceCompletion") and correlation.get("exactlyOnceCompletion")
        ),
        "bothAvoidedDuplicateEffects": bool(
            direct.get("duplicateExternalEffects") == 0
            and correlation.get("duplicateExternalEffects") == 0
        ),
        "b1AdditionalCorrelationEvents": int(correlation.get("correlationEventCount", 0)),
        "b1HostObjectDelta": int(correlation.get("hostObjectCount", 0))
        - int(direct.get("hostObjectCount", 0)),
        "b1HostObjectByteDelta": int(correlation.get("hostObjectBytes", 0))
        - int(direct.get("hostObjectBytes", 0)),
        "b1CorrelationBytes": int(correlation.get("correlationBytes", 0)),
        "disposition": "absorb-into-host-and-provider-observation-adapters",
    }
    pair_path = output / "pair-report.json"
    pair_path.write_text(json.dumps(pair, indent=2, sort_keys=True) + "\n")
    print(json.dumps(pair, indent=2, sort_keys=True))
    return 0 if pair["bothCompletedExactlyOnce"] and pair["bothAvoidedDuplicateEffects"] else 1


def parser() -> argparse.ArgumentParser:
    root = _repository_root()
    result = argparse.ArgumentParser(description="Ordivon World W1 experiment")
    commands = result.add_subparsers(dest="command", required=True)

    def common(command: argparse.ArgumentParser) -> None:
        command.add_argument("--arm", required=True, type=_arm, choices=list(TrialArm))
        command.add_argument("--trial-id", required=True)
        command.add_argument("--trial-root", required=True, type=Path)
        command.add_argument("--repository-root", type=Path, default=root)
        command.add_argument("--config", type=Path)

    dispatch = commands.add_parser("dispatch")
    common(dispatch)
    dispatch.add_argument("--probe-source", required=True, type=Path)
    dispatch.set_defaults(handler=command_dispatch)

    resume = commands.add_parser("resume")
    common(resume)
    resume.set_defaults(handler=command_resume)

    pair = commands.add_parser("pair-live")
    pair.add_argument("--output-root", required=True, type=Path)
    pair.add_argument("--experiment-id")
    pair.add_argument("--network", default="wsl-current")
    pair.add_argument("--route", default="host-current")
    pair.add_argument("--repository-root", type=Path, default=root)
    pair.add_argument("--config", type=Path)
    pair.set_defaults(handler=command_pair_live)
    return result


def entrypoint() -> int:
    args = parser().parse_args()
    return int(args.handler(args))


if __name__ == "__main__":
    raise SystemExit(entrypoint())
