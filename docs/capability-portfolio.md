# World Capability Portfolio

Generated from adapter-local declarations. This is a read-only view, not a registry or operational authority.

| Adapter | Owner | Facets | Capabilities | Consumers | Deletion trigger |
|---|---|---|---|---|---|
| `cloudflare` `0.1.0` | provider-adapter | `capability`, `dispatch`, `inspect-result`, `artifact`, `cancel-close` | `fetch` (ready), `browser.run` (ready), `artifact.r2` (ready), `receipt` (ready), `evidence.run` (ready) | ordivon-computer research-source capture; ordivon-world provider post-deployment acceptance | delete an unused capability or adapter facet when no recurring consumer remains and direct provider use has lower total cost |
| `network-observation` `0.1.0` | source-native-observation-module | `capability`, `observation` | `network.http-tls.observe` (ready), `network.quic.observe` (ready), `network.transfer.observe` (ready), `network.connection-lifetime.observe` (ready) | ordivon-host StateRef projection; private network diagnosis and path-condition experiments | delete any probe or retained field that does not alter a real Task decision, verification or recovery path |

## Admission rule

A capability remains local unless two materially different workloads reproduce one unowned, non-bypassable responsibility with lower total cost.
