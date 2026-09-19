# djassa — Container orchestration security architecture

Goal: provide concrete, actionable security guidance for running `djassa` in container orchestration platforms (Docker Compose for local/dev and Kubernetes for production). This document covers design principles, build-time and runtime controls, CI/CD gating, supply-chain protections, monitoring, and concrete Kubernetes manifest examples.

Principles
- Least privilege: run services with the minimum permissions, network reachability, and file-system access they need.
- Immutable images: build reproducible, versioned images; never build in production clusters.
- Defense in depth: combine network segmentation, runtime detection, admission controls, and audit logging.
- Fail closed: CI gates must block vulnerable images; admission controllers must reject non-compliant workloads.

1) Environment segmentation
- Keep three logical zones (matches the existing docker-compose):
  - edge (ingress/proxy) — only component with host-facing ports.
  - app (application network) — API, workers; no direct host exposure.
  - data (storage) — DB, Redis, object storage; never exposed publicly.

- Kubernetes mapping:
  - Use separate namespaces: `edge`, `app`, `data`.
  - Use NetworkPolicies to restrict cross-namespace traffic to only required flows (ingress -> app/api; app -> data).

2) Image build and supply chain
- Build images in CI with reproducible build args, fixed base image digests (use `FROM python:3.11-slim@sha256:...`).
- Generate an SBOM for every image (Syft) and attach it as build artifact.
- Scan every image for vulnerabilities (Trivy/Clair) and fail builds on disallowed severities (e.g., HIGH/CRITICAL).
- Sign images (cosign) and verify signatures in the cluster admission policy.
- Use ephemeral build runners or hardened build runners; avoid developer machines as the single source of truth for production images.

3) Secrets management
- Do not store secrets in Git. Use one of:
  - Cloud-managed secret stores (AWS Secrets Manager, Azure Key Vault, GCP Secret Manager).
  - Kubernetes External Secrets / Secret Store CSI driver to sync secrets into the cluster at deploy time.
- In Docker Compose, mount secrets via Docker secrets (already present). Ensure secret files are excluded from commits and use OS-level permissions.
- Restrict which ServiceAccounts / Pods can access secrets via RBAC and admission policies.

4) Kubernetes runtime controls
- Pod-level controls:
  - `securityContext` with `runAsNonRoot: true`, non-root user, `readOnlyRootFilesystem: true`, drop capabilities (`NET_RAW`, `SYS_ADMIN`), and set `seccompProfile` to `RuntimeDefault`.
  - Resource limits and requests for CPU/memory to prevent noisy neighbors.
  - Readiness and liveness probes to detect failures.

- Namespace & cluster controls:
  - PodSecurity admission in `restricted` mode for production namespaces.
  - NetworkPolicy to implement north-south and east-west filtering.
  - RBAC least-privilege for CI/CD agents and runtime controllers.
  - Admission controllers: OPA/Gatekeeper or Kyverno to enforce labeling, disallow `latest` tags, enforce image signatures, and block privileged containers.

5) Runtime detection and response
- Use Falco or a cloud-native detection agent to watch for suspicious syscalls, unexpected network connections, or privilege escalations.
- Forward alerts and audit logs to a central logging/monitoring stack (ELK, Loki+Grafana, or cloud equivalents). Keep audit logs immutable and retained for compliance.

6) Network and Ingress
- Terminate TLS at the edge (ingress) and use mTLS for inter-service communications if high assurance is required (service mesh like Istio/Linkerd with strict mTLS policy).
- Certificate management: use cert-manager with ACME or cloud CA; store private keys in secrets with strict access control.

7) Node & host hardening
- Use minimal host OS images, keep container runtime (containerd) and kubelet updated, and apply CIS Kubernetes benchmark hardening.
- Lock down SSH access and use bastion hosts + MFA. Use IAM roles for node operations instead of static credentials.

8) Backup, recovery, and secrets rotation
- Regularly backup databases and object storage with encrypted snapshots; test restore procedures.
- Rotate secrets and keys on a schedule; support emergency rotation workflows.

9) CI/CD gating (example rules)
- SBOM produced + attached to build.
- Vulnerability scan: fail on >= 1 Critical or N High (configurable).
- Image signing required; admission controller verifies signature.
- Linting + container image policy (no root user, no latest tag).

10) Operational checklist
- Enforce PodSecurity level `restricted` in production namespaces.
- NetworkPolicies: deny-all default, allow only known flows.
- Enforce image scanning and SBOM production in CI.
- Install runtime detection (Falco) and centralize alerts.
- Enable Kubernetes audit logging and export to tamper-evident storage.

Recommended tools
- Build & SBOM: Syft (Anchore), Docker buildx
- Scanning: Trivy, Clair, Snyk
- Image signing: cosign
- Admission control: OPA/Gatekeeper, Kyverno
- Runtime detection: Falco
- Secrets: External Secrets Operator, K8s CSI Secret Store
- Monitoring/logging: Prometheus, Grafana, Loki, ELK

References & further reading
- Kubernetes Pod Security Standards
- CIS Kubernetes Benchmark
- NIST guidance on supply chain security

Appendix: quick Kubernetes manifest examples are in `k8s/` subfolder.

Quick deploy steps

- Ensure `kubectl` context points to the target cluster and you have appropriate privileges.
- Install cert-manager and External Secrets Operator in the cluster (see their docs).
- Apply manifests:

```bash
chmod +x scripts/deploy-k8s.sh
./scripts/deploy-k8s.sh
```

CI notes (registry + secrets)

- Set the following GitHub repository secrets used by the CI workflow:
  - `REGISTRY_URL` — e.g. `ghcr.io/yourorg` or `registry.example.com`
  - `REGISTRY_USERNAME`
  - `REGISTRY_PASSWORD`

- The workflow will build the image, optionally push (set `push: true` if desired), generate SBOM, and fail the job on High/Critical vulnerabilities as configured.

