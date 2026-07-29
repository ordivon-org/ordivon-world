# Split from the network incubator

The original `ordivon-edge` repository incubated both Link and Edge concepts. Its complete pre-split state remains on branch `archive/network-incubator`.

All local network, probe, observer, console, Baseline wire, and QUIC reference code moved with history to:

```text
https://github.com/zycxfyh/ordivon-link
```

The `ordivon-edge` main branch now starts from an explicit external-execution boundary. No network code was silently deleted; it was transferred and retained before this branch was reframed.
