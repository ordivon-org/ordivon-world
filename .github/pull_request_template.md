## Responsibility

What current workload and failure does this change address?

## Authority and recovery

- Which layer owns the changed fact?
- What is the exact request or operation identity?
- What happens after response loss, process replacement or condition drift?
- Why can this not be owned more cleanly by Host, Runtime, the provider or the domain?

## Verification

- [ ] locked Python and provider dependencies
- [ ] Python adapter tests
- [ ] cross-language contract gate
- [ ] Cloudflare provider gate when applicable
- [ ] network gate when applicable
- [ ] wheel isolated installation
- [ ] live doctor / commit-bound acceptance when external effects changed

## Deletion condition

When should this structure, adapter, field or check be removed?
