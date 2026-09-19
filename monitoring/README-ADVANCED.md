Advanced monitoring run notes

- Use `scripts/start-monitoring.sh` to render `prometheus.yml` and start compose.
- On Linux, the script detects the docker gateway IP to allow scraping services running on the host.
- To build for alternate architectures use `scripts/start-all.sh <arch>` where `<arch>` is `amd64` or `arm64`.

Examples:

```bash
# start monitoring only
./scripts/start-monitoring.sh

# start everything for arm64
./scripts/start-all.sh arm64
```
