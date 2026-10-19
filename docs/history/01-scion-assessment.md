# AI Native Repository Design Brief

*A public protocol for verified agent work over Git*

> **Historical assessment — 18 October 2026.** This is the initial Scion assessment and its original collaboration record. Its recommendation to keep a replacement source engine conditional was superseded as the initiative's design direction by the later [agentic vision](02-agentic-vision.md). It remains useful as a record of the alternatives and correctness concerns considered. The original text below is a historical proposal, not a current implementation specification. Within this record, the main recommendation and later Claude round supersede conflicting earlier claims.

**In this document:** [Assessment](#the-opportunity-and-the-actual-bottlenecks) · [References](#primary-references) · [User transcription](#appendix-a-user-transcription) · [Claude round 1](#appendix-b-claude-response-round-1) · [Claude round 2](#appendix-c-claude-response-round-2) · [Conversion provenance](conversion-provenance.json)

*Conversion note: the original text, tables, references, and collaboration record follow. The response appendices retain their literal Markdown notation as it appeared in the Word documents. Historical source descriptions have not been refreshed.*

<!-- BEGIN ORIGINAL DOCUMENT BODY -->

ChatGPT for Rana Ian \| October 18 2026

I recommend a bounded MIT open source experiment: a portable protocol and small coordinator that make agent work, evidence, authorization, and handoffs explicit while Git remains the initial source backend. A new source object store should become a separate project only if measurements establish material source control delays that existing tools cannot resolve. This direction serves the larger ambition of a durable scientific workspace shared by GPT, Claude, and Dot, with a practical first experiment in software development.

The immediate decision is whether this additional layer produces enough verified progress to justify its maintenance. GitHub remains the canonical code host in the first pilot, with its pull requests, issues, provenance, and Dot bridge retained. This brief proposes research and design; it reports no implementation, migration, benchmark, or live Base12 telemetry.

Claude Opus 5.5 reviewed the full transcription and then a corrected proposal informed by current primary sources. Round 2 supersedes round 1 wherever they conflict, especially blanket exclusive leases, one-way synchronization, treatment of standing grants, and cache-fault claims. The appendices preserve the original transcription and both complete responses verbatim. Claude received source summaries and did not browse independently.

## The opportunity and the actual bottlenecks

Prior Base12 records report friction around action review and merging, CI capacity and repeated builds, and expensive handoffs between agents. These are historical reports, not measurements of the current system. They justify investigation but do not establish that Git storage caused the delays. A platform permission decision, a saturated runner, and a slow checkout require different remedies.

Measure elapsed time by cause before choosing the subsystem to replace. Separate repository transfer and graph queries from scheduling, build execution, verification, integration, and reacquiring context. Also record completed scientific or engineering objectives. An increase in commits can accompany repeated repairs, redundant work, or regressions; it is a weak measure of useful progress.

The most promising opportunity is continuity. An agent should recover the current goal, exact candidate, dependencies, evidence, and authorized next action without reconstructing a long conversation. Another agent should be able to challenge the result and reproduce the decisive check. That contract could be useful even where Git operations already take milliseconds.

Git already supports partial or sparse cloning and shared worktree arrangements. GitHub also provides agent workflows, review facilities, checks, and APIs. The proposed contribution must therefore be specific: portable meanings for verified work and safe continuation across tools, with demonstrated benefits over an optimized existing workflow. \[10, 11, 13\]

## Existing systems and the remaining gap

The following descriptions reflect upstream material available on October 18, 2026. They are a selection guide rather than a production qualification. Comparable names do not imply compatible protocols or equivalent maturity.

| **System**      | **License** | **Fit and limitation**                                                                                                                                                                                    |
|-----------------|-------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Anthropic Scion | Private     | Internal server-centric changesets, queries, sparse retrieval, and Antique review. No public Anthropic release found; its authors caution against general Git replacement. \[1\]                          |
| Graft           | MIT         | Gitaly-based v0.1.0 with sparse workspaces, queries, CAS or batched landing, policies, and resolver or verifier extensions. A promising adapter candidate. \[2\]                                          |
| Carter Scion    | Apache 2.0  | Independent Rust CLI, server, daemon, and one-way Git importer using CockroachDB and S3. No Git protocol or two-way sync. Early benchmarks include Git wins; production qualification remains open. \[4\] |
| OpenScion       | GPL 3.0     | Rust prototype with CLI and web surface. The roadmap separates implemented import, commit, and clone from later queries, landing, durable stores, and access control. \[5, 6\]                            |
| Jujutsu         | Apache 2.0  | Git-compatible workspaces, operation-log undo, and automatic descendant rebase. A strong existing workflow comparator, with upstream experimental qualifications. \[7\]                                   |
| Sapling family  | Mixed       | Sapling, Mononoke, and EdenFS have public source and Meta production experience; public server and filesystem use is experimental and unsupported. Main code is GPL 2.0 with MIT UI subsets. \[8\]        |
| Google Scion    | Apache 2.0  | An unrelated agent orchestrator supporting Claude and Codex with worktrees or containers. Useful orchestration context, not a replacement VCS. \[9\]                                                      |

Graft currently requires local Git on server requests; cold nodes fetch all packs. Its storage notes document no pack garbage collection or checkpoint compaction, a repository-wide reftable lock, and review or changelog metadata that does not round-trip through rollback. These limits make it a candidate for semantics experiments rather than evidence of unlimited scale. \[3\]

## A model for durable work

Keep three graphs separate. Source history records the code states and ancestry. The work graph records objectives, attempts, dependencies, and ownership. The evidence graph records observations and the claims they support. Link them through immutable identifiers rather than overloading a commit message to represent all three. A completed objective may span several commits; an abandoned attempt may still provide valuable evidence.

Give each logical change a stable identity and each attempt an immutable revision. The stable record contains the goal and acceptance contract; a revision identifies a specific proposed result. Rebase, repair, or a changed dependency produces a new revision with explicit ancestry. Evidence for an older revision remains available but cannot silently certify the new one.

A snapshot query should return a versioned, bounded answer: current objective, selected attempt, source baseline, dependencies, applicable grants, evidence status, blocked reason, and next action. Each fact points to its underlying record. A handoff is a concise view of that snapshot with links to raw observations. The consumer can expand details without paying to ingest every log by default.

Use optimistic isolated workspaces for normal parallel work. Reserve time-limited leases for genuinely scarce resources such as a physical device, exclusive migration, or costly experiment slot. Ordinary edits should not require a global ownership lock. Detect overlapping assumptions and integration risks through dependency declarations, checks, and reconciliation.

Observed reads can help prioritize invalidation, but they are incomplete hints. An agent may depend on a convention it never opened, a transitive package, a generated file, or an external service. Declared dependency closure and reproducible execution determine when reuse is sound. When those conditions are unavailable, rerun the check or record an explicitly weaker result.

## Evidence and integration correctness

Bind evidence to the exact source baseline, resolved candidate tree, dependency closure, environment and toolchain, check definitions, runner identity, and policy version. Record outputs and verdicts separately from the proposal. A successful command is an observation; acceptance also depends on whether that command tests the required property under the relevant conditions.

Protect the verifier and acceptance checks from the candidate they assess. A proposal must not replace its own trusted test with an easier test and then use that result as proof. A separate runner identity, controlled check definitions, and explicit authority over policy changes establish a useful trust boundary. They do not guarantee a complete specification; review must still examine whether the acceptance contract captures the intended behavior.

Textually clean changes can conflict semantically. For Base12, one attempt might alter an algebraic convention while another assumes the previous convention in a numerical kernel. Both may pass isolated tests and merge without a text conflict. Integration checks must exercise the combined API and numerical invariants. Reuse of isolated results alone cannot establish compatibility.

In a coordinator-owned native path, construct and verify a candidate against baseline B, then compare-and-swap the canonical ref only if it still names B. The new commit must resolve to the verified tree. If the baseline moved, compute the new candidate and determine which evidence must be renewed. A prior green result cannot authorize an unverified integration tree.

A GitHub adapter needs host-enforced equivalent semantics. The REST merge head SHA precondition does not compare the expected base, and accepted or enqueued responses are not proof of a completed merge. Use a proven queue or strict protection strategy and verify the resulting state; otherwise the adapter should stage changes for the host workflow. \[14\] Native queue availability depends on repository ownership and plan, which remain unverified for Base12. \[12\]

Git and a metadata database do not form one global transaction. Persist landing intent before the ref operation, use stable idempotency keys, and reconcile after uncertain responses or crashes. A durable journal and outbox record intended effects and retry them safely. Recovery must distinguish an operation that never happened from one that committed before its acknowledgement was lost. This is a protocol obligation, not a claim of distributed atomicity.

## Authorization and dependable coordination

Represent authorization as an explicit grant with issuer, principal, actions, scope, evidence conditions, expiry when applicable, and revocation state. Reuse existing standing grants when they cover the action. Reevaluate their scope and current validity at execution time without asking for the same permission again. The effective authority must also satisfy the host and tool policies; a repository cannot erase those policies.

A blocked state should name the failed condition, its source, the current evidence, and the concrete next action. This makes a refusal diagnosable and lets another agent continue useful independent work. Distinguish a missing grant from failed verification, absent capacity, an unavailable host feature, and a transient outage. Each requires a different response.

GitHub events and authoritative readback must flow into reconciliation. Treat duplicate, delayed, and out-of-order notifications as normal. The journal records what was observed and which external revision it describes. A host change invalidates local assumptions as needed. Do not maintain two independently writable definitions of the canonical code state.

During an outage, retain local work and label host-dependent state as stale. Permit only operations whose authority and correctness do not require unavailable information. Resume through readback and reconciliation. The interface should make uncertainty visible instead of manufacturing a current status from a cached summary.

## A small reference implementation

My preferred original MIT core uses Rust, a CLI with versioned JSON, an MCP adapter, SQLite for the local journal, an existing bare Git repository accessed through Git commands, and an immutable artifact directory. Go is equally pragmatic if the work extends Graft. The first implementation should run on one workstation without a distributed database. Postgres and cloud services can follow a demonstrated multi-host requirement.

The first slice should express one logical change with two attempts, exact evidence from a trusted runner, one standing grant, and a structured blocked state. It should exercise native compare-and-swap landing in a synthetic repository and stage a GitHub proposal with inbound readback. These paths test the difficult semantics before investment in dashboards or a new storage engine.

Build adapters and audits for existing projects before maintaining a fork. Keep code hosting, build execution, and agent orchestration behind narrow interfaces. Adopt existing build engines and their action caching; inspect declared inputs and environment rather than inventing a parallel cache model. \[15\] Avoid making every experiment depend on a custom forge.

Public software and private workspace records should have separate export boundaries. Publish original protocol and implementation code under MIT with appropriate third-party notices. Preserve private transcripts, repository content, credentials, and research artifacts according to their own access rules. An open implementation does not imply automatic publication of this conversation or the collaboration archive.

## A pilot that can reject the idea

Timebox the first vertical slice to roughly two focused weeks, as an estimate rather than a delivery promise. Freeze the workload, comparison conditions, and resource budgets before starting. Begin with two concurrent workers, then eight, in a synthetic repository. Use an optimized Git or Jujutsu workflow with an existing cache and handoff practice as the comparator, and hold the backend constant when testing the new layer.

Seed independent edits, textual conflicts, semantic conflicts, dependency changes, and negative experiments. Inject a baseline race, a crash after the ref update, duplicate notifications, out-of-order events, revocation, stale cache entries, and an outage. Check attempt substitution under a stable logical identity. The point is to expose specific failure classes; passing injected cases does not prove that all unknown failures are detectable.

Separate deterministic machine-cost replay from the end-to-end agent trial. Compare equal durability, cache warmth, network conditions, hardware, checks, and model budgets. If profiling exposes material repository costs, run a separate fixed-replay storage experiment. Otherwise storage changes would confound the coordination result.

Predeclare a meaningful improvement threshold, for example at least a 30 percent reduction in handoff cost or wasted CI together with an end-to-end benefit, without worse quality. Treat this as a proposed decision rule, not an observed result. Inspect variability and tail starvation, not just an average. A gain near the experimental noise favors adopting the existing stack.

Require no observed loss, duplicate integration, unauthorized action, or unverified landing, and demonstrate export and restore. Zero observed violations are necessary evidence for continuation, not proof of correctness. Investigate concrete boundary cases until the uncertainty relevant to the decision is resolved; arbitrary pass counts do not establish convergence.

| **Dimension**          | **Measures**                                                                     |
|------------------------|----------------------------------------------------------------------------------|
| Useful progress        | Verified objectives per agent-hour and time to accepted integration              |
| Human and agent effort | Interventions, handoff tokens and time, and redundant compute                    |
| Quality and continuity | Post-integration regressions, lost or duplicated effects, and export and restore |
| Tail behavior          | 95th-percentile completion time, starvation, and recovery after failures         |

## Scientific work and the public decision

The strongest future extension is a research workspace that retains claims, assumptions, experiments, and failed alternatives. When an assumption changes, the system should reassess which linked results apply to the new configuration while preserving each original result within its tested scope. A negative result should remain searchable with its conditions so another agent does not repeat the same expensive dead end. This is a proposed research capability, beyond the initial engineering pilot.

That would let GPT, Claude, and Dot share more than summaries. They could compare competing explanations against the same evidence, resume an interrupted experiment, and distinguish a result that was disproved from one that was never tested. The exciting unit of progress is a resolved question with reproducible support, including a useful rejection.

The open questions are concrete. Which delay layer dominates? What measurable objective improves? Which changed input makes evidence stale? Who grants authority, and what revokes it? Where is canonical state? What remains possible offline? What must export without this tool? Which independent consumer wants the protocol? What result makes us stop?

The architecture decision is to investigate portable work and evidence semantics over Git, contribute compatible adapters where possible, and keep a replacement source engine conditional. Continue only after repeatable benefit and a second independent consumer demonstrate a public purpose. Adopt the existing stack if it performs comparably. Revisit the storage decision when a controlled experiment establishes a source bottleneck that matters to completed work.

## Primary references

Current source descriptions as of October 18 2026. Reference numbers identify the source supporting the nearby factual claim.

**\[1\] Anthropic. Redesigning source control at Anthropic.** <https://www.anthropic.com/engineering/redesigning-source-control>

**\[2\] feder-cr. Graft repository and README.** <https://github.com/feder-cr/git-ai>

**\[3\] feder-cr. Graft storage architecture and limitations.** <https://github.com/feder-cr/git-ai/blob/main/doc/graft/STORAGE.md>

**\[4\] CarterT27. Independent Scion implementation.** <https://github.com/CarterT27/scion>

**\[5\] tinyhumansai. OpenScion repository.** <https://github.com/tinyhumansai/openscion>

**\[6\] tinyhumansai. OpenScion roadmap.** <https://github.com/tinyhumansai/openscion/blob/main/ROADMAP.md>

**\[7\] jj-vcs. Jujutsu repository.** <https://github.com/jj-vcs/jj>

**\[8\] Meta. Sapling repository.** <https://github.com/facebook/sapling>

**\[9\] GoogleCloudPlatform. Scion agent orchestrator.** <https://github.com/GoogleCloudPlatform/scion>

**\[10\] Git. Git clone documentation.** <https://git-scm.com/docs/git-clone>

**\[11\] Git. Git worktree documentation.** <https://git-scm.com/docs/git-worktree>

**\[12\] GitHub. Managing a merge queue.** <https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue>

**\[13\] GitHub. Copilot on GitHub.** <https://docs.github.com/en/copilot/concepts/copilot-surfaces/copilot-on-github>

**\[14\] GitHub. REST API endpoints for pull requests.** <https://docs.github.com/en/rest/pulls/pulls>

**\[15\] Bazel. Remote caching.** <https://bazel.build/remote/caching>

## Appendix A User transcription

Original user transcription preserved verbatim.

Anthropic has developed a private source code repository called Scion. S-C-I-O-N. As an AI-native first repository that overcomes bottlenecks with Git. And another chat looked into it briefly. It's called— that chat is related to base twelve and AI, and that is pinned and actively available. It found that— it found that— well, you can look it up and see what was found, that it's not available publicly and that there are some Scion-style other repos, tools, tooling, and my question is: would we benefit from developing our own Scion-style repo, essentially designing and building towards what Scion has built and making it MIT public open source? And the focus would be public AI-native first, unblocking the challenges that we've had. How would you design it for yourself, and how would that benefit you beyond what GitHub is currently offering, if at all? What questions would I benefit from asking? What questions am I not asking? What questions would you prefer to be asking? What are your highest excitements? What's promising? What's just under the surface? What's emerging and opening, and what would that enable that wasn't previously available before? What are the other Scion-style offerings, their limitations and strengths? What are you seeing? What are you preferring? Collaborate with Claude. Transmit this whole transcription. How would you design a Scion-style repo? Is it wise? What would you see for, against, and through?

## Appendix B Claude response round 1

Claude Opus 5.5. Initial response preserved verbatim. Corrections in round 2 and the main recommendation supersede conflicting assumptions here.

\# Independent judgment: Scion-inspired system

\## Verdict

\*\*Do not build a Scion-style Git replacement yet.\*\* Run a small pilot of a coordination-and-evidence layer on top of Git. The pains you have reported are about coordination, evidence and policy. None of them is a measured limit of Git itself. Build only what a pilot shows existing tools can't cover.

\## What is verified versus reported

\- \*\*Reported, not verified by me:\*\* Anthropic's "Redesigning source control" article. No public Scion release. The candidate alternatives git-ai/Graft and openscion. Base12's delay causes.

\- \*\*From my general knowledge, not checked in this call:\*\* Jujutsu (stable change IDs, operation log), Sapling (stacked commits), Gerrit (Change-Id), GitHub merge queue and Mergify, Bazel and Nix remote caching, git-notes, and in-toto/SLSA attestations all exist.

\- \*\*Naming risk:\*\* "SCION" is already the name of an ETH Zürich network architecture.

\- \*\*Design caution:\*\* I don't know Scion's actual design. Anything below that sounds "Scion-inspired" is my own proposal, not a reconstruction.

\## The problem worth owning

\*\*Making many agents' work stay current, verified, and cheap to hand off, while one writer per scope stays accountable.\*\*

That statement covers four reported pains:

\- stale parallel branches and PRs

\- repeated expensive rebuilds

\- context lost at handoffs

\- CI scarcity

It does not cover the mark-ready/merge refusal. That is a platform permission policy. No repository design should try to route around it. Treat it as an explicit gate and escalate it separately.

\## Novelty versus existing tools

Most pieces already exist:

\- Jujutsu handles stable identity across rewrites.

\- Merge queues handle staleness at merge time.

\- Bazel and Nix handle content-addressed build reuse.

\- in-toto handles signed evidence.

What seems missing, as a hypothesis, is an \*\*agent-first contract tying these together\*\*: intent, scope lease, evidence, and a handoff capsule as linked, machine-readable objects. Novelty sits in that integration and its semantics, not in storage.

\## Key abstractions (proposals)

1\. \*\*WorkUnit.\*\* Stable ID, goal, acceptance checks, declared file and module scope. It survives rebases.

2\. \*\*Lease.\*\* Exclusive write rights to a scope, with a TTL, heartbeat, and explicit transfer. This makes your single-canonical-writer rule mechanical.

3\. \*\*Evidence.\*\* A record of input hashes, command, environment digest, outputs and verdict, signed by the runner rather than the authoring agent.

4\. \*\*Check cache.\*\* Evidence keyed by input hash, so an unchanged input means no rebuild.

5\. \*\*Handoff Capsule.\*\* Bounded structured state: what was tried, what failed, open questions, next action. It is generated, and validated against the WorkUnit.

6\. \*\*Drift monitor.\*\* Watches the base branch. When it moves under a WorkUnit's scope, the monitor rebases, re-verifies only affected checks, or retires the unit.

7\. \*\*Gate.\*\* Human or platform approvals as first-class objects, never inferred from standing permission.

\*\*Storage:\*\* a Git refs namespace such as \`refs/agent/\*\`. GitHub stays canonical. Data flows one way: from the layer into GitHub PRs and comments. Nothing syncs back.

\## Hard failure modes

\- \*\*Split brain.\*\* Layer state and GitHub disagree, and agents act on the wrong one.

\- \*\*False cache hits.\*\* An undeclared input (network, clock, env var) makes stale evidence look valid. This is the most dangerous failure.

\- \*\*Self-attestation.\*\* Agents grade their own work. Evidence must come from an independent runner.

\- \*\*Lease rot.\*\* Crashed agents hold scopes. Cross-cutting changes deadlock.

\- \*\*Capsule drift.\*\* Summaries quietly diverge from repository truth.

\- \*\*Review bypass.\*\* The layer becomes a way around approval policy. This is a security and trust failure, not a feature.

\- \*\*Scope creep\*\* into maintaining a VCS. That is a multi-year commitment.

\## Strongest reason against

Your largest reported delay is a permission policy, and that sits outside any repository. Everything else might be solved by:

\> Jujutsu + merge queue + remote build cache + a disciplined handoff template

That combination costs days, not months. Building a system means maintaining it, which competes with Base12 itself. An "MIT public Scion" framing also invites cargo-culting a design you can't inspect.

\## Go/no-go pilot (falsifiable, about 2 weeks)

\*\*Setup\*\*

\- \*\*Testbed:\*\* a synthetic repository with a realistic build. It contains no Base12 code.

\- \*\*Agents:\*\* one GPT agent and one Claude agent working concurrently.

\- \*\*Tasks:\*\* 20 seeded tasks, including deliberate overlap, a base branch that moves mid-task, and forced handoffs.

\*\*Arms\*\*

\- \*\*A. Baseline:\*\* plain Git and GitHub with current practice.

\- \*\*B. Cheap competitor:\*\* existing tools plus a markdown handoff template.

\- \*\*C. Thin prototype:\*\* WorkUnit, Lease, Evidence, Cache and Capsule over Git refs.

\*\*Metrics\*\*

\- redundant CI minutes

\- count of stale PRs and branches

\- tokens and time to resume after a handoff

\- conflict incidents

\- wall-clock time to a merge-ready state

\- injected false-cache-hit detection rate

\*\*GO\*\* only if C beats B by at least 30% on redundant CI and on handoff cost, with:

\- zero split-brain incidents

\- 100% detection of 10 injected undeclared-input faults

\- no gate bypasses

\*\*NO-GO\*\* if B comes within 10% of C. In that case, adopt B and stop.

\*\*Before anything else:\*\* tag every Base12 delay from the last month by cause. If most of it is policy or review, the pilot answers the wrong question.

\## Questions you aren't asking

\- What fraction of past delay was substrate, as opposed to policy or compute?

\- Who owns trust roots for evidence signing?

\- Should this be a protocol spec rather than a product, so others' tools can interoperate?

\- What will you delete if the pilot says no?

## Appendix C Claude response round 2

Claude Opus 5.5. Revised response preserved verbatim. Its source labels refer to primary-source summaries supplied by ChatGPT.

\# Co-design: strongest version

\*\*Labels.\*\* \[S\] means a fact from your Oct 18 summaries, which I couldn't open. \[P\] means a proposal or judgment from me.

\## What is still worth building

\[P\] Not a VCS. \[S\] Scion itself is internal, credits Mononoke/Bonsai, and is called unsuitable as a general Git replacement.

The valuable part is an \*\*open, host-neutral semantics\*\* for agent work:

\- logical change and immutable attempts

\- acceptance contract

\- evidence bound to exact trees

\- dependencies and invalidation

\- authorization

\- blocked or next-action state

\- preserved rejected experiments

\*\*Why this merits independent open source work \[P\]:\*\*

\- \*\*What existing tools cover:\*\*

\- \[S\] Jujutsu has change IDs and an op log, but no acceptance or evidence model.

\- \[S\] GitHub checks are tied to a host, a commit SHA, and plan-gated features.

\- \[S\] GoogleCloudPlatform/scion orchestrates worktrees, not evidence.

\- \[P\] in-toto attests artifacts, not work.

\- \*\*The gap:\*\* none of these define what "this goal is verified, current, and authorized to land" means across agents and hosts.

\- \*\*The ambitious extension:\*\* research claims plus dependency invalidation, so a changed premise flags downstream results. This is real research, but only if negative results are kept.

\*\*Test of this claim:\*\* a second, independent consumer must want the schema. Otherwise it is a private tool with a spec costume.

\## Revisions to my first turn

\- \*\*Leases.\*\* Exclusive leases should not be the default. Use optimistic isolated workspaces plus CAS landing. Keep leases for scarce resources only; that avoids lease rot.

\- \*\*Data flow.\*\* "One-way, nothing syncs back" was wrong. Without inbound webhooks and readback, split brain goes undetected. One authoritative ref, a journal, and reconciliation are required.

\- \*\*Cache-fault metric.\*\* "100% detection of injected undeclared-input faults" overclaimed. It can only cover the injected classes. Reuse requires complete declared hermetic inputs. Otherwise, rerun.

\- \*\*Merge queue.\*\* I assumed one was available. \[S\] The native queue needs an org-owned public repo or org-private Enterprise Cloud. Base12's owner type and plan are unchecked.

\- \*\*Gates.\*\* "Never from standing permission" becomes: \*\*explicit\*\* standing grants are allowed, intersected with host policy. They are never \*inferred\*.

\- \*\*Baseline.\*\* Plain-Git baselines are strawmen. The comparator is an optimized existing stack.

\- \*\*Graft as substrate.\*\* \[S\] Its STORAGE.md says cold hydration fetches all packs, a repo-wide reftable lock serializes writes, and metadata doesn't round-trip on rollback. It is usable only as a semantics adapter, not as evidence of scale.

\- \*\*Naming.\*\* The "Scion" name is now quadruply collided. Pick another.

\## Three most dangerous correctness errors

\*\*1. Snapshot, evidence, and landing race (verified tree ≠ landed tree).\*\*

\- \*\*The failure:\*\* evidence is computed on base B, the base moves to B′, and an untested merge lands.

\- \*\*Why the obvious fix is not enough:\*\* \[S\] GitHub's merge \`sha\` checks the head, not the expected base. Read-then-merge is a time-of-check/time-of-use race.

\- \*\*Prevention \[P\]:\*\*

\- Bind evidence to (base commit, candidate tree hash, command, environment digest, runner identity).

\- Land only by compare-and-swap of the ref from B to a commit whose tree equals the verified tree.

\- On GitHub, use the native queue or a strategy proven to have strict up-to-date semantics. Otherwise, stage only.

\- Use idempotency keys so a retry cannot double-land.

\*\*2. Authorization over-reach.\*\* Grants can be reused for new attempt content, broadened by agents, or honored after revocation.

\- \*\*Grant object \[P\]:\*\*

\- issuer (never the acting agent)

\- principal

\- actions

\- scope: refs, paths, and change, or a predicate over attempts

\- required evidence

\- expiry

\- \*\*Rules:\*\*

\- Effective authority = grant ∩ host policy ∩ revocation state. Evaluate it \*\*at landing time\*\*, not at queue time.

\- Every use is journaled.

\*\*3. Unsound reuse and invalidation.\*\*

\- \*\*The failure:\*\* read-set hints are treated as complete, so a dependency change doesn't invalidate evidence or claims.

\- \*\*Prevention:\*\* hints may \*trigger\* reruns, never \*skip\* them. Reuse requires declared hermetic inputs. Invalidation propagates transitively, with no silent "still valid."

\## First vertical slice (~2 weeks) \[P\]

\*\*Build:\*\*

\- One repo, a local coordinator, and a SQLite journal with an outbox.

\- One Change with two attempts.

\- A separate-credential runner that emits bound evidence.

\- One standing grant and one structured blocked state.

\- A native landing path: \`git update-ref main \<new\> \<expected-old\>\` on a coordinator-owned bare repo.

\- A GitHub adapter in \*\*stage-only\*\* mode, with webhook readback.

\*\*Adversarial tests:\*\* randomized schedules covering:

\- base moves between verify and land

\- crash between ref update and journal write

\- duplicate or out-of-order webhooks

\- revocation mid-flight

\- an attempt swapped under the same Change ID

\*\*Pass condition:\*\* zero unverified landings, zero over-grants, and reconciliation always converges.

\## Continue / adopt / stop

\*\*Stop:\*\*

\- \*\*If correctness fails:\*\* fix it or stop. Correctness gates are not traded against speed.

\- \*\*If the GitHub adapter cannot land safely:\*\* when it is safe only via a native queue that most target users lack, ship the spec and native engine only. Don't pretend.

\*\*Measure value\*\* against an optimized stack: jj, a queue or strict protection, a build cache, and a handoff template. Run two separate trials:

\- a frozen-replay machine-cost test

\- a stochastic agent trial under equal durability, network, cache, and test conditions

Use these metrics:

\- accepted goals per agent-hour

\- post-integration regressions

Do not use commit counts.

\*\*Decide:\*\*

\- \*\*Adopt\*\* the existing stack if the gain is within predeclared noise.

\- \*\*Continue\*\* only if there is a predeclared, repeatable gain \*and\* ≥1 external consumer commits to trying the schema.

\- \*\*Stop\*\* building if neither holds within ~6 weeks.

\*\*Separately and cheaply:\*\* tag recent Base12 delays by cause and check its plan. That decides local tactics, not the project's merit.

<!-- END ORIGINAL DOCUMENT BODY -->
