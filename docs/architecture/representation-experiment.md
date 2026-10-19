# Research experiment: is a context sufficient for the next decision?

Status: proposed experiment, not an implemented automatic detector.

Prime Radiant's available research kit treats state representation, observability, and information loss as research questions. Continuum can borrow that method without borrowing a physical theory: investigate whether a project representation preserves what a future decision actually needs.

## A discriminating pair of histories

Consider two histories with identical current source files:

- In history A, an operation was submitted to an external worker and its reply was lost.
- In history B, that operation was never submitted.

A source-only summary maps both histories to the same context. The next action should differ: history A needs reconciliation or an explicit unknown outcome, while history B can issue the first request under existing authority.

A repository that remembers only source state loses this distinction. A work graph retaining the operation identity and receipt state can preserve it.

The current Rust acceptance experiment is a local concrete witness: process death after commit but before acknowledgement leaves a recoverable receipt, so a fresh process can return the existing result.

## General test

Choose a declared class of future questions and authorized actions. Construct paired histories that look identical under a proposed context projection but require different correct responses within that class.

If such a pair exists, the projection is insufficient for that class. Add the smallest missing state, or explicitly mark the missing distinction unknown. Do not claim universal sufficiency; new questions may require new information.

Potential hidden distinctions include:

- Pending external effects.
- Expired authority or changed policy epochs.
- Different evidence applicability.
- Rejected alternatives whose original failure conditions have changed.
- A source-derived claim versus an untested model assertion.
- Correlated reviews versus independent observations.
- An operation that failed before dispatch versus an uncertain remote outcome.

## Evaluation design

Compare at least three context conditions: a source-only description, an ordinary narrative handoff, and an exact graph projection with typed state and expandable sources. Hold the task and budget comparable, preserve model/provider exposure, and evaluate against the actual decision contract.

Measure wrong action, duplicated work, missed uncertainty, time to correct orientation, and context size. Collect failure cases as preserved fixtures. Improvement is an empirical question.

This is the central research opening: context preparation can become a tested engineering function rather than an ever-longer summary prompt.

