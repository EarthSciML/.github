# Shared lint workflow

`.github/workflows/lint.yml` is the format and lint gate for EarthSciML's
multi-language repositories: EarthSciAST, EarthSciIntegrator, EarthSciASTDiff
and EarthSciIO. (The Julia-only packages keep their own FormatCheck setup.)

## What it runs

| Language   | Format gate                  | Lint gate                                               | Version                      |
| ---------- | ---------------------------- | ------------------------------------------------------- | ---------------------------- |
| Rust       | `cargo fmt --all -- --check` | `cargo clippy --workspace --all-targets <args> -- -D warnings`, one job per target/feature set | Rust 1.99.1 |
| Python     | `ruff format --check`        | `ruff check`; optional pyright or mypy job               | ruff 0.17.3                  |
| Julia      | Runic `--check`              | (Aqua / ExplicitImports belong in the package's tests)  | Runic 1.13                   |
| TypeScript | the repo's npm scripts (`format:check`) | the repo's npm scripts (`lint`, `typecheck`) | the repo's `package-lock.json` |
| Go         | `gofmt -l`                   | `golangci-lint run`                                     | golangci-lint v2.15.0        |
| Lean       | (none)                       | `lake build --wfail` (input `lean-build-args`), axiom audit, `lake lint` when the lakefile sets a lint driver | the repo's `lean-toolchain` |

## Principles

- **Versions are pinned here, rules live in the repository.** One PR to
  `lint.yml` moves every caller to a new tool version. Each repository keeps
  its rules in the tool's native file (`rustfmt.toml`, `[workspace.lints]`,
  `ruff.toml`, `eslint.config.js`, `.golangci.yml`, `lakefile.toml`), so a
  local run agrees with CI. `lint-templates/` has starter files.
- **Pin everything.** An unpinned linter applies new rules to unchanged code
  and turns `main` red with no commit behind it.
- **Lint is not a test step.** Each language is its own job, separate from the
  test jobs, so one finding never hides another or a test result. Test jobs
  keep their floating toolchains; only the lint job is pinned.
- **Warnings fail CI** (`-D warnings`, `--wfail`), without changing rule
  levels in the repository.

## Calling it

```yaml
# .github/workflows/lint.yml in the calling repository
name: Lint
on:
  pull_request:
  push:
    branches: [main]
  workflow_dispatch:
permissions:
  contents: read
concurrency:
  group: lint-${{ github.ref }}
  cancel-in-progress: true
jobs:
  lint:
    uses: EarthSciML/.github/.github/workflows/lint.yml@main
    with:
      rust-dirs: '["rust"]'
      rust-clippy: >-
        [{"dir": "rust", "args": "--features conformance,object-store"},
         {"dir": "rust", "target": "wasm32-unknown-unknown", "args": "--features opfs"}]
      python-dir: "."
      julia-paths: "."
```

Every input is documented in `lint.yml`. A language runs only when its input
is set.

## Bumping a tool version

1. Change the default in `lint.yml`.
2. The PR runs `lint-canary.yml`, which calls the new `lint.yml` against each
   caller's `main`. Fix any new findings in the callers first, or in the same
   change window.
3. Merge. Callers reference `@main`, so they pick it up on their next run.

## Adopting it in a repository

1. One formatting-only commit per formatter, listed in
   `.git-blame-ignore-revs` (the repositories use merge commits, so the SHA
   survives the merge).
2. A separate commit with the lint fixes.
3. Add the caller workflow and remove any lint steps it replaces.
4. Add the repository to `lint-canary.yml`.
