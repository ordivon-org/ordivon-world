import {
  EDGE_NODE_SCHEMA_VERSION,
  type EdgeLifecycleOperation,
  type EdgeLifecycleOutcome,
  type EdgeLifecycleSnapshot,
  type EdgeNodeLifecycleState
} from "./node-contracts.js";

const ALLOWED: Readonly<Record<EdgeLifecycleOperation, readonly EdgeNodeLifecycleState[]>> = {
  provision: ["declared"],
  admit: ["provisioned"],
  start: ["admitted", "frozen"],
  freeze: ["running"],
  capture: ["running", "frozen"],
  snapshot: ["frozen"],
  restore: ["snapshotted"],
  retire: ["provisioned", "admitted", "running", "frozen", "evidence-captured", "snapshotted"],
  destroy: ["provisioned", "admitted", "frozen", "evidence-captured", "snapshotted", "retired"]
};

const NEXT: Readonly<Record<EdgeLifecycleOperation, EdgeNodeLifecycleState>> = {
  provision: "provisioned",
  admit: "admitted",
  start: "running",
  freeze: "frozen",
  capture: "evidence-captured",
  snapshot: "snapshotted",
  restore: "admitted",
  retire: "retired",
  destroy: "destroyed"
};

interface UncertainOperation {
  readonly operationId: string;
  readonly operation: "provision" | "destroy";
}

const OPERATION_ID = /^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$/;

export class EdgeNodeLifecycle {
  #state: EdgeNodeLifecycleState;
  #uncertain: UncertainOperation | undefined;
  readonly #outcomes = new Map<string, EdgeLifecycleOutcome>();

  constructor(snapshot?: EdgeLifecycleSnapshot | EdgeNodeLifecycleState) {
    if (snapshot === undefined || typeof snapshot === "string") {
      this.#state = snapshot ?? "declared";
      return;
    }
    if (snapshot.schema_version !== EDGE_NODE_SCHEMA_VERSION) {
      throw new Error("unsupported lifecycle snapshot schema");
    }
    this.#state = snapshot.state;
    if (snapshot.uncertain !== undefined) {
      this.#uncertain = {
        operationId: snapshot.uncertain.operation_id,
        operation: snapshot.uncertain.operation
      };
    }
    for (const outcome of snapshot.outcomes) {
      this.#validateOperationId(outcome.operation_id);
      if (this.#outcomes.has(outcome.operation_id)) {
        throw new Error("duplicate lifecycle operation ID in snapshot");
      }
      this.#outcomes.set(outcome.operation_id, { ...outcome });
    }
    this.#validateSnapshot();
  }

  get state(): EdgeNodeLifecycleState {
    return this.#state;
  }

  snapshot(): EdgeLifecycleSnapshot {
    return {
      schema_version: EDGE_NODE_SCHEMA_VERSION,
      state: this.#state,
      ...(this.#uncertain === undefined
        ? {}
        : {
            uncertain: {
              operation_id: this.#uncertain.operationId,
              operation: this.#uncertain.operation
            }
          }),
      outcomes: [...this.#outcomes.values()].map((outcome) => ({ ...outcome }))
    };
  }

  apply(
    operationId: string,
    operation: EdgeLifecycleOperation,
    effect: "applied" | "uncertain" = "applied"
  ): EdgeLifecycleOutcome {
    this.#validateOperationId(operationId);
    const replay = this.#replay(operationId, operation);
    if (replay !== undefined) return replay;
    if (this.#uncertain !== undefined) {
      return this.#rejected(operationId, operation, "reconciliation required before redispatch");
    }
    if (!ALLOWED[operation].includes(this.#state)) {
      return this.#rejected(
        operationId,
        operation,
        `${operation} is invalid from ${this.#state}`
      );
    }
    if (effect === "uncertain") {
      if (operation !== "provision" && operation !== "destroy") {
        return this.#rejected(operationId, operation, "only provider effects may be uncertain");
      }
      this.#uncertain = { operationId, operation };
      this.#state = operation === "provision" ? "provision-uncertain" : "destroy-uncertain";
      return this.#record({
        operation_id: operationId,
        operation,
        disposition: "uncertain",
        state: this.#state,
        reconciliation_required: true
      });
    }
    this.#state = NEXT[operation];
    return this.#record({
      operation_id: operationId,
      operation,
      disposition: "applied",
      state: this.#state,
      reconciliation_required: false
    });
  }

  reconcile(operationId: string, providerBodyExists: boolean): EdgeLifecycleOutcome {
    this.#validateOperationId(operationId);
    const replay = this.#outcomes.get(operationId);
    if (replay !== undefined) {
      if (this.#uncertain === undefined) return replay;
      return this.#rejected(
        operationId,
        this.#uncertain.operation,
        "reconciliation operation ID was already used"
      );
    }
    const uncertain = this.#uncertain;
    if (uncertain === undefined) {
      return this.#rejected(operationId, "provision", "no uncertain provider effect");
    }
    this.#uncertain = undefined;
    if (uncertain.operation === "provision") {
      this.#state = providerBodyExists ? "provisioned" : "declared";
    } else {
      this.#state = providerBodyExists ? "retired" : "destroyed";
    }
    const resolvedOriginal: EdgeLifecycleOutcome = {
      operation_id: uncertain.operationId,
      operation: uncertain.operation,
      disposition: "applied",
      state: this.#state,
      reconciliation_required: false,
      reason: providerBodyExists ? "provider body exists" : "provider body absent"
    };
    this.#outcomes.set(uncertain.operationId, resolvedOriginal);
    return this.#record({
      ...resolvedOriginal,
      operation_id: operationId
    });
  }

  #replay(
    operationId: string,
    operation: EdgeLifecycleOperation
  ): EdgeLifecycleOutcome | undefined {
    const prior = this.#outcomes.get(operationId);
    if (prior === undefined) return undefined;
    if (prior.operation !== operation) {
      return this.#rejected(operationId, operation, "operation ID is bound to another operation");
    }
    return prior;
  }

  #record(outcome: EdgeLifecycleOutcome): EdgeLifecycleOutcome {
    this.#outcomes.set(outcome.operation_id, outcome);
    return outcome;
  }

  #rejected(
    operationId: string,
    operation: EdgeLifecycleOperation,
    reason: string
  ): EdgeLifecycleOutcome {
    return {
      operation_id: operationId,
      operation,
      disposition: "rejected",
      state: this.#state,
      reconciliation_required: this.#uncertain !== undefined,
      reason
    };
  }

  #validateSnapshot(): void {
    const stateIsUncertain =
      this.#state === "provision-uncertain" || this.#state === "destroy-uncertain";
    if (stateIsUncertain !== (this.#uncertain !== undefined)) {
      throw new Error("lifecycle snapshot uncertainty is inconsistent");
    }
    if (
      this.#uncertain?.operation === "provision" &&
      this.#state !== "provision-uncertain"
    ) {
      throw new Error("provision uncertainty has invalid state");
    }
    if (
      this.#uncertain?.operation === "destroy" &&
      this.#state !== "destroy-uncertain"
    ) {
      throw new Error("destroy uncertainty has invalid state");
    }
    if (
      [...this.#outcomes.values()].some(
        (outcome) =>
          outcome.disposition === "uncertain" &&
          outcome.operation_id !== this.#uncertain?.operationId
      )
    ) {
      throw new Error("lifecycle snapshot contains stale uncertain outcomes");
    }
    const uncertainOutcome =
      this.#uncertain === undefined
        ? undefined
        : this.#outcomes.get(this.#uncertain.operationId);
    if (
      this.#uncertain !== undefined &&
      (uncertainOutcome?.disposition !== "uncertain" ||
        uncertainOutcome.operation !== this.#uncertain.operation ||
        uncertainOutcome.state !== this.#state ||
        !uncertainOutcome.reconciliation_required)
    ) {
      throw new Error("lifecycle snapshot lacks its uncertain outcome");
    }
  }

  #validateOperationId(operationId: string): void {
    if (!OPERATION_ID.test(operationId)) {
      throw new Error("invalid lifecycle operation ID");
    }
  }
}
