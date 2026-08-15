from __future__ import annotations

import unittest

from ordivon_world.resource_discovery import (
    AcquisitionAssessment,
    AuthorityEvidence,
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
        verified_capabilities=("public-data-read", "bulk-snapshot"),
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



def acquisition(
    resource_id: str = "resource:open-data",
    *,
    eligibility: str = "eligible",
    mode: str = "agent-self-service",
    expected_benefit: float = 0.9,
    option_value: float = 0.8,
    acquisition_cost: float = 0.1,
    maintenance_cost: float = 0.1,
    payment_exposure: float = 0.0,
    lock_in_cost: float = 0.1,
    expiry_pressure: float = 0.1,
    observed_at: str = "2026-08-13T04:58:00Z",
    human_actions: tuple[str, ...] = (),
    prerequisite_resources: tuple[str, ...] = (),
) -> AcquisitionAssessment:
    return AcquisitionAssessment(
        resource_id=resource_id, observed_at=observed_at, eligibility=eligibility,
        acquisition_mode=mode, expected_benefit=expected_benefit, option_value=option_value,
        acquisition_cost=acquisition_cost, maintenance_cost=maintenance_cost,
        payment_exposure=payment_exposure, lock_in_cost=lock_in_cost,
        expiry_pressure=expiry_pressure, evidence_refs=("artifact:acquisition",),
        human_actions=human_actions, prerequisite_resources=prerequisite_resources,
    )


def authority_evidence(
    resource_id: str = "resource:open-data",
    *,
    authority: str = "free-key",
    status: str = "active",
    observed_at: str = "2026-08-13T04:59:00Z",
) -> AuthorityEvidence:
    return AuthorityEvidence(
        resource_id=resource_id, observed_at=observed_at, authority_class=authority,
        authority_id=f"secret-ref:{resource_id}", status=status,
        evidence_refs=("artifact:authority",),
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

    def test_explicit_owner_terms_block_precedes_missing_capability_attestation(self) -> None:
        row = candidate(owner_source=True)
        blocked_owner = OwnerVerification(
            resource_id=row.resource_id,
            owner_id="owner:test",
            official_locator="https://owner.test/docs",
            verified_at="2026-08-13T04:50:00Z",
            authority_class="anonymous-public",
            terms_status="forbidden",
            allowed_purposes=("academic-research",),
            license_class="cc0",
            cost_class="free",
            quota_class="bounded-public",
            machine_interfaces=("https",),
            evidence_refs=("artifact:owner-forbidden",),
            verified_capabilities=(),
        )
        evaluation = evaluate_resource(row, demand(), as_of=NOW, owner=blocked_owner)
        self.assertEqual(evaluation.decision, "blocked-by-terms")
        self.assertEqual(evaluation.hard_reasons, ("consumer-purpose-not-owner-admitted",))

    def test_candidate_capability_label_without_owner_attestation_fails_closed(self) -> None:
        row = candidate(owner_source=True)
        unbound_owner = OwnerVerification(
            resource_id=row.resource_id,
            owner_id="owner:test",
            official_locator="https://owner.test/docs",
            verified_at="2026-08-13T04:50:00Z",
            authority_class="anonymous-public",
            terms_status="allowed",
            allowed_purposes=("academic-research",),
            license_class="cc0",
            cost_class="free",
            quota_class="bounded-public",
            machine_interfaces=("https",),
            evidence_refs=("artifact:owner-identity-terms-interface-only",),
            verified_capabilities=(),
        )
        evaluation = evaluate_resource(
            row,
            demand(),
            as_of=NOW,
            owner=unbound_owner,
            transport=transport(),
        )
        self.assertEqual(evaluation.decision, "owner-verification-required")
        self.assertEqual(
            evaluation.hard_reasons,
            ("required-capabilities-not-owner-attested:public-data-read",),
        )
        self.assertEqual(evaluation.demand_fit, 0.0)
        self.assertEqual(evaluation.preferred_fit, 0.0)

    def test_stale_owner_capability_attestation_does_not_establish_current_fit(self) -> None:
        row = candidate(owner_source=True)
        evaluation = evaluate_resource(
            row,
            demand(),
            as_of=NOW,
            owner=owner(verified_at="2026-08-12T04:50:00Z"),
            transport=transport(),
        )
        self.assertEqual(evaluation.decision, "owner-verification-required")
        self.assertEqual(evaluation.hard_reasons, ("owner-verification-stale",))
        self.assertEqual(evaluation.demand_fit, 0.0)
        self.assertEqual(evaluation.preferred_fit, 0.0)

    def test_owner_attested_capability_drives_fit_not_candidate_label(self) -> None:
        row = candidate(owner_source=True)
        partial_owner = OwnerVerification(
            resource_id=row.resource_id,
            owner_id="owner:test",
            official_locator="https://owner.test/docs",
            verified_at="2026-08-13T04:50:00Z",
            authority_class="anonymous-public",
            terms_status="allowed",
            allowed_purposes=("academic-research",),
            license_class="cc0",
            cost_class="free",
            quota_class="bounded-public",
            machine_interfaces=("https",),
            evidence_refs=("artifact:owner-capability",),
            verified_capabilities=("public-data-read",),
        )
        evaluation = evaluate_resource(
            row,
            demand(),
            as_of=NOW,
            owner=partial_owner,
            transport=transport(),
        )
        self.assertEqual(evaluation.decision, "consumable-now")
        self.assertEqual(evaluation.demand_fit, 1.0)
        self.assertEqual(evaluation.preferred_fit, 0.0)

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

    def test_authority_budget_is_not_a_veto_for_positive_value_acquisition(self) -> None:
        evaluation = evaluate_resource(
            candidate(),
            demand(authority="anonymous-public"),
            as_of=NOW,
            owner=owner(authority="free-key"),
            acquisition=acquisition(),
            transport=transport(),
        )
        self.assertEqual(evaluation.decision, "acquire-now")
        self.assertGreater(evaluation.acquisition_net_value or 0.0, 0.15)

    def test_missing_possessed_authority_never_turns_willingness_into_access(self) -> None:
        evaluation = evaluate_resource(
            candidate(), demand(authority="payment"), as_of=NOW,
            owner=owner(authority="free-key"), transport=transport(),
        )
        self.assertEqual(evaluation.decision, "acquisition-verification-required")
        self.assertFalse(evaluation.authority_present)

    def test_active_authority_evidence_unlocks_transport_and_consumption(self) -> None:
        evaluation = evaluate_resource(
            candidate(), demand(), as_of=NOW, owner=owner(authority="free-key"),
            authority=authority_evidence(), acquisition=acquisition(), transport=transport(),
        )
        self.assertEqual(evaluation.decision, "consumable-now")
        self.assertTrue(evaluation.authority_present)

    def test_high_value_student_entitlement_becomes_human_action_not_rejection(self) -> None:
        evaluation = evaluate_resource(
            candidate(), demand(), as_of=NOW, owner=owner(authority="student"),
            acquisition=acquisition(
                mode="human-verification", human_actions=("verify-current-student-status",),
                expected_benefit=1.0, option_value=1.0, acquisition_cost=0.2,
            ),
        )
        self.assertEqual(evaluation.decision, "human-action-required")
        self.assertGreater(evaluation.acquisition_net_value or 0.0, 0.15)

    def test_child_offer_waits_on_parent_entitlement_without_duplicate_human_action(self) -> None:
        parent = candidate("resource:github-student-pack")
        child = candidate("resource:github-pack-datadog")
        board = build_opportunity_board(
            (parent, child), demand(), as_of=NOW,
            owners=(
                owner("resource:github-student-pack", authority="student"),
                owner("resource:github-pack-datadog", authority="account"),
            ),
            acquisitions=(
                acquisition(
                    "resource:github-student-pack", mode="human-verification",
                    human_actions=("verify-student-status",), expected_benefit=1.0, option_value=1.0,
                ),
                acquisition(
                    "resource:github-pack-datadog", mode="human-login",
                    prerequisite_resources=("resource:github-student-pack",),
                    human_actions=("redeem-partner-offer",), expected_benefit=0.9, option_value=0.7,
                ),
            ),
        )
        self.assertEqual([row.resource_id for row in board.human_action_queue], ["resource:github-student-pack"])
        self.assertEqual([row.resource_id for row in board.dependent_acquisition_queue], ["resource:github-pack-datadog"])

    def test_parent_authority_releases_child_into_its_own_acquisition_lane(self) -> None:
        child = candidate("resource:github-pack-datadog")
        parent_authority = authority_evidence(
            "resource:github-student-pack", authority="student"
        )
        board = build_opportunity_board(
            (child,), demand(), as_of=NOW,
            owners=(owner("resource:github-pack-datadog", authority="account"),),
            authorities=(parent_authority,),
            acquisitions=(acquisition(
                "resource:github-pack-datadog", mode="human-login",
                prerequisite_resources=("resource:github-student-pack",),
                human_actions=("redeem-partner-offer",),
            ),),
        )
        self.assertEqual([row.resource_id for row in board.human_action_queue], ["resource:github-pack-datadog"])
        self.assertEqual(board.dependent_acquisition_queue, ())

    def test_negative_net_value_is_deferred_not_moralized(self) -> None:
        evaluation = evaluate_resource(
            candidate(), demand(), as_of=NOW, owner=owner(authority="payment"),
            acquisition=acquisition(
                mode="human-payment", expected_benefit=0.2, option_value=0.1,
                acquisition_cost=0.9, maintenance_cost=0.8, payment_exposure=1.0,
                lock_in_cost=0.8, expiry_pressure=0.8, human_actions=("enter-payment-method",),
            ),
        )
        self.assertEqual(evaluation.decision, "defer-acquisition")
        self.assertLess(evaluation.acquisition_net_value or 0.0, 0.15)

    def test_unknown_new_customer_eligibility_can_be_resolved_in_positive_value_human_flow(self) -> None:
        evaluation = evaluate_resource(
            candidate(), demand(), as_of=NOW, owner=owner(authority="payment"),
            acquisition=acquisition(
                eligibility="unknown", mode="human-payment", expected_benefit=0.9, option_value=0.9,
                payment_exposure=0.2, human_actions=("complete-provider-signup",),
            ),
        )
        self.assertEqual(evaluation.decision, "human-action-required")
        self.assertIn("eligibility-resolved-in-human-acquisition-flow", evaluation.hard_reasons[0])

    def test_ineligible_entitlement_is_rejected_by_owner_fact_not_friction(self) -> None:
        evaluation = evaluate_resource(
            candidate(), demand(), as_of=NOW, owner=owner(authority="student"),
            acquisition=acquisition(eligibility="ineligible", mode="human-verification"),
        )
        self.assertEqual(evaluation.decision, "not-eligible")

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

    def test_opportunity_board_spends_verification_budget_on_acquisition_facts_before_transport(self) -> None:
        acquisition_missing = candidate("resource:acquisition-missing")
        transport_missing = candidate("resource:transport-missing")
        board = build_opportunity_board(
            (acquisition_missing, transport_missing), demand(), as_of=NOW,
            owners=(owner("resource:acquisition-missing", authority="free-key"), owner("resource:transport-missing")),
            verification_budget=1,
        )
        self.assertEqual([row.resource_id for row in board.acquisition_verification_queue], ["resource:acquisition-missing"])
        self.assertEqual(board.transport_verification_queue, ())

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

    def test_opportunity_board_separates_acquire_human_transport_and_consumption(self) -> None:
        public = candidate("resource:public")
        agent = candidate("resource:agent")
        human = candidate("resource:human")
        owned = candidate("resource:owned")
        board = build_opportunity_board(
            (public, agent, human, owned), demand(), as_of=NOW,
            owners=(
                owner("resource:public"), owner("resource:agent", authority="free-key"),
                owner("resource:human", authority="student"), owner("resource:owned", authority="free-key"),
            ),
            authorities=(authority_evidence("resource:owned"),),
            acquisitions=(
                acquisition("resource:agent"),
                acquisition("resource:human", mode="human-verification", human_actions=("verify-student",)),
            ),
            transports=(transport("resource:public"), transport("resource:owned")),
        )
        self.assertEqual([row.resource_id for row in board.consumption_queue], ["resource:owned", "resource:public"])
        self.assertEqual({row.resource_id for row in board.feedback_queue}, {"resource:public", "resource:owned"})
        self.assertEqual([row.resource_id for row in board.acquire_now_queue], ["resource:agent"])
        self.assertEqual([row.resource_id for row in board.human_action_queue], ["resource:human"])
        self.assertEqual({row.resource_id for row in board.authority_queue}, {"resource:agent", "resource:human"})

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
