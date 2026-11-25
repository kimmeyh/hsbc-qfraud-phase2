# Sprint Retrospective Guide

Adapted 2026-08-30 from spamfilter-multi's SPRINT_RETROSPECTIVE.md. The source's 14-category x 4-role structure and 7-step protocol are preserved in shape and EXTENDED to 16 categories (15 and 16 are team-lead additions from Sprint 2); examples are adapted to this project.

## Purpose (team lead, verbatim, 2026-10-23)

"The overall goals of the Retrospective is for the entire team (Coding
Agents and Non-Coding agents) to be long-term (many sprints) more effective
while as efficient as reasonably possible in the context of long-term
support of the repository and keeping in mind the Architecture, Software
Engineering, Security, DevOps, Six Sigma (heavily weighting improvement
that can prevent any current and future issues instead of responding to
them), Agile standards and best practices. To accomplish this we must base
what we do on facts supported by references, honesty, objectivity while
treating each other in a "tactfully honest way" (as opposed to "brutally
honest")."

This applies to every retrospective without being restated in the prompt.
The team lead does not need to paste it or the standing request below.

## Standing request (team lead, verbatim, 2026-10-23; applies every sprint)

"Please complete your sprint retrospective feedback (same sections)
Combined feedback (yours and mine) and Summarize
Make suggestions for improvements to be implemented. Ensure that all
improvement suggestions first attempt to prevent the problem from happening
first, then implement additional controls if absolutely necessary. Look for
ways of extending current method of preventions "connected" to the current
improvement when it makes more sense than creating a new method.
Display suggestions for improvement for review and approval."

How the 7-step protocol below carries it out:

- Steps 2-3: Claude completes its own feedback in all 16 categories.
- Step 4: the combined feedback is displayed AND summarized.
- Step 5: each proposal is prevention first (stop the problem from
  occurring); a detection or control is added only if prevention cannot
  be made sufficient, and the proposal says why. Before proposing a new
  guard, test, hook or document, check whether an existing prevention
  connected to the problem can be extended instead; prefer extending it
  when that makes more sense, and name it. Each proposal cites the fact
  it rests on (a finding, a commit, a file and line, a measurement).
- Steps 5-6: the proposals are displayed for review and approval; nothing
  is applied before the team lead disposes it.

## Rules

- Retrospectives are MANDATORY for every sprint, conducted after Phase 6 (PR updated, reviews on the draft PR complete, findings fixed) and BEFORE the PR is marked ready. The step 1 prompt goes out when the reviews start, so the team lead's feedback is collected while they run (team lead, 2026-10-23, Sprint 28 DV5).
- **The review findings are an input.** Step 5 groups them by class. Each RECURRING class (two or more findings this sprint, or seen in an earlier sprint) must produce an improvement: a card acceptance criterion, a Phase 5 gate, a test or a hook. A single finding gets its root cause recorded. After step 7, ONE short review of the improvement commits only; no second round (`SPRINT_EXECUTION_WORKFLOW.md` Phase 7).
- **A retrospective is NEVER complete unless ALL 16 categories are addressed by ALL 4 roles.** The team lead wears Product Owner, Scrum Master, and Lead Developer; Claude provides the Development Team perspective. A role with nothing to say writes `No issues -- expectations met.` explicitly; silence is not acceptable.
- Record the team lead's words VERBATIM; never paraphrase or substitute Claude's draft for them.

## The 7-Step Protocol (run in order; do not collapse, reorder, or skip)

1. **Send the prompt**: ask the team lead for PO/SM/LD feedback across all 16 categories (combined per-category lines acceptable), noting that Claude is drafting its own role's feedback in parallel.
2. **Draft in parallel**: Claude writes its Development Team feedback for all 16 categories into `docs/sprints/drafts/SPRINT_N_RETROSPECTIVE_claude_draft.md` while waiting.
3. **Record verbatim**: paste the template into `docs/sprints/SPRINT_N_RETROSPECTIVE.md`; the team lead's exact words per category; Claude's lines from the draft. Exit gate: 16 categories, 4 roles, no placeholders.
4. **Combine, display and summarize** in chat: both feedback sets together per category, then a short summary of the themes.
5. **Propose improvements** from the combined feedback and the review findings, in the format below (team lead, 2026-11-07, Sprint 31). It applies to every retrospective improvement, question and decision, a review finding not fixed included. The goal is long-term effectiveness at reasonable efficiency, aligned with this repository's architecture, its agile and software engineering practice, and its risk-based, automated testing. Display; do NOT auto-apply.
   - Number the items `i1` to `in`, each followed by a brief title. Never use `IMP-n`, and never reuse a number inside the sprint.
   - Each item has these fields, in this order:
     - **What it is:** the change, the file it changes and the rule it adds.
     - **Source:** where the item came from: the category and role, the review finding, the commit or the team lead's request (Sprint 34 i10).
     - **What it prevents and/or catches:** prevention is preferred, at the earliest stage that can hold it: the sprint process, the backlog item, the sprint card, development, then testing. Name the stage. Something that only catches says so, and says why prevention is not enough.
     - **Long-term value:** why it is still worth having after this sprint.
     - **Evidence:** the facts that suggest it has long-term value: how many times the problem occurred (and in which sprints), the time it wasted, and the efficiency it gains and how. A count that is not known is written "not measured", never estimated without saying so.
     - **Pros and cons:** of the proposal itself.
     - **Prevention or control,** **Extends** (the existing prevention it extends, or "new" and why) and **Effort**: for EACH option, the minutes and files to implement it AND its impact on test time (per task, per suite run, per gate run, as applies), each either measured (say from what) or marked as a best guess with its basis. "Not measured" is not accepted for effort or test impact (team lead, 2026-11-24, Sprint 34 i10, after the spamfilter-multi example).
     - **Options for implementing,** lettered `a` to `z`. Each states what is done, when (now, or the backlog with its card number and priority) and its effort, with one pro and one con. The recommended option is marked `(Recommendation)`. A usual order, where it fits:
       - a. the best option, now or backlog depending on its effort;
       - b. the best option, but backlogged for its time or the number of files it touches;
       - c. the next best alternative;
       - d. the next best after c;
       - e. skip for this sprint, but track it, in case it recurs;
       - f. skip.
   - The team lead answers in one line, "i1. a i2. c i3. b", or "all as recommended". This answer form replaces the digit rule for retrospective items only. Each option must be executable the moment its letter arrives: card numbers and priorities are named in it.
   - Write the items to the retrospective file before display. When an item is also a numbered decision (`SPRINT_n_DECISIONS.md`), the decision's "Changed since asked" note maps its options to the item's letters.
   - Checklist before display:
     - [ ] Every item has an `i` number, a title and every field above, in order.
     - [ ] "What it prevents" names the stage, and "Evidence" names counts and times, or says "not measured".
     - [ ] Every option names its timing, effort, card number and priority where it has one, a pro and a con. One option is marked `(Recommendation)`.
     - [ ] The Effort line gives every option's effort and test-time impact, each measured or marked as a best guess; none says "not measured".
     - [ ] The chat display shows every field. It does not show only titles.
6. **Team lead disposes each** with the `i1. a` answer form, or "all as recommended". Record the answer verbatim in an "Improvement Decisions" section.
7. **Apply**: now-items as commits on the sprint branch; backlog-items to ALL_SPRINTS_MASTER_PLAN.md; skips noted. Then the mandatory completion updates (master plan Last Completed Sprint, summary doc scheduling, CHECKLIST reconciliation, **one `docs/VELOCITY_LOG.md` row per task from `sprint_status.json` `task_actuals`** (IMP-7, Sprint 22)). THEN `gh pr ready`.

## The 16 Mandatory Categories

1. **Effective while as Efficient as Reasonably Possible** -- right outcome, least reasonable effort, workflow followed, rework counted.
2. **Testing Approach** -- did automated tests catch problems before validation; coverage adequate for the scope (for this project: known-answer statistical tests, leakage positive controls, loader validations).
3. **Effort Accuracy** -- estimates vs actuals per task; variance patterns.
4. **Planning Quality** -- task clarity, acceptance-criteria sufficiency, dependencies, scope fit.
5. **Model Assignments** -- were subagent/model choices right (reviews, research agents, main-loop work); escalations needed.
6. **Communication** -- narration, timely blocker reporting, commit/PR clarity.
7. **Requirements Clarity** -- ambiguity encountered; hidden requirements surfaced mid-sprint.
8. **Documentation** -- docs updated with the work; prereg amendments recorded properly; reference docs current.
9. **Process Issues** -- errors, blockers, tooling friction, anything that belongs in a troubleshooting note or hook. **The troubleshooting note now EXISTS: `docs/TROUBLESHOOTING.md`** (IMP-2, Sprint 20). A category-9 finding with an authoritative home gets an entry there -- one symptom line, one cause line, one pointer. This category asked for that document from Sprint 2 and nine retrospectives' findings had nowhere to go, so each was rediscovered by a later session.
10. **Risk Management** -- risks identified vs materialized (hardware budget, leakage, deadline, grant timing); mitigation effectiveness.
11. **Next Sprint Readiness** -- blockers for next sprint; master plan current.
12. **Architecture Maintenance** -- for this project: protocol integrity (does anything in code diverge from the frozen preregistration; are amendments logged), pipeline structure, results.json schema adherence.
13. **Minor Function Updates for the Next Sprint Plan** -- sub-hour items to fold inline into Sprint N+1. Format: `[ROLE] <one-line> -- target: Sprint N+1 plan, est: <Xm>`.
14. **Function Updates for the Future Backlog** -- larger items for ALL_SPRINTS_MASTER_PLAN.md "Next Sprint Candidates" with a new F#. Format: `[ROLE] <title> -- estimated: <X>, priority: <N>, depends on: <list>`.
15. **Assigned Coding Agents Quality** (team lead addition, Sprint 2) -- quality of delegated subagent/background-agent output: first-pass correctness, spec adherence, rework required.
16. **Questions to be discussed before ending the sprint** (team lead addition, Sprint 2) -- open items requiring discussion before close; `none` is an acceptable and explicit answer.

## Mandatory Feedback Template (copy verbatim into `docs/sprints/SPRINT_N_RETROSPECTIVE.md`)

```markdown
## Sprint N Retrospective Feedback

### 1. Effective while as Efficient as Reasonably Possible

- **Product Owner**: [feedback]
- **Scrum Master**: [feedback]
- **Lead Developer**: [feedback]
- **Claude Code Development Team**: [feedback]

### 2. Testing Approach
[same four-role block]

### 3. Effort Accuracy
[same four-role block]

### 4. Planning Quality
[same four-role block]

### 5. Model Assignments
[same four-role block]

### 6. Communication
[same four-role block]

### 7. Requirements Clarity
[same four-role block]

### 8. Documentation
[same four-role block]

### 9. Process Issues
[same four-role block]

### 10. Risk Management
[same four-role block]

### 11. Next Sprint Readiness
[same four-role block]

### 12. Architecture Maintenance
[same four-role block]

### 13. Minor Function Updates for the Next Sprint Plan
[same four-role block]

### 14. Function Updates for the Future Backlog
[same four-role block]

### 15. Assigned Coding Agents Quality
[same four-role block]

### 16. Questions to be discussed before ending the sprint
[same four-role block]

## Improvement Decisions

| # (i1-in) | Title | Alternative taken (a-z) | Effort | Decision (now/backlog/skip) |
|---|---|---|---|---|
```

## Transition note

Sprint 1 (2026-08-30) closed under the earlier lightweight three-question retro before this guide was adopted; its retrospective doc records that explicitly. The full protocol applies from Sprint 2 onward.
