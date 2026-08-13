from __future__ import annotations

import unittest

from ordivon_world.resource_discovery import (
    ConsumerDemand,
    ConsumptionOutcome,
    DiscoveryEvidence,
    OwnerVerification,
    ResourceCandidate,
    TransportEvidence,
    build_opportunity_board,
    evaluate_resource,
    pareto_frontier,
    rank_resource_evaluations,
)

NOW = "2026-08-13T05:00:00Z"


def provenance(kind: str = "aggregator") -> DiscoveryEvidence:
    return DiscoveryEvidence(
        source_id=f"source:{kind}",
        source_kind=kind,
        observed_at="2026-08-13T04:55:00Z",
        locator="https://example.test/catalog",
        source_digest="sha256:" + "1" * 64,
        evidence_refs=("artifact:catalog",),
    )


def candidate(
    resource_id: str = "resource:open-data",
    *,
    owner_source: bool = False,
    reuse: float = 0.8,
    diversity: float = 0.6,
) -> ResourceCandidate:
    sources = [provenance()]
    if owner_source:
        sources.append(provenance("owner"))
    return ResourceCandidate(
        resource_id=resource_id,
        name=resource_id,
        capabilities=("public-data-read", "bulk-snapshot"),
        interfaces=("https",),
        provenance=tuple(sources),
        owner_hint="owner:test",
        reuse_potential=reuse,
        diversity_potential=diversity,
    )


def owner(
    resource_id: str = "resource:open-data",
    *,
    authority: str = "anonymous-public",
    terms: str = "allowed",
    purposes: tuple[str, ...] = ("academic-research",),
    verified_at: str = "2026-08-13T04:50:00Z",
) -> OwnerVerification:
    return OwnerVerification(
        resource_id=resource_id,
        owner_id="owner:test",
        official_locator="https://owner.test/docs",
        verified_at=verified_at,
        authority_class=authority,
        terms_status=terms,
        allowed_purposes=purposes,
        license_class="cc0",
        cost_class="free",
        quota_class="bounded-public",
        machine_interfaces=("https",),
        evidence_refs=("artifact:owner",),
    )


def transport(
    resource_id: str = "resource:open-data",
    *,
    status: str = "available",
    observed_at: str = "2026-08-13T04:59:00Z",
) -> TransportEvidence:
    return TransportEvidence(
        resource_id=resource_id,
        observed_at=observed_at,
        path_id="fabric:surf-clash:generation-1",
        resolver_id="resolver:surf-clash:doh",
        status=status,
        latency_ms=1200,
        evidence_refs=("artifact:transport",),
    )


def demand(*, authority: str = "anonymous-public", purpose: str = "academic-research") -> ConsumerDemand:
    return ConsumerDemand(
        workload_id="workload:research",
        purpose=purpose,
        required_capabilities=("public-data-read",),
        preferred_capabilities=("bulk-snapshot",),
        authority_budget=authority,
        owner_max_age_seconds=3600,
        transport_max_age_seconds=300,
    )


class ResourceDiscoveryTests(unittest.TestCase):
    def test_aggregator_candidate_never_becomes_owner_authority(self) -> None:
        row = candidate()
        self.assertFalse(row.owner_evidence_present)
        evaluation = evaluate_resource(row, demand(), as_of=NOW)
        self.assertEqual(evaluation.decision, "owner-verification-required")

    def test_current_owner_and_transport_make_anonymous_resource_consumable(self) -> None:
        row = candidate(owner_source=True)
        evaluation = evaluate_resource(
            row,
            demand(),
            as_of=NOW,
            owner=owner(),
            transport=transport(),
        )
        self.assertEqual(evaluation.decision, "consumable-now")
        self.assertGreaterEqual(evaluation.evidence_quality, 0.9)

    def test_stale_owner_fails_closed_before_transport(self) -> None:
        evaluation = evaluate_resource(
            candidate(),
            demand(),
            as_of=NOW,
            owner=owner(verified_at="2026-08-12T00:00:00Z"),
            transport=transport(),
        )
        self.assertEqual(evaluation.decision, "owner-verification-required")
        self.assertIn("owner-verification-stale", evaluation.hard_reasons)

    def test_purpose_restriction_is_not_confused_with_data_license(self) -> None:
        evaluation = evaluate_resource(
            candidate(),
            demand(purpose="commercial"),
            as_of=NOW,
            owner=owner(purposes=("academic-research",)),
            transport=transport(),
        )
        self.assertEqual(evaluation.decision, "blocked-by-terms")

    def test_account_resource_stays_authority_required_under_anonymous_budget(self) -> None:
        evaluation = evaluate_resource(
            candidate(),
            demand(authority="anonymous-public"),
            as_of=NOW,
            owner=owner(authority="free-key"),
            transport=transport(),
        )
        self.assertEqual(evaluation.decision, "authority-required")

    def test_transport_currentness_includes_resolver_identity(self) -> None:
        evidence = transport()
        self.assertEqual(evidence.resolver_id, "resolver:surf-clash:doh")
        stale = transport(observed_at="2026-08-13T04:40:00Z")
        evaluation = evaluate_resource(
            candidate(), demand(), as_of=NOW, owner=owner(), transport=stale
        )
        self.assertEqual(evaluation.decision, "transport-verification-required")

    def test_consumption_outcome_changes_tiebreaker_without_changing_authority(self) -> None:
        row = candidate()
        base = evaluate_resource(row, demand(), as_of=NOW, owner=owner(), transport=transport())
        positive = evaluate_resource(
            row,
            demand(),
            as_of=NOW,
            owner=owner(),
            transport=transport(),
            outcomes=(
                ConsumptionOutcome(
                    resource_id=row.resource_id,
                    workload_id="workload:research",
                    observed_at="2026-08-13T04:59:30Z",
                    useful=True,
                    value=1.0,
                    evidence_refs=("artifact:outcome",),
                ),
            ),
        )
        self.assertEqual(base.decision, positive.decision)
        self.assertGreater(positive.potential_score, base.potential_score)

    def test_pareto_frontier_preserves_tradeoffs(self) -> None:
        a = candidate("resource:a", reuse=1.0, diversity=0.2)
        b = candidate("resource:b", reuse=0.5, diversity=1.0)
        c = candidate("resource:c", reuse=0.2, diversity=0.1)
        rows = [
            evaluate_resource(a, demand(), as_of=NOW, owner=owner("resource:a"), transport=transport("resource:a")),
            evaluate_resource(b, demand(), as_of=NOW, owner=owner("resource:b"), transport=transport("resource:b")),
            evaluate_resource(c, demand(), as_of=NOW, owner=owner("resource:c"), transport=transport("resource:c")),
        ]
        frontier = pareto_frontier(rows)
        self.assertEqual({row.resource_id for row in frontier}, {"resource:a", "resource:b"})
        self.assertNotIn("resource:c", {row.resource_id for row in frontier})

    def test_opportunity_board_bounds_expensive_verification_not_candidate_breadth(self) -> None:
        rows = tuple(candidate(f"resource:{index}") for index in range(20))
        board = build_opportunity_board(rows, demand(), as_of=NOW, verification_budget=3)
        self.assertEqual(board.candidate_count, 20)
        self.assertEqual(len(board.owner_verification_queue), 3)
        self.assertEqual(len(board.transport_verification_queue), 0)
        self.assertEqual(len(board.evaluations), 20)

    def test_opportunity_board_spends_remaining_budget_on_transport_verification(self) -> None:
        owner_missing = candidate("resource:owner-missing")
        transport_missing = candidate("resource:transport-missing")
        board = build_opportunity_board(
            (owner_missing, transport_missing),
            demand(),
            as_of=NOW,
            owners=(owner("resource:transport-missing"),),
            verification_budget=2,
        )
        self.assertEqual([row.resource_id for row in board.owner_verification_queue], ["resource:owner-missing"])
        self.assertEqual([row.resource_id for row in board.transport_verification_queue], ["resource:transport-missing"])

    def test_opportunity_board_separates_authority_from_consumption_and_feedback(self) -> None:
        public = candidate("resource:public")
        gated = candidate("resource:gated")
        board = build_opportunity_board(
            (public, gated),
            demand(),
            as_of=NOW,
            owners=(owner("resource:public"), owner("resource:gated", authority="free-key")),
            transports=(transport("resource:public"), transport("resource:gated")),
        )
        self.assertEqual([row.resource_id for row in board.consumption_queue], ["resource:public"])
        self.assertEqual([row.resource_id for row in board.feedback_queue], ["resource:public"])
        self.assertEqual([row.resource_id for row in board.authority_queue], ["resource:gated"])

    def test_rank_keeps_hard_decision_classes_ahead_of_score(self) -> None:
        usable = evaluate_resource(
            candidate("resource:usable", reuse=0.1, diversity=0.0),
            demand(),
            as_of=NOW,
            owner=owner("resource:usable"),
            transport=transport("resource:usable"),
        )
        blocked = evaluate_resource(
            candidate("resource:blocked", reuse=1.0, diversity=1.0),
            demand(),
            as_of=NOW,
            owner=owner("resource:blocked", purposes=("commercial",)),
            transport=transport("resource:blocked"),
        )
        ranked = rank_resource_evaluations((blocked, usable))
        self.assertEqual(ranked[0].resource_id, "resource:usable")
        self.assertEqual(ranked[-1].decision, "blocked-by-terms")


if __name__ == "__main__":
    unittest.main()
