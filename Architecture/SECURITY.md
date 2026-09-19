# Sécurité en profondeur — Backend Djassa

> Principe : aucune couche ne doit être la seule ligne de défense. Si une couche est contournée (un secret fuité, une dépendance vulnérable, une erreur de configuration), les couches suivantes doivent limiter les dégâts plutôt que d'exposer directement les données.

## Couche 1 — Réseau et conteneurs

- **Un seul point d'entrée public** : seul le reverse proxy publie un port vers l'extérieur (443). Tous les autres conteneurs communiquent via un réseau Docker interne (`internal: true` pour le réseau données).
- **Segmentation en trois réseaux Docker** : `edge` (proxy ↔ API), `app` (API ↔ worker/scheduler), `data` (API/worker ↔ DB/Redis/storage). Un conteneur compromis dans `edge` ne peut pas atteindre directement `data`.
- **Aucun conteneur ne tourne en root** : chaque `Dockerfile` définit un utilisateur non privilégié (`USER app`) avant l'exécution.
- **Images de base minimales** (`alpine` ou `distroless`) pour réduire la surface d'attaque et le nombre de paquets à surveiller.
- **Secrets jamais dans l'image ni dans le repo** : injectés via Docker secrets ou un gestionnaire dédié (voir couche 3), jamais via des variables d'environnement en clair commitées.
- **Scan d'image obligatoire avant déploiement** (Trivy, Grype, ou équivalent) intégré à la CI — aucune image avec vulnérabilité critique connue ne doit atteindre la production.

## Couche 2 — Application

- **Validation stricte de toute entrée** à la frontière de l'API (schéma de validation systématique — ex. Zod/Joi côté Node, Pydantic côté Python), avant toute logique métier.
- **Requêtes paramétrées uniquement** — jamais de concaténation de chaîne SQL, même pour un besoin ponctuel. Utiliser l'ORM ou le query builder de façon systématique.
- **Rate limiting par endpoint et par identité** (IP + compte), particulièrement strict sur les routes d'authentification et de webhook — un webhook mobile money reçoit un rate limit différent d'une route de consultation classique.
- **En-têtes de sécurité systématiques** : `Content-Security-Policy`, `Strict-Transport-Security`, `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY` — configurés au niveau du reverse proxy, pas laissés au hasard de chaque route.
- **CORS restrictif** : liste blanche explicite des origines autorisées (l'app mobile/web Djassa, pas de wildcard `*`).
- **Vérification obligatoire de la signature de chaque webhook mobile money** avant tout traitement — c'est le point d'entrée le plus exposé du système (voir section dédiée plus bas).
- **Aucun message d'erreur détaillé exposé au client** en production (pas de stack trace, pas de nom de table ou de requête) — les détails vont dans les logs internes, jamais dans la réponse HTTP.

## Couche 3 — Secrets et identité applicative

- **Gestionnaire de secrets dédié** (HashiCorp Vault, AWS Secrets Manager, ou a minima Docker secrets en environnement contraint) — jamais de `.env` committé, jamais de clé API en dur dans le code.
- **Rotation des clés d'API des partenaires** (agrégateur de paiement, opérateurs mobile money) planifiée et documentée, pas laissée indéfiniment identique.
- **Un identifiant de service distinct par conteneur** pour accéder à la base de données, avec des permissions strictement limitées à ce dont ce service a besoin (le worker n'a pas besoin des mêmes droits que l'API d'administration).
- **JWT à courte durée de vie** (15–30 min) pour les sessions utilisateur, avec refresh token séparé et révocable — jamais de token à durée de vie longue pour l'authentification applicative.

## Couche 4 — Données

- **Chiffrement au repos** de la base de données (chiffrement natif PostgreSQL/volume chiffré) et du stockage objet.
- **Chiffrement en transit systématique**, y compris entre conteneurs internes si l'environnement de déploiement le permet (mTLS interne en option avancée, TLS obligatoire vers l'extérieur).
- **Minimisation des données personnelles** : ne stocker que ce qui sert directement l'utilisateur (voir `dkassa-inclusion-financiere.md`, principe déjà posé pour le produit) — un numéro de téléphone peut être partiellement masqué dans les logs et les interfaces d'administration.
- **Sauvegarde chiffrée et testée régulièrement** — une sauvegarde qui n'a jamais été restaurée en test n'est pas une sauvegarde fiable.
- **Séparation des environnements** : les données de production ne doivent jamais être copiées telles quelles vers un environnement de test ou de développement sans anonymisation préalable.

## Couche 5 — Identité et contrôle d'accès (RBAC)

- **Rôles distincts et explicites** : client, commerçant, agent commercial, administrateur Djassa, partenaire IMF (accès score en lecture seule, jamais accès à la base complète). Chaque rôle a un périmètre d'API strictement défini.
- **MFA obligatoire pour tout accès administrateur** au tableau de bord interne ou à l'infrastructure — pas seulement recommandé.
- **Journal d'audit immuable** de toute action sensible (modification de score, validation manuelle d'un crédit, accès à des données d'un tiers) — qui a fait quoi, quand, avec quel compte.
- **Principe du moindre privilège appliqué aux partenaires externes** : une IMF partenaire accède au score et à l'historique nécessaires à sa décision de crédit, jamais à l'ensemble des données de l'utilisateur.

## Couche 6 — Validation spécifique des webhooks mobile money (point critique)

C'est le point d'entrée le plus exposé du backend Djassa : une donnée externe, non authentifiée par défaut, qui déclenche un mouvement d'argent ou une mise à jour de solde si elle est acceptée à tort.

- Vérifier la **signature cryptographique** fournie par l'agrégateur (CinetPay et la plupart des opérateurs fournissent un secret partagé ou une clé publique pour signer chaque callback) avant tout traitement.
- Vérifier que le **montant et l'identifiant de transaction** du webhook correspondent à une transaction initiée côté Djassa — ne jamais créditer un compte sur la seule foi du webhook sans réconciliation.
- **Idempotence obligatoire** : un même webhook reçu deux fois (retry réseau côté opérateur) ne doit jamais créditer deux fois.
- **Timeout et retry contrôlés** : si le traitement échoue, renvoyer un code d'erreur clair à l'opérateur pour déclencher son propre retry, plutôt que de risquer une perte silencieuse d'événement.
- **Réconciliation quotidienne automatisée** entre les transactions enregistrées côté Djassa et l'historique fourni par l'agrégateur — détecte tout écart avant qu'il ne devienne un problème comptable ou de confiance.

## Couche 7 — Observabilité et détection

- **Logs centralisés**, jamais uniquement locaux à un conteneur qui peut disparaître à tout moment.
- **Alertes sur anomalies de transaction** : pic inhabituel de webhooks, montants hors norme, tentatives d'authentification répétées échouées — utile autant pour la sécurité que pour la détection de fraude déjà documentée comme un risque réel du mobile money en Côte d'Ivoire.
- **Séparation stricte logs applicatifs / logs contenant des données personnelles** — un log de debug ne doit jamais contenir un numéro de téléphone complet ou un montant en clair sans nécessité.
- **Plan de réponse à incident documenté** avant le premier incident réel, pas après : qui est prévenu, comment un compte compromis est gelé, comment un partenaire (IMF, opérateur) est notifié.

## Conformité réglementaire à ne pas oublier

- **Loi ivoirienne sur la protection des données personnelles** (n°2013-450) — l'ARTCI est l'autorité de régulation ; toute collecte de donnée doit avoir une finalité déclarée et un consentement explicite, cohérent avec les garde-fous déjà posés dans `dkassa-inclusion-financiere.md`.
- **Cadre BCEAO sur les agréments EME/EP** — rappel : aucune fonctionnalité de mouvement de fonds ne doit être déployée en production sans validation préalable du statut réglementaire requis (voir `dkassa-inclusion-financiere.md`, section contraintes réglementaires).
- **Conformité PISPI** (interopérabilité des paiements) obligatoire pour tout établissement financier partenaire à partir du 30 juin 2026 — à vérifier avec chaque partenaire de paiement avant intégration.

## Checklist avant tout déploiement en production

- [ ] Aucun secret en dur dans le code ou l'image Docker
- [ ] Tous les conteneurs tournent avec un utilisateur non-root
- [ ] Scan de vulnérabilité des images passé sans faille critique
- [ ] Signature des webhooks vérifiée et testée avec des cas invalides
- [ ] Rate limiting actif sur toutes les routes publiques
- [ ] En-têtes de sécurité vérifiés (CSP, HSTS, X-Frame-Options)
- [ ] Sauvegarde restaurée avec succès en environnement de test dans les 30 derniers jours
- [ ] RBAC testé pour chaque rôle, y compris les tentatives d'accès hors périmètre
- [ ] Plan de réponse à incident revu par l'équipe