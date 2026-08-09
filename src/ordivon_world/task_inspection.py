from __future__ import annotations

from typing import Any

from ordivon_host import HostExtensionPort

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
        current = self.port.load_namespace(task_id, "world")
        if current.projection.revision != expected_revision:
            raise WorldTaskInspectionSuperseded(
                "World Task inspection revision differs from current Host Task revision"
            )

        retained = self.port.storage.read_task_extension_state(task_id, "world")
        if retained is None:
            legacy = False
            world_state: dict[str, Any] = {
                "eventKind": None,
                "revision": None,
                "stateDigest": None,
                "legacy": False,
            }
        else:
            pointer, _data = retained
            legacy = pointer.legacy
            world_state = {
                "eventKind": pointer.event_kind.value,
                "revision": pointer.revision,
                "stateDigest": pointer.state_digest,
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
