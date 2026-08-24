from . import resource_discovery as _resource_discovery
from .cloudflare import (
    CloudflareWorldAdapter,
    PreparedWorldDispatch,
    ReconciliationResult,
    WorldObservation,
    WorldOutcomeUnknown,
)
from .entity_migration import EntityMigrationBundle
from .host import HostWorldExtension
from .message_delivery import MessageDeliveryBundle
from .resource_transfer import ResourceTransferBundle
from .schemas import ContractError, load_schema, validate_contract
from .task_inspection import WorldTaskInspector
from .version import __version__

# Keep explicit pre-1.0 package attributes for compatibility without making the
# demand-scoped planning model part of the default wildcard/fresh-Agent surface.
AcquisitionAssessment = _resource_discovery.AcquisitionAssessment
AuthorityEvidence = _resource_discovery.AuthorityEvidence
ConsumerDemand = _resource_discovery.ConsumerDemand
ConsumptionOutcome = _resource_discovery.ConsumptionOutcome
DiscoveryEvidence = _resource_discovery.DiscoveryEvidence
OwnerVerification = _resource_discovery.OwnerVerification
ResourceCandidate = _resource_discovery.ResourceCandidate
ResourceEvaluation = _resource_discovery.ResourceEvaluation
ResourceOpportunityBoard = _resource_discovery.ResourceOpportunityBoard
TransportEvidence = _resource_discovery.TransportEvidence
build_opportunity_board = _resource_discovery.build_opportunity_board
evaluate_resource = _resource_discovery.evaluate_resource
pareto_frontier = _resource_discovery.pareto_frontier
rank_resource_evaluations = _resource_discovery.rank_resource_evaluations

__all__ = [
    "CloudflareWorldAdapter",
    "ContractError",
    "EntityMigrationBundle",
    "HostWorldExtension",
    "MessageDeliveryBundle",
    "PreparedWorldDispatch",
    "ReconciliationResult",
    "ResourceTransferBundle",
    "WorldObservation",
    "WorldOutcomeUnknown",
    "WorldTaskInspector",
    "__version__",
    "load_schema",
    "validate_contract",
]
