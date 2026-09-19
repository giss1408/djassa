# ExternalSecrets example

This document shows a minimal example using ExternalSecrets (Kubernetes External Secrets) to fetch secrets from Vault.

1. Create a `SecretStore` or `ClusterSecretStore` pointing to Vault with the right auth method.

2. Example `ExternalSecret`:

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: djassa-mobile-money
  namespace: default
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: vault-backend
    kind: ClusterSecretStore
  target:
    name: djassa-mobile-money
    creationPolicy: Owner
  data:
    - secretKey: MOBILE_MONEY_SECRETS
      remoteRef:
        key: secret/djassa/mobile-money
        property: secrets
```

3. The `MOBILE_MONEY_SECRETS` can be a comma-separated list of keys (latest first) used by the app for signature verification and rotation.

4. Document rotation: update Vault `secret/djassa/mobile-money` with new value and adjust rollout.
