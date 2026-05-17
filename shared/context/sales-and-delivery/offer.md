# Offer — DivineSide

> **What we sell, what we promise, what we charge.** Universal across channels (cold email, Upwork, LinkedIn, inbound): same offer, same guarantee, same payment model. Pricing is per-project, anchored at the numbers in §03, and is currently being tested.
>
> The guarantee deep-dive (TYPE A / TYPE B verbatim, claim mechanic, voids) lives in [`guarantee.md`](guarantee.md). This file is the strategic offer; that file is the legal mechanic.
>
> **Loading discipline** — any agent or human running outreach, sales calls, audits, or proposals should load:
> 1. [`../identity/business-info.md`](../identity/business-info.md) — what we sell, what we don't
> 2. [`../identity/audience.md`](../identity/audience.md) — who we sell to (channel-specific)
> 3. [`../identity/voice.md`](../identity/voice.md) — brand tone
> 4. **This file** — the unified offer
> 5. [`guarantee.md`](guarantee.md) — the guarantee mechanic (TYPE A/B, what triggers, what voids)
> 6. [`sales-playbook.md`](sales-playbook.md) — the process wrapped around the offer
> 7. [`sales-discovery-call.md`](sales-discovery-call.md) — for the live call

Last updated: 2026-05-17

---

## 01 · The headline promise

**"Your business, running on AI."**

Long-form, what we say on calls, in the audit doc, in the proposal:

> *"In 8 weeks, we build the AI brain that learns your business and runs the repetitive work for you. You don't pay anything upfront. You only pay when we've delivered what we agreed at kickoff. If we miss the target, you don't pay anything, and I pay you $500 out of my own pocket for the time you committed."*

Universal across channels. The specific *target* depends on the guarantee variant (TYPE A or TYPE B); see §04 and [`guarantee.md`](guarantee.md).

### Naming discipline

- **External / customer-facing default:** *"Your business, running on AI."* Lead with the outcome, not the category noun.
- **Internal / strategy / repo:** *AI Operating System.* DivineCore is the internal AI OS; every client build is an AI OS for that brand. CLAUDE.md uses this language; don't change internal vocabulary.
- **In-call frame** when a prospect asks *"what is this exactly?":* *"It's the AI brain for your business. It learns how you do things, then runs the repetitive work for you."*
- **Upwork channel exception** (per [../../../CLAUDE.md](../../../CLAUDE.md) §13 and [../../../sales_os/integrations/upwork/.overview.md](../../../sales_os/integrations/upwork/.overview.md)): the application body and Loom lead with the AIOS framing because on Upwork specifically AIOS is the differentiator that justifies the price floor. Verbatim sentence: *"I don't build commoditized automations. I build AI Operating Systems: your business, running on AI."*

---

## 02 · The pilot

**8 weeks, fixed shape.** What we build varies brand to brand. The shape doesn't.

### Phases

| Weeks | Phase | What happens |
|-------|-------|--------------|
| 1-2 | **Context** | We learn the business (products, voice, SOPs, decisions, why you do things the way you do). This becomes the AI brain. |
| 3-4 | **Data** | We connect the brain to the business (Shopify, Klaviyo, Gorgias, Meta, GoHighLevel, whatever's relevant). Now it sees what's happening in real time. |
| 5-7 | **Build** | We ship the workflow that takes the specific repetitive task off the team's plate. Live, monitored, used daily. |
| 8 | **Verify** | Delivery test against the kickoff spec (TYPE B) or the hours-saved baseline (TYPE A). Buyer pays. |

### Deliverables at the end of week 8

- The AI brain (a maintained context layer about the business)
- One live workflow that demonstrably performs the function we agreed on (TYPE B) or saves 10+ hrs/week (TYPE A)
- Documentation of what we built and how to extend it
- A 30-day support window where we tune the workflow as the team uses it

---

## 03 · Pricing

**All pricing is per-project, agreed at kickoff before any work begins.** Pricing is currently in test mode, anchored around the numbers below, refined as we run more pilots.

### Anchors (provisional, May 2026)

| Item | Anchor | Notes |
|---|---|---|
| **Pilot (one workflow, 8 weeks)** | ~£2.5k | Varies by scope. Higher for complex builds, lower for straightforward ones. |
| **Foundation retainer (post-pilot)** | ~£2.5k / month | Default-on after the pilot ships. Context maintained + monitoring + weekly 30-min check-in + up to 2 active workflows. |
| **Each additional active workflow** | +£500 / month | On top of the Foundation retainer. |

### Payment

- **0% upfront.** Buyer commits to the price at kickoff but pays nothing until delivery.
- **100% on delivery**, conditional on the guarantee (see §04 and [`guarantee.md`](guarantee.md)).

The payment model is the same across all channels. No "founding partner" discount or tiered pricing. Every pilot is quoted per-project from kickoff, with the £2.5k anchor as the rough starting point.

---

## 04 · The guarantee

**You only pay when the system is delivered and we've verified it does what we agreed at kickoff. If we miss the target at the delivery test, you don't pay me anything, and I pay you $500 out of my own pocket for the time you committed.**

Two variants:

- **TYPE B (functions-delivered, DEFAULT).** Use for the vast majority of JDs and prospects. The trigger is "a function in the signed spec doesn't work, work correctly, or is missing at the week 8 delivery test."
- **TYPE A (hours-saved).** Use only when four signals are all present (see [`guarantee.md`](guarantee.md) §02). The trigger is "the system fails to save the team at least 10 hours per week by the end of month two."

Full deep-dive in [`guarantee.md`](guarantee.md), including: the four-signal test for picking TYPE A, the verbatim paragraphs as they appear in the application body and proposal Doc, what does NOT trigger the guarantee, buyer obligations during the build, what voids the guarantee on the buyer's side, and the claim mechanic.

The guarantee terms are the same across channels. Only the variant (A vs B) depends on the specific JD or prospect.

---

## 05 · Scope envelope

The pilot is **fixed in shape, variable in subject.** Inside the envelope:

- **One workflow per pilot.** Not "1-2." One.
- **Buildable in ≤2 weeks of engineering** (within the 8-week pilot framework; the rest of the time is context, integration, testing, refinement).
- **Uses APIs we can access.** Standard stack (Shopify, Klaviyo, Gorgias, Meta, Google, OpenAI/Anthropic, etc.) is fine. Niche internal tools are case-by-case.
- **Measurable.** TYPE A in hours saved, TYPE B against a function checklist.

Anything outside this envelope = separate engagement, separately priced. Don't wedge it into the pilot.

---

## 06 · What needs its own engagement

Real and valuable, but **not** in the pilot:

- More than one workflow at a time (each additional = its own scope + price)
- Workflows requiring custom hardware or physical logistics
- Workflows requiring data we don't have API/permissions for
- Migrations from old tools or large-scale data clean-up
- Training programs or hiring support for client staff
- Anything taking more than 2 weeks of engineering

If a prospect wants any of these, scope and price separately in the audit doc. Don't pretend they fit.

---

## 07 · Expansion path

The pilot proves one workflow. The retainer keeps it running and adds the next ones, one at a time.

**Order of expansion:**
1. Same brand, same department, **second workflow** (e.g., CS triage → CS draft responses)
2. Same brand, **second department** (e.g., marketing pilot → returns automation)
3. Same brand, **full operational coverage** (compounding across functions)

**One task at a time, one department at a time.** Don't sell breadth before depth. The brand should feel the win on workflow #1 before they're scoped for workflow #2.

This is also how the AI brain (context layer) compounds. Each new workflow runs faster and cheaper than the last because the brain is already trained on the business. By workflow #4, *they* describe it as their AI operating system. You earn the platform language by showing the value, not by claiming it.

---

## 08 · Channels: same offer, different audiences

The offer is universal. The **audience** and **naming discipline** differ by channel:

| Channel | Audience | Naming discipline |
|---|---|---|
| **Cold email** | UK skincare/beauty e-comm brands, £500k-£5M revenue, 5-50 employees | Outcome-first (no AIOS) |
| **Upwork** | Open, qualify on budget + fit | AIOS-first (channel exception per §01) |
| **LinkedIn DMs / inbound** | Open, qualify on budget + fit | Outcome-first |
| **Warm intro / network** | Open, say yes if budget exists | Outcome-first |

The **payment model, guarantee, pricing anchor, scope envelope, and expansion path** are the same across all channels.

---

## 09 · What this doc is, what it isn't

**It is:**
- The unified offer for **all channels** (cold email, Upwork, LinkedIn, inbound) as of 2026-05-17.
- The training doc any agent generating proposals, audit docs, or sales pitches loads from.
- A living doc, revised after every 3-5 pilots once we know what works.

**It isn't:**
- The guarantee deep-dive. That's [`guarantee.md`](guarantee.md): TYPE A vs B classification rules, verbatim paragraphs, claim mechanic, voids, buyer obligations.
- Final on pricing. The £2.5k pilot anchor and £2.5k/mo retainer are provisional. We'll lock them after testing.
- The cold email or call script. Those reference this doc but live separately: see [`../playbooks/outbound-playbook.md`](../playbooks/outbound-playbook.md) and [`sales-discovery-call.md`](sales-discovery-call.md).

**Update cadence:** revise once per quarter or after every 3 pilots, whichever comes first. Append a `## Lessons` section at the bottom with one-liners after each pilot.

---

## 10 · Lessons

*(Add a one-liner per pilot here. What worked, what didn't, what the actual outcome was, whether the guarantee variant + pricing landed.)*
