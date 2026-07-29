use std::path::Path;
use std::sync::Arc;
use std::time::Duration;

use anyhow::Result;
use tokio::sync::{RwLock, broadcast};
use tokio::time::sleep;
use tracing::{info, warn};

use crate::model::{LinkEvent, LinkSnapshot};
use crate::observer::SystemObserver;
use crate::store::Store;

pub struct LinkStateEngine {
    observer: SystemObserver,
    store: Store,
    latest: RwLock<Option<LinkSnapshot>>,
    updates: broadcast::Sender<LinkSnapshot>,
}

impl LinkStateEngine {
    pub fn open(observer: SystemObserver, database_path: &Path) -> Result<Arc<Self>> {
        let (updates, _) = broadcast::channel(32);
        let store = Store::open(database_path)?;
        let latest = store.latest_snapshot()?;
        Ok(Arc::new(Self {
            observer,
            store,
            latest: RwLock::new(latest),
            updates,
        }))
    }

    pub async fn refresh(&self) -> Result<LinkSnapshot> {
        let snapshot = self.observer.collect().await?;
        let previous = self.latest.read().await.clone();
        self.store.record_snapshot(&snapshot, previous.as_ref())?;
        *self.latest.write().await = Some(snapshot.clone());
        let _ = self.updates.send(snapshot.clone());
        Ok(snapshot)
    }

    pub async fn latest(&self) -> Option<LinkSnapshot> {
        self.latest.read().await.clone()
    }

    pub fn subscribe(&self) -> broadcast::Receiver<LinkSnapshot> {
        self.updates.subscribe()
    }

    pub fn recent_events(&self, limit: usize) -> Result<Vec<LinkEvent>> {
        self.store.recent_events(limit)
    }

    pub async fn run(self: Arc<Self>, interval: Duration) {
        loop {
            sleep(interval).await;
            match self.refresh().await {
                Ok(snapshot) => info!(health = ?snapshot.health, "edge snapshot refreshed"),
                Err(_) => {
                    warn!("edge snapshot refresh failed; retaining last known state")
                }
            }
        }
    }
}
