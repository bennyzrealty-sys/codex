# Layer 27 research packet — "What else is buildable" (snapshot 2026-08)

This document is the output of the August 2026 research session on widening Layer 27
("From Zero to Your Own AI") beyond its four original builds. It contains:

1. The synthesis — buildable segments with demand, organized as a capability ladder.
2. Emerging spaces and why now.
3. Honesty revisions the research forces on the four existing builds.
4. The edit plan for Layer 27 (a later session executes it in `index.html`).
5. A ready-to-run deep-research brief for the next round: emerging cybersecurity
   threats and unsolved problems.

All facts below are snapshot-dated **August 2026** and should be marked as such when
they land in codex cards.

---

## 1. Synthesis — the capability ladder of buildables

The organizing idea mirrors the existing shopping ladder (`l27-spending-ladder`):
each hardware/capital tier unlocks a different menu of things worth building.
The ladder is an **OR, not an AND** — see §4 (ladder clarification).

### Tier 1 — Pi + rented GPU + APIs (solo, ~£0–200): start this month

Ranked by evidence strength for this operator:

1. **AI phone receptionist / voice agents for one UK trade or clinic niche.**
   Best evidence of the whole study. UK SMBs pay £59–199/mo; inbound answering is
   52% of voice-agent revenue; Avoca reached a $1B valuation. Buildable on
   Vapi/Retell — no GPU required.
2. **Productised AI implementation service in one vertical.** Most solo-buildable;
   78% of successful SMB AI deployments used an external partner. This is the
   funnel that reveals which SaaS to extract later.
3. **Private LLM+RAG for professional firms — as a productised service**, not SaaS:
   install £2–5k + retainer; the Pi-as-appliance is the pitch.
4. **EU AI Act SME compliance packs + Article 4 literacy training.** Enforcement
   began 2 Aug 2026; enterprise platforms ignore SMEs. Time-boxed window; the
   high-risk wave returns in 2027.
5. **Ambient scribes for unsaturated professions** (vets, physios, letting agents).
   The Heidi playbook is proven (£30–100/user/mo; half of UK GPs); the giants
   haven't covered adjacent niches.
6. **Vertical AI agents — one workflow, one boring industry** (freight quoting,
   UK lettings admin, niche recruitment). $3.07B went into agent startups
   Aug 2025–Jul 2026; the moat is workflow depth + integrations.
7. **Document/data extraction for SMB back offices** (invoices/tenancy docs/CVs →
   Xero/Sage/TMS). IDP market ~$4B growing 16%+; enterprise vendors ignore
   sub-£5k/yr buyers.
8. **MCP servers/integrations.** The standard won (Linux Foundation, Dec 2025);
   payment rails are new (Stripe MPP Mar 2026, x402). Early; best as
   wrapper/distribution for another product.
9. **LLM red-teaming/evals as a service** — service, not platform (the platform
   war is over: Statsig→OpenAI $1.1B, W&B→CoreWeave).
10. **C2PA provenance workflow tooling for niches** (insurance claims, lettings
    inventories) — the solo-accessible corner of synthetic media; detection
    itself is not.
11. **GEO (generative engine optimization) monitoring/services.** Only 16% of
    brands track AI-search visibility; thin moat, fast window.
12. **Fine-tuned SLM endpoints / edge appliances.** 90% cost cuts vs frontier APIs
    documented; Pi + rented GPU is an actual advantage; moat = accumulated niche
    data. (Bridges into Tier 2.)

**Strongest five for this operator:** voice receptionist in one UK niche;
productised implementation service (the funnel); private RAG appliance as a
service; EU AI Act SME pack (window open now); scribe/agent for an unsaturated
UK profession.

### Tier 2 — "After the laptop" (~£1.5k+: 36–48GB+ Apple-Silicon Mac or mini-PC + 16–24GB NVIDIA, plus hourly A100/H100)

Through-line: the Pi could only orchestrate other people's cloud models; this tier
runs a genuinely capable model on your own metal and rents an 80GB card for the few
jobs (training, video) it can't do. **"Own-metal baseline + rent-the-spike."**

The delta the hardware unlocks:

- **30–70B local inference.** Llama 3.3 70B / Qwen 72B at Q4 = 20–35 tok/s on a
  64GB+ Mac; a 24GB NVIDIA card tops out around 30B. Private assistants good
  enough to bill for (84% of orgs want on-prem/edge — IDC).
- **Local agentic-coding model.** Qwen3-Coder 30B (~220 tok/s), Devstral 24B
  (46.8% SWE-Bench); private agent loops offline / air-gapped.
- **Real QLoRA fine-tuning on a rented A100/H100.** A 7B run costs ~$3–10 over
  2–4h; a 70B run ~$20–50. The biggest capability jump of the tier: you produce
  an **owned weight file**, not just prompts. This is CUDA territory — the Mac
  does the demo, the rented NVIDIA card does the run.
- **Fine-tuned vertical SLM endpoints as product.** 5–20× cheaper than frontier
  at volume; the weight file is resellable IP; you carry the eval/maintenance
  burden.
- **Local image generation** (Flux/SDXL via ComfyUI). FLUX.2 klein (Jan 2026) is
  Apache-2.0, the first fully commercial-friendly Flux; sell
  workflows-as-a-service; licensing is a minefield per model.
- **Local/rented video** (LTX/Wan/Hunyuan) — mostly still a rented-GPU job;
  16GB local = previews only; price the GPU cost in.
- **Voice cloning/TTS trained and owned** (XTTS-v2, F5-TTS, Fish Speech on your
  GPU) — an owned offline brand voice; consent/deepfake/UK-DP liability is yours.
- **The on-prem AI appliance you build and sell.** Mac Studio/Mini, mini-PC, or
  DGX Spark (128GB, ~£3–4k) preloaded with a fine-tuned model + RAG, air-gapped.
  Entry boxes list $8–12k; break-even 3–6 months; hardware margin + recurring
  support. The ops burden is real.
- **Deeper on-prem RAG** — full embed+store+generate on one private box with
  quality answers; upgrades the existing best market to credibly fully on-prem
  (price and win-rate uplift).
- **Synthetic data at volume** — 10k–100k filtered rows generated privately;
  feeds fine-tuning; curation is the whole game (else model collapse).
- **Local agent swarms** — parallel agent grunt-work on owned metal without
  metering an API; hybrid (local volume + frontier adjudication) is safest.

Still needs rented GPU / not viable at this tier: client-grade video (40–80GB),
any real 34–70B training (CUDA rental), multi-user production serving,
frontier-quality reasoning, full pretraining / large RLHF, and
laptop-as-24/7-server (thermals — use a Studio/Mini/desktop).

**Biggest three vs the Pi:** (1) you can TRAIN, not just prompt; (2) a useful
private model runs on your box (regulated clients, price uplift); (3) the box
itself becomes a higher-ticket product.

### Tier 3 — Enterprise / funded (revenue or investment £250k–£5M+, small team)

Framing: the constraint shifts from your hours to capital + team. The solo-traps
become defensible only with a standing team defending a moat (data, adversarial
ML, on-call, certifications) AND the enterprise sales motion to monetise it.
Backdrop: 2026 AI seed median ~£3.6M; Series A infra/agent rounds $20–120M. You
are NOT competing at the foundation-model tier — you play the
application/vertical/infra-services layer.

Unlocked (traps that become viable at scale):

- **LLM observability/eval platform** — Braintrust $80M Series B at ~$800M
  valuation; needs 24/7 ingestion + certs + an ML team; late entry with <£5M is
  likely too little.
- **Enterprise AI governance platform** — Credo AI $42M; moat = regulatory
  content + government trust; 72% of enterprise buyers screen for ISO 42001.
- **Deepfake detection** — Reality Defender $48M; needs proprietary datasets +
  a permanent adversarial-ML team (the model decays weekly); an opex-forever
  treadmill.
- **Horizontal anti-bot** — a network-effect product; needs customer density
  before the signal works; "buy your way to the network effect."
- **Text-to-video** — even the funded tier should NOT chase frontier (Sora app
  shut Mar 2026: $1M/day burn against $2.1M lifetime revenue); the viable play
  is specialised licensed-data video on open weights for one vertical.
- **US healthcare RCM/prior-auth core** — >$500M into RCM AI in 2026 (Candid
  $120M, Cohere Health $90M); needs HIPAA + payer integrations + clinical SMEs;
  steep for a UK founder.
- **Fine-tuning / continued-pretraining at scale + domain foundation models** —
  multi-GPU SFT/RLHF needs a labelling operation + platform team; open-weight
  bases (e.g. Thinking Machines "Inkling") let you own a domain model without
  frontier pretraining ($10M–$500M stays out of reach).
- **The data moat** (licensed/curated datasets + a human-in-the-loop team) —
  the single most defensible use of capital; survives model commoditisation.
- **Real multi-tenant SaaS with SLAs** — SLAs imply 24/7 on-call (impossible
  solo); the price of 5-figure+ ACV deals.
- **Going up-market in the real segments** — voice agents → enterprise contact
  centre ($4.5B raised by voice-AI firms; Avoca $1B, EliseAI $250M at $2.2B);
  vertical agents → category vertical SaaS (62.7% CAGR, "eating horizontal
  SaaS"); private AI → sovereign/on-prem ($24.8B → $301.6B by 2040); agent
  security → enterprise platform.
- **The enterprise sales motion itself** (the meta-unlock) — PLG → design
  partners → direct sales/RFPs/MEDDPICC; this is what actually monetises the
  rest (Legora: $1M → $100M ARR in 18 months).

**Rent-vs-own GPU crossover:** an 8×H100 node is ~$285k; H100 rent is
$1.49–2.69/hr on neoclouds; reserved discounts 15–30% (up to 60% on long
commits); break-even ~14,000 GPU-hours ≈ 18–19 months at full 24/7 use.
Rule: below ~40% sustained utilisation → rent; above 40% (especially 24/7
inference) → reserve or own. Depreciation trap: H100 rental fell 64–75% from
Q4 2024 to early 2026, so reserved cloud usually beats ownership except for
predictable high-utilisation loads. Ladder: on-demand (spiky) → reserved
neocloud (steady baseline) → buy + colocate (proven >40% 24/7 floor).

**Certifications are sales unlocks, not nice-to-haves:** Cyber Essentials UK
(~£300–500, days, the government floor — do first) → ISO 27001 (mid-£k,
6–12 months; financial/health/public sector) → ISO 42001 AI (£75k–250k+,
6–12 months, or 4–6 months if you hold 27001; 72% of buyers screen for it) →
SOC 2 Type 2 in parallel (US/mid-market table stakes) → HIPAA (mandatory for US
health data). Combined 27001 + 42001 + SOC 2 = maximum credible enterprise AI
vendor posture in 2026.

**What to do FIRST when money arrives:** (1) pick ONE vertical where you have a
data/domain edge; (2) start Cyber Essentials day one and queue 27001 → 42001 →
SOC 2 (the 6–12-month clocks gate every deal); (3) sign 2–3 design partners
before building the platform; (4) reserve neocloud GPU — don't buy hardware yet;
(5) spend capital on the data moat, not frontier training; (6) hire enterprise
sales + an on-call SRE, not just ML; (7) still avoid frontier text-to-video,
cold-start horizontal anti-bot, and late governance/observability platforms.

---

## 2. Emerging spaces — why now (trigger-framed)

- **Agentic payments rails (x402/AP2/ACP).** x402 Foundation under the Linux
  Foundation Jul 2026; Stripe integrated Feb 2026; ~$600M annualized volume.
  Solo-fit HIGH: build ON the rails (x402-metered APIs / MCP servers), not the
  rails themselves.
- **MCP server economy.** 10k+ servers, <5% monetized — a "pre-monetization App
  Store"; the registry is live. Solo-fit HIGH: paid vertical servers, MCP
  security auditing.
- **Agent security.** 367 vendors, $3.6B raised; Bessemer calls it "the defining
  cybersecurity challenge of 2026." Solo-fit MEDIUM: niches only (red-team
  datasets, MCP scanners, pentest services).
- **Agent identity / delegated auth.** Entra Agent ID GA Apr 2026, Okta XAA;
  a greenfield integration layer. Solo-fit MEDIUM-HIGH: SDKs/middleware/
  consulting, not an IdP.
- **SMB voice agents over telephony.** Latency crossed the human threshold;
  buyers are paying now; the app layer is wide open. Solo-fit: HIGHEST near-term
  revenue (matches Tier 1 #1).
- **On-device speech-to-speech.** Kyutai Pocket TTS (Jan 2026) runs real-time on
  CPU — i.e. on the Pi 5. A build-ahead bet that fits the hardware exactly.
- **Local/private AI as a product category.** Ollama at 52M downloads/mo;
  privacy is the #1 enterprise barrier; no "private AI in a box" brand yet.
  Solo-fit HIGH; the only category where the Pi is a differentiator.
- **EU AI Act tooling.** Article 50 live 2 Aug 2026; compelled payers; the SME
  tier is open.
- **C2PA provenance tooling** (ride the mandate) vs deepfake detection (a
  team-scale arms race; CEO-deepfake fraud hits ~400 companies/day).
- **LLMOps evals** — consolidating (Gartner Market Guide Feb 2026;
  Promptfoo→OpenAI, Langfuse→ClickHouse); enter only via vertical eval suites /
  adversarial datasets.
- **Healthcare admin agents** — strongest proven demand; solo only at the
  micro-practice tier.
- **AI tutoring** (niches: non-English, special-needs) and **AI eldercare**
  (voice check-ins, Pi-based in-home monitors) — real need, distribution hard.
- **Open VLA robotics** (LeRobot/SmolVLA, <$300 arm) — a learning/option-value
  bet, not revenue.
- **Agent-readable web / "AX" services** — ai-catalog.json (Jun 2026),
  Lighthouse agentic audit; the "SEO agency in 1998" moment; zero capital.

**Hype flags:** agent marketplaces, world models (for solos), generic LLMOps
platforms, generic consumer tutoring, eldercare market-size projections.

---

## 3. Honesty revisions to Layer 27's four existing builds

The research contradicts the current text; these edits are required, not optional:

- **Video generator → trap.** Text-to-video is a capital bonfire (Sora app shut
  down at $15M/day burn across the segment; API prices collapsed). Selling this
  is a trap; thin niche apps on top are the only lane. Keep the build as
  education, kill it as a business.
- **Voice model → pivot.** Raw TTS / voice-cloning APIs are in a 14–28× price
  war. Pivot the skill into **voice agents on telephony** (Tier 1 #1); keep the
  owned-voice-model angle as a Tier 2 build.
- **Anti-bot detector → narrow.** The horizontal scoring API is incumbent-owned
  (Forrester Wave) and needs cross-site signal a solo can't see. The solo lane is
  agent-security/red-team services and niche detection (agent-access analytics
  for publishers at most).
- **Private LLM+RAG → validated, but as a service.** Not SaaS: productised
  install (£2–5k) + retainer, Pi/box-as-appliance.

---

## 4. Layer 27 edit plan (for the implementation session)

All new cards in the codex's two-voice format (plain + tech), snapshot-dated
2026-08, cross-referenced to Layers 04/23/25.

1. **New subsection "What each tier lets you build"** after
   `l27-use-cases-and-money`, containing three cards:
   - **"Tier 1 — what the Pi + rented GPU builds"** (~£0–200): the ranked
     segments from §1 Tier 1, each with who-pays-now + one-line demand evidence.
   - **"Tier 2 — what the laptop unlocks"**: the delta from §1 Tier 2 —
     headline "you can TRAIN, not just prompt" (owned weight files as IP).
     Caveat box: training is CUDA-rented, not Mac-local; client-grade video
     still needs the rented card; laptop ≠ 24/7 server (thermals).
   - **"Tier 3 — what money and a team unlock"**: solo-traps that become
     defensible at scale, rent-vs-own GPU crossover (>40% utilisation rule),
     certification ladder as sales unlock, "what to do FIRST when money
     arrives." Explicit "even here, don't chase" note: frontier text-to-video,
     cold-start anti-bot, late platform plays.
2. **New card "Emerging spaces — why now"**: the trigger-framed list from §2,
   with hype flags.
3. **Honesty edits to the four existing builds** per §3.
4. **Ladder/Mac clarification** in `l27-spending-ladder` +
   `l27-best-laptop-buy-build-rent`: the ladder is an OR, not an AND — a £1,500
   Mac makes the £200/£500 rungs redundant but not the £50 NVMe rung (the Pi
   keeps the always-on role); Mac ≠ CUDA (rental credit survives for training);
   70B-at-48GB is a stretch, comfort band ~30B; bandwidth varies by chip tier.
5. **Glossary additions** (only if the terms appear in the new cards): x402,
   MCP monetization, C2PA tooling vs detection, GEO, agent identity, ISO 42001,
   neocloud, unified-memory-vs-CUDA.

---

## 5. Next deep research — cybersecurity brief (ready to run)

**Goal:** feed a future codex layer/card — what's emerging in cybersecurity,
the newest threats, and what remains unsolved. Round 1 already surfaced leads to
chase: agent security as "the defining challenge of 2026" ($3.6B, 367 vendors,
Lakera→Check Point), CEO-deepfake fraud ~400 companies/day, real-time
KYC-liveness defeat, x402 free-riding/PII-leakage papers, agent identity
(Entra Agent ID, Okta XAA).

**Five research questions:**

1. **New threat classes 2025–26:** AI-enabled offense (agentic malware,
   LLM-assisted vulnerability discovery/exploitation, polymorphic generation),
   prompt-injection attacks in the wild against deployed agents,
   deepfake-enabled fraud (voice vishing, KYC bypass, BEC 2.0), supply chain
   (npm/PyPI/model-hub poisoning, malicious MCP servers, backdoored
   fine-tunes/LoRAs), the infostealer economy, ransomware evolution.
2. **New attack surfaces:** agentic AI itself (tool-use hijacking, memory
   poisoning, the lethal trifecta in production), MCP/A2A protocol weaknesses,
   agent payment rails (x402 abuse), model-weight theft, edge/IoT AI devices,
   non-human identities at scale.
3. **Defence-side buildable segments** (the codex's angle — build/sell the
   shield): agent guardrails and MCP scanners, red-team datasets/services,
   AI-SOC triage, non-human-identity management, C2PA/provenance, continuous
   pentesting, SBOM tooling, post-quantum migration services. For each: who
   pays, and solo vs team-scale.
4. **Unsolved problems:** prompt injection (no general fix — verify current
   state), agent authorization/delegation semantics, provenance in an
   open-weights world, the deepfake-detection arms race, attribution,
   interpretability at scale, PQC migration timeline vs "harvest now, decrypt
   later".
5. **The line:** keep detection/defence only, consistent with the Deep Field
   boundary — mechanisms explained for comprehension, no offensive artifacts.

**Method:** 12–18 searches across:
- Vendor threat reports: CrowdStrike Global Threat Report, Mandiant M-Trends,
  Microsoft Digital Defense Report, Verizon DBIR, ENISA Threat Landscape,
  IBM X-Force, Sophos/Recorded Future ransomware trackers.
- Government/CERT: NCSC UK annual review + advisories, CISA advisories/KEV,
  Europol IOCTA.
- AI-specific: OWASP Top 10 for LLM Applications + OWASP Agentic Security
  Initiative, MITRE ATLAS, model-hub incident reports, MCP security research,
  arXiv on prompt injection / agent hijacking (verify claims against deployed
  incidents, not just lab demos).
- Market/funding: agent-security funding rounds, acquisitions (Lakera→Check
  Point class), analyst coverage (Bessemer, Gartner) — to rank the defence-side
  buildables by who-pays evidence.
- Cross-check every "in the wild" claim against at least two independent
  sources; date-stamp everything; separate demonstrated-in-lab from
  observed-in-production.

**Output format:** structured findings mapped to the five questions, each item
carrying (threat/surface/segment, evidence + date, solo-fit or team-scale,
unsolved-or-solved status), ready to convert into codex cards with the same
two-voice format and snapshot date.
