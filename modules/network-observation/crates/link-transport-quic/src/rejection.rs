use link_wire::{ErrorScope, ProtocolErrorCode};
use thiserror::Error;

#[derive(Debug, Clone, PartialEq, Eq, Error)]
#[error(
    "peer rejected Baseline operation with {code:?} ({scope:?}, related {related_id}): {detail}"
)]
pub struct ProtocolRejection {
    pub code: ProtocolErrorCode,
    pub scope: ErrorScope,
    pub related_id: u64,
    pub detail: String,
}

impl ProtocolRejection {
    pub(crate) fn request(
        code: ProtocolErrorCode,
        request_id: u64,
        detail: impl Into<String>,
    ) -> Self {
        Self {
            code,
            scope: ErrorScope::Request,
            related_id: request_id,
            detail: detail.into(),
        }
    }
}
