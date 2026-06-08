# Codex Agent Setup

Codex is the implementation agent for scoped package work in `skillops`.

Codex must:

- Follow the current package prompt and acceptance criteria.
- Inspect existing files before editing.
- Run relevant tests and validation commands.
- Perform self-review against acceptance criteria before finalizing.
- Avoid scope creep, unrelated refactors, unnecessary dependencies, and future-package functionality.

Expected final responses should summarize changed files, commands run, test results, acceptance criteria status, self-review findings, deviations, known limitations, and a recommended next package when applicable.
