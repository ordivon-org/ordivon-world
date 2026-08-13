# Resource Acquisition — Human Action Handoff

This is the thin human-only edge of the R2 acquisition loop. Research, ranking, transport, credential validation, integration, quota/expiry tracking, and dogfood remain Agent work.

As-of: 2026-08-13. Revalidate owner terms at execution time if a provider changes its signup flow.

## Wave A — no-card / highest leverage

### 1. GitHub Student Developer Pack

Entry: `https://education.github.com/pack/join`

Human action:

1. Use the already active GitHub account if that is the account you want to bind to the entitlement.
2. Open GitHub Education benefits / Student Developer Pack.
3. Complete current student verification if GitHub does not already show verified student status.
4. Complete any email/MFA/CAPTCHA steps presented by GitHub.
5. Stop after the Pack/education entitlement is visibly active; do not manually redeem every partner offer yet.

Why first: one parent entitlement unlocks GitHub Pro/Codespaces and a large partner catalog. Ordivon will revalidate and rank child offers after the parent authority is proven active.

### 2. Azure for Students

Entry: `https://azure.microsoft.com/en-us/free/students/`

Human action:

1. Sign in with the Microsoft account you want to own the subscription.
2. Start Azure for Students, not the generic paid Azure subscription flow.
3. Complete academic/student verification.
4. Do not add a payment card unless the current official student flow unexpectedly requires one and we re-evaluate that change.
5. Stop when the Azure for Students subscription and credit balance are visible.

Expected current entitlement: $100 credit for 12 months, no credit card in the published student offer, with eligible free-service quotas and renewal while student status remains eligible.

### 3. GroqCloud Free

Entry: `https://console.groq.com/`

Human action:

1. Create/sign in to the GroqCloud account.
2. Complete any third-party login/email/MFA steps.
3. Generate one API key for Ordivon only if the console makes the key visible once.
4. Put the key into the existing Ordivon secrets authority, not chat or source control.

Do not upgrade to the paid Developer plan during this acquisition wave.

### 4. OpenAlex free API key

Entry: `https://openalex.org/settings/api`

Human action:

1. Create/sign in to an OpenAlex account.
2. Copy the free API key into Ordivon secrets authority.
3. Do not buy API credits; the first dogfood uses the recurring free allowance.

### 5. GBIF account

Entry: `https://www.gbif.org/`

Human action:

1. Register/sign in.
2. Verify email if requested.
3. Stop after the account is active.

The account is valuable primarily because it unlocks authenticated asynchronous occurrence downloads and citation/DOI workflows; ordinary occurrence search remains anonymous.

### 6. Hugging Face account

Entry: `https://huggingface.co/join`

Human action:

1. Create/sign in.
2. Complete verification steps.
3. Do not create a broad-scope token yet unless a real repository/API consumer requires it. Ordivon should request the narrowest token after choosing the first workload.

## Wave B — card-gated / protected free value

These are still positive expected-value acquisitions, but the human action creates a payment instrument or billing account. The initial dogfood must preserve the provider's free/no-charge mode and add spending guards before normal use.

### 7. Brave Search API

Entry: `https://api-dashboard.search.brave.com/`

Human action:

1. Create/verify the Brave Search API account.
2. Subscribe to the Search plan using the required payment card.
3. Immediately set a conservative monthly spending limit in the dashboard before issuing the production key.
4. Generate an API key and put it in Ordivon secrets authority.

Current owner model: $5 per 1,000 Search requests and an automatic $5 recurring monthly credit; usage beyond credits is pay-as-you-go, so the spending guard is part of acquisition.

### 8. Google Cloud Free Trial

Entry: `https://cloud.google.com/free`

Human action:

1. Start the Free Trial / Welcome credit flow.
2. Complete identity verification and payment-method verification.
3. Do not manually upgrade to a Paid billing account during initial dogfood.
4. Stop when the $300/90-day trial credit is visible.

### 9. AWS Free Plan

Entry: `https://aws.amazon.com/free/`

Human action:

1. Start the current new-customer Free Plan signup.
2. Enter the payment method required for identity verification.
3. Complete identity/MFA checks.
4. Choose/retain the Free Plan; do not convert to the Paid plan during initial dogfood.
5. Stop when the initial credit/free-plan status is visible.

Current owner model: $100 signup credit plus up to another $100 earned through eligible exploration, with Free Plan lasting up to six months or until credits are depleted. Final new-customer eligibility is resolved by the signup flow.

### 10. Oracle Cloud Free Tier

Entry: `https://www.oracle.com/cloud/free/`

Human action:

1. Start OCI Free Tier signup.
2. Choose the home region deliberately; Always Free capacity is region-sensitive.
3. Complete email/phone/CAPTCHA/identity steps.
4. Enter the supported payment card for identity verification.
5. Accept Oracle Cloud terms.
6. Stop after the Free Tier / trial account is active. Do not create duplicate Free Tier accounts.

Current owner model: $300 trial for up to 30 days plus Always Free resources subject to capacity and current provider policy.

## After GitHub Student Pack is active

Return control to Ordivon before manually claiming partner offers. The next Agent pass should first prove the parent entitlement and then revalidate/redeem high-value children in roughly this order:

1. DigitalOcean — current GitHub catalog advertises $200 platform credit for one year; exact new-user/payment/redemption eligibility must be checked at claim time.
2. Camber — compute/LLM resource pool.
3. Datadog — observability capacity.
4. Zyte Scrapy Cloud — external web-data acquisition surface.
5. Sentry — error/performance/replay observability with on-demand disabled in the student offer.
6. Appwrite — backend/cloud project capacity.
7. Doppler — secrets-management Team entitlement.
8. MongoDB Atlas, Deepnote, Heroku, New Relic, Clerk, Termius, 1Password, LocalStack, Name.com, JetBrains, .TECH — re-rank after exact current redemption terms are verified.

GitHub Copilot student new-plan signup is currently shown as temporarily paused in the Student Pack catalog; do not spend human time on it until the owner state changes.

## Return-to-Agent evidence

After each completed acquisition, do **not** paste credentials into chat. The desired return signal is only:

```text
<resource> 已开通，凭据已经放到 /root/.config/ordivon/secrets（或告诉你尚未生成凭据）
```

Ordivon then owns:

- proving the authority without exposing secret values;
- recording expiry/credit/quota/payment exposure;
- configuring spending/usage guards;
- selecting current network path/resolver;
- integrating into the correct consumer project;
- performing real dogfood and emitting `ConsumptionOutcome`;
- deleting or downgrading resources whose realized value is poor.
