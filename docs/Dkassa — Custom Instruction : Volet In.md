# Dkassa — Custom Instruction : Volet Inclusion Financière#2

> Ce document définit ce que Dkassa doit faire, ne doit pas faire, et dans quel ordre, pour adresser l'inclusion financière en Côte d'Ivoire. Il sert de cadre de référence pour toute décision produit, technique ou de contenu touchant à ce volet — y compris pour guider un assistant IA travaillant sur ce repo.

## Mission du volet

Dkassa part d'un programme de fidélité commerçant et transforme progressivement l'historique de transaction généré par ce programme en **passerelle vers des services financiers réels** — crédit, épargne, assurance — pour des clients et commerçants aujourd'hui exclus du système bancaire classique.

Le principe directeur : **ne jamais construire un produit financier générique**. Chaque fonctionnalité doit être justifiée par une donnée ou un comportement que Dkassa observe déjà via la fidélité, et répondre à un écart identifié dans la recherche (voir `inclusion-financiere.md`) : fort accès au mobile money, faible accès au crédit et à l'épargne structurée.

## Proposition de valeur — pourquoi un commerçant utilise Dkassa

L'argument "ça fidélise vos clients" ne suffit pas : c'est l'argument générique de tout programme de fidélité, sans lien avec l'inclusion financière. Le vrai argument de vente auprès du commerçant est différent et doit être répété dans toute la documentation et tout le discours commercial :

> **Chaque vente enregistrée via Dkassa rapproche le commerçant d'un crédit qu'il ne pouvait pas obtenir avant.**

Le mécanisme concret : un petit commerçant n'a aujourd'hui aucun moyen de prouver à une banque ou une IMF que son activité est stable et rentable — pas de comptabilité formelle, pas d'historique bancaire exploitable. Chaque transaction enregistrée via Dkassa devient, avec le temps, un **historique de chiffre d'affaires vérifiable** (régularité, volume, saisonnalité) qui peut servir de preuve de revenu pour obtenir un crédit de trésorerie, un crédit de stock, ou une avance sur recettes auprès d'une IMF partenaire ou d'un dispositif de garantie existant (SGPME, GUDE-PME). C'est un modèle déjà validé ailleurs en Afrique (avance de trésorerie basée sur les données de transaction, type Kopo Kopo au Kenya), mais pas encore capturé en Côte d'Ivoire.

**Positionnement : accélérateur, pas condition d'accès.** Dkassa ne doit jamais se présenter comme un passage obligé pour obtenir un crédit ("sans Dkassa, pas de crédit") : cette position est coercitive, fragilise la confiance des utilisateurs, et attire l'attention du régulateur sur un risque de position dominante avant même d'avoir prouvé sa valeur. Dkassa se positionne comme un **canal privilégié qui accélère et simplifie** l'accès au crédit — le commerçant ou le client reste libre d'obtenir un crédit autrement, mais Dkassa rend le parcours plus rapide et les conditions potentiellement meilleures. Toute fonctionnalité, tout partenariat et toute communication doivent respecter ce positionnement.

## Ce que Dkassa DOIT faire

### 1. Construire un historique exploitable, dès le MVP fidélité
- Chaque transaction enregistrée (montant, fréquence, régularité) doit être structurée pour être réutilisable plus tard comme donnée de solvabilité — sans attendre la V2 pour y penser.
- Le client et le commerçant doivent pouvoir consulter leur propre historique à tout moment (transparence = confiance = condition d'adoption).

### 2. Digitaliser la tontine comme porte d'entrée vers le crédit formel
- Permettre à un groupe de clients/commerçants d'organiser une tontine via l'app : cotisations automatisées par mobile money, calendrier de tour, rappels automatiques.
- Chaque cycle de tontine complété sans incident doit générer une preuve de régularité consultable, utilisable comme argument de solvabilité auprès d'un partenaire financier.
- Ne pas réinventer la tontine : respecter les règles sociales existantes (ordre du tour, montant fixe, groupe fermé) plutôt qu'imposer un mécanisme différent.

### 3. Générer un score de fiabilité interne, avant tout score de crédit formel
- Construire un score simple et explicable (régularité des achats, respect des cycles de tontine, ancienneté) — pas une boîte noire.
- Ce score sert d'abord en interne (débloquer un paiement différé chez un commerçant partenaire) avant d'être proposé à un partenaire externe (IMF, banque).
- Le score doit être compréhensible par l'utilisateur lui-même : il doit savoir ce qui l'améliore.

### 4. S'associer, ne pas se substituer, aux acteurs du crédit et de la garantie
- Dkassa ne prête pas d'argent. Le crédit réel est distribué par des institutions de microfinance (IMF), des banques partenaires, ou des dispositifs de garantie existants (SGPME, GUDE-PME).
- Le rôle de Dkassa est de fournir la donnée de solvabilité et la distribution (l'app comme canal), pas le risque de crédit lui-même.
- Prioriser les partenariats avec des acteurs déjà orientés inclusion financière (APIF, IMF locales, programmes de garantie ciblant femmes/PME/agriculture) plutôt qu'avec des banques classiques peu adaptées à ce segment.

### 4bis. Construire le volet financement du commerçant lui-même, pas seulement du client
- L'historique de chiffre d'affaires généré par un commerçant actif sur Dkassa doit pouvoir être exporté (avec son consentement) vers une IMF partenaire comme preuve de revenu, en vue d'un crédit de trésorerie, de stock, ou d'une avance sur recettes.
- Ce volet est le principal levier d'adoption commerçant : il doit être mis en avant dès le discours commercial du pilote, pas introduit seulement en phase 4 (voir phasage plus bas).
- Toujours présenter Dkassa comme un accélérateur de parcours de crédit existant, jamais comme une condition d'accès obligatoire (voir section positionnement ci-dessus).

### 5. Intégrer l'éducation financière comme composant transverse, jamais comme produit séparé
- Chaque interaction significative (premier crédit débloqué, premier cycle de tontine terminé, premier score amélioré) est une occasion d'expliquer, en langage simple, ce qui vient de se passer et pourquoi.
- Pas de module "formation" isolé que personne n'ouvre : l'éducation doit être contextuelle, au moment où elle est utile.

### 6. Respecter l'écart de genre comme priorité, pas comme option
- Suivre spécifiquement le taux d'usage féminin sur chaque fonctionnalité financière (l'écart de genre mobile money s'est creusé récemment en Afrique subsaharienne).
- Concevoir les groupes de tontine et les critères de score de façon à ne pas désavantager structurellement les femmes (ex. : ne pas pénaliser les montants de transaction plus faibles, qui reflètent souvent un accès moindre au capital plutôt qu'un manque de fiabilité).

## Ce que Dkassa NE DOIT PAS faire

- **Ne pas prétendre être une IMF ou une banque.** Toute communication doit être claire : Dkassa facilite l'accès, ne délivre pas de crédit en son nom propre, tant qu'aucun agrément BCEAO (EME/EP) n'est obtenu.
- **Ne pas construire de scoring opaque.** Un score que l'utilisateur ne comprend pas est inutilisable et contraire à l'objectif d'inclusion.
- **Ne pas viser le grand public généraliste des finances personnelles.** Ce segment est déjà occupé par un acteur régional établi (Djamo) — Dkassa reste positionné sur le commerce de proximité et les communautés d'épargne, pas sur une app de gestion financière individuelle.
- **Ne pas lancer de fonctionnalité de cash-out ou de crédit réel avant validation réglementaire.** Toute fonctionnalité impliquant un mouvement d'argent au-delà du programme de fidélité doit d'abord vérifier le cadre d'agrément BCEAO applicable (EME, EP, ou partenariat avec un établissement déjà agréé).
- **Ne pas collecter de données au-delà de ce qui sert directement l'utilisateur.** La donnée de transaction est sensible — la finalité doit toujours être explicite et bénéficier en premier lieu à la personne qui la génère.

## Contraintes réglementaires à vérifier avant chaque nouvelle fonctionnalité financière

1. Toute fonctionnalité de mouvement d'argent (cash-out, cotisation groupée, paiement différé) nécessite soit un agrément propre (EME/EP auprès de la BCEAO), soit un partenariat avec un établissement déjà agréé.
2. Toute activité de scoring crédit destinée à un tiers (IMF, banque) doit anticiper l'évolution du cadre réglementaire BCEAO sur le credit scoring, actuellement en construction — se rapprocher d'un éventuel dispositif de test encadré (regulatory sandbox) plutôt que de lancer en zone grise.
3. La conformité PISPI (interopérabilité des paiements instantanés) devient obligatoire pour tout établissement financier à partir du 30 juin 2026 — à anticiper dès qu'un partenariat de paiement est signé.

## Modèle de rémunération du volet inclusion financière

Ce volet ne remplace pas l'abonnement SaaS commerçant défini pour le MVP fidélité — il s'y ajoute, et devient à terme la source de revenu la plus importante :

1. **Abonnement SaaS commerçant** (base, dès le jour 1) — revenu indépendant du volet crédit, déjà défini pour le MVP fidélité.
2. **Commission d'apport d'affaires (referral fee)** — quand un commerçant ou un client obtient un crédit grâce à son historique Dkassa, l'IMF ou la banque partenaire verse une commission à Dkassa. C'est le modèle d'"embedded finance" (finance intégrée à un canal de distribution non-financier) déjà utilisé par des plateformes comparables ailleurs en Afrique, et c'est la source de revenu appelée à devenir la plus importante une fois les partenariats établis.
3. **Frais sur les cotisations de tontine** traitées via mobile money — petit pourcentage par transaction, sur le modèle des agrégateurs de paiement (CinetPay, etc.).
4. **Licence de données de scoring agrégées et anonymisées** à des IMF partenaires, uniquement avec consentement explicite des utilisateurs concernés — à traiter avec prudence réglementaire (BCEAO) et transparence totale vis-à-vis des utilisateurs ; ne pas monétiser cette donnée sans un cadre de consentement clair et vérifiable.

**Ce qu'il ne faut pas faire à ce stade** : prêter l'argent directement (nécessite un agrément EME/EP et du capital de risque hors de portée en phase pilote). La commission d'apport permet de capter la valeur du crédit généré sans en porter le risque.

## Phasage recommandé

| Phase | Ce qui est construit | Ce qui n'est PAS encore construit |
|---|---|---|
| **1 — MVP fidélité** (actuel) | Historique de transaction structuré et consultable ; discours commercial commerçant articulé autour de la future preuve de revenu (même si le partenariat crédit n'existe pas encore) | Tontine, score, crédit, partenariat externe |
| **2 — Tontine digitale** | Module tontine intégré, cotisation via mobile money, preuve de régularité | Score formel, partenariat financier externe |
| **3 — Score de fiabilité interne** | Score explicable, débloque un avantage chez le commerçant (paiement différé, réduction) | Transmission du score à un tiers financier |
| **4 — Partenariat crédit externe** | Score et historique de chiffre d'affaires partagés (avec consentement) à une IMF ou un dispositif de garantie partenaire ; premières commissions d'apport d'affaires | Dkassa comme prêteur direct |

Aucune phase ne démarre avant que la précédente ait été validée par un usage réel (pas seulement construite) — cohérent avec l'approche pilote déjà adoptée pour le MVP fidélité. Important : même en phase 1, le discours commercial auprès des commerçants doit déjà mentionner l'objectif de financement futur — c'est cet horizon qui justifie l'adoption, pas seulement la fidélité en elle-même.

## Indicateurs de succès du volet inclusion financière

- % d'utilisateurs actifs sur le module tontine après 90 jours
- % de cycles de tontine complétés sans incident
- Nombre de clients ayant débloqué un avantage grâce à leur score de fiabilité interne
- Écart d'usage homme/femme sur chaque fonctionnalité (suivi, pas seulement mesuré une fois)
- Nombre de partenariats signés avec des IMF ou dispositifs de garantie existants (SGPME, APIF, GUDE-PME)
- Nombre de commerçants ayant obtenu un crédit (trésorerie, stock, avance sur recettes) grâce à leur historique Dkassa
- Revenu généré par les commissions d'apport d'affaires, comparé au revenu d'abonnement SaaS (suivi de la bascule progressive vers ce second modèle)
