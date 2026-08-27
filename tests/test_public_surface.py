from __future__ import annotations

import unittest

import ordivon_world

_RESOURCE_PLANNING_NAMES = {
    "DiscoveryEvidence",
    "ResourceCandidate",
    "OwnerVerification",
    "AuthorityEvidence",
    "AcquisitionAssessment",
    "TransportEvidence",
    "ConsumerDemand",
    "ConsumptionOutcome",
    "ResourceEvaluation",
    "ResourceOpportunityBoard",
    "build_opportunity_board",
    "evaluate_resource",
    "pareto_frontier",
    "rank_resource_evaluations",
}


class PublicSurfaceTests(unittest.TestCase):
    def test_retired_resource_planning_api_is_absent_from_default_package(self) -> None:
        for name in _RESOURCE_PLANNING_NAMES:
            self.assertFalse(hasattr(ordivon_world, name), name)
        self.assertTrue(_RESOURCE_PLANNING_NAMES.isdisjoint(ordivon_world.__all__))


if __name__ == "__main__":
    unittest.main()
