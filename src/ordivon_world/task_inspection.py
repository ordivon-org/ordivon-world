from __future__ import annotations

from typing import Any

from ordivon_host import HostExtensionPort, TaskRevisionMismatch

from .entity_migration import HostEntityMigrationJournal
from .host import HostWorldExtension
from .message_delivery import HostMessageDeliveryJournal
from .resource_transfer import HostResourceTransferJournal


class WorldTaskInspectionError(RuntimeError):
    pass


class WorldTaskInspectionSuperseded(WorldTaskInspectionError):
    pass


class WorldTaskInspector:
    """Bounded read-only projection of World-owned Task commitments.

    Family-specific journals own interpretation of their retained state. This
    aggregator only fences the Host Task revision, reports the retained World
    namespace pointer, and combines bounded family projections. It does not
    decode payload/provenance/continuity bodies and does not grant authority.
    """

    _projector_types = (
        HostWorldExtension,
        HostResourceTransferJournal,
        HostMessageDeliveryJournal,
        HostEntityMigrationJournal,
    )

    def __init__(self, port: HostExtensionPort) -> None:
        self.port = port

    def inspect_task(self, task_id: str, *, expected_revision: int) -> dict[str, Any]:
        try:
            current = self.port.load_namespace_snapshot(
                task_id,
                "world",
                expected_revision=expected_revision,
            )
        except TaskRevisionMismatch as error:
            raise WorldTaskInspectionSuperseded(
                "World Task inspection revision differs from current Host Task revision"
            ) from error

        legacy = current.legacy
        if not current.retained:
            world_state: dict[str, Any] = {
                "eventKind": None,
                "revision": None,
                "stateDigest": None,
                "legacy": False,
            }
        else:
            assert current.owner_event_kind is not None
            assert current.owner_state_digest is not None
            assert current.owner_revision is not None
            world_state = {
                "eventKind": current.owner_event_kind.value,
                "revision": current.owner_revision,
                "stateDigest": current.owner_state_digest,
                "legacy": legacy,
            }

        commitments: list[dict[str, Any]] = []
        for projector_type in self._projector_types:
            projector = projector_type(self.port)
            commitments.extend(
                projector.project_owner_commitments(
                    task_id,
                    current.data,
                    legacy=legacy,
                )
            )
        commitments.sort(key=lambda value: (str(value["family"]), str(value["identity"])))

        return {
            "schemaVersion": 1,
            "kind": "ordivon.world.task-commitment-inspection",
            "ownerNamespace": "world",
            "taskId": task_id,
            "taskRevision": current.projection.revision,
            "worldState": world_state,
            "commitments": commitments,
            "constraints": [
                "informational-owner-projection-only",
                "inspection-does-not-grant-action-authority",
                "terminal-evidence-is-historical-not-current-presence",
                "unknown-outcome-requires-owner-reconciliation-before-retry",
            ],
        }

    def inspect_replacement_readiness(
        self, task_id: str, *, expected_revision: int
    ) -> dict[str, Any]:
        """Project whether controller replacement would orphan reconciliation work.

        This is derived, revision-fenced information only. A clear result never
        grants retry, reconciliation, dispatch, or external-currentness authority.
        """

        inspection = self.inspect_task(task_id, expected_revision=expected_revision)
        blockers: list[dict[str, Any]] = []
        for commitment in inspection["commitments"]:
            operation = commitment.get("nextOwnerOperation")
            if isinstance(operation, str) and operation.startswith("reconcile-"):
                blockers.append(
                    {
                        "family": commitment["family"],
                        "identity": commitment["identity"],
                        "state": commitment["state"],
                        "nextOwnerOperation": operation,
                    }
                )
        return {
            "schemaVersion": 1,
            "kind": "ordivon.world.controller-replacement-readiness",
            "taskId": task_id,
            "taskRevision": inspection["taskRevision"],
            "replaceable": not blockers,
            "reconciliationBlockers": blockers,
            "actionAuthority": "not-granted-by-inspection",
            "externalCurrentness": "not-claimed",
            "constraints": [
                "derived-from-owner-native-commitment-projections",
                "clear-readiness-does-not-grant-action-authority",
                "unknown-outcome-remains-owner-reconciliation-work",
            ],
        }
