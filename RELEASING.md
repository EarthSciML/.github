# Releasing EarthSciML multi-language packages

Repositories that ship a Julia package alongside other bindings (EarthSciAST,
EarthSciASTDiff, EarthSciIntegrator, EarthSciIO) release through the reusable
workflows in `.github/workflows/release-*.yml` here. Each repository keeps
three small caller workflows:

| Caller (in the package repo) | Calls | Does |
| --- | --- | --- |
| `release-register.yml` — *Release 1 - Register Julia* | `release-analyze.yml`, the repo's own gates, `release-register.yml` | On a push to `main` that bumps the Julia version: checks the version sites agree, runs the gates, and asks JuliaRegistrator to register that commit with release notes. |
| `TagBot.yml` — *Release 2 - TagBot* | `release-tagbot.yml` | When General merges the registration, tags the registered commit `v<version>` and creates the GitHub release. |
| `release.yml` — *Release 3 - Publish* | `release-resolve.yml`, `release-publish.yml`, `release-report.yml`, plus its own PyPI job | On the tag push: checks the tag is the tree General registered, publishes to PyPI, crates.io, npm and the Go proxy, attaches command-line binaries, and opens an issue if anything failed. |

Every registry publishes from the one commit General accepted. General can
refuse a registration, and the other registries never let a version be
reused, so nothing else ships until General has said yes. (EarthSciAST v0.3.0
reached npm, PyPI, crates.io and Go while its General PR sat refused.)

## Cutting a release

1. Bump the version in every manifest in one reviewed commit. The Julia
   `Project.toml` is the source of truth; the caller's `version-files` (and
   `version-check`, if set) must all agree with it or the run fails. If a
   Rust crate's `Cargo.lock` is tracked, bump the crate's own entry too
   (`cargo metadata --format-version 1 >/dev/null`), or `cargo publish` will
   refuse the tree its build dirtied.
2. For a breaking release (any 0.x minor bump), optionally write
   `release-notes/v<version>.md`; it goes first in the release notes. The
   generated notes always carry the "Breaking changes" and "Changelog"
   headings General's AutoMerge looks for.
3. Merge to `main`. The gates run, then Registrator replies on the commit
   with a link to the General PR.
4. **AutoMerge passes:** nothing to do. TagBot tags, `release.yml` publishes.
   **AutoMerge refuses:** fix the cause on `main` (no version bump), then run
   *Release 1 - Register Julia* by hand. Registrator updates the open PR.
5. **`release.yml` fails partway:** it opens an issue. Fix the cause and run
   *Release 3 - Publish* by hand with the tag; finished steps are skipped.

## Why PyPI stays in each repository

PyPI's trusted publishing cannot match a reusable workflow. A `workflow_call`
run carries two claims — `job_workflow_ref` (the reusable file) and
`workflow_ref` (the caller) — and the OIDC exchange matches the first while
PEP 740 attestations match the second, so no publisher configuration
satisfies both. The ~30-line `publish-pypi` job therefore lives directly in
each repo's `release.yml`, which the tag push starts.

## Reusable workflow inputs

All take `julia-package` (name in General) and `julia-subdir` (directory of
its `Project.toml`, default `.`) where relevant.

- **`release-analyze.yml`** — `version-files` (whitespace-separated
  manifests: `*.toml` read from their first `version = "..."` line,
  `*.json` from `.version`), `version-check` (extra command). Outputs
  `needs_release`, `version`.
- **`release-register.yml`** — `version`, `release-notes-dir` (default
  `release-notes`). Calling job needs `permissions: contents: write`.
- **`release-tagbot.yml`** — `secrets: inherit` (for `TAGBOT_APP_PRIVATE_KEY`).
  Calling job should use
  `if: github.event_name == 'workflow_dispatch' || github.actor == 'JuliaTagBot'`.
- **`release-resolve.yml`** — `tag`, `version-files`, `version-check`.
  Outputs `tag`, `version`.
- **`release-publish.yml`** — `tag`, `version`, and any of:
  - `crates`: crate directories, in dependency order; `cargo-publish-args`
  - `npm-dir`
  - `go-module-dir` (tagged `<dir>/v<version>`)
  - `cli-name`, `cli-bins` (`<crate dir>:<binary>` pairs): built for Linux
    x64/ARM64 (glibc 2.17 floor), macOS x64/ARM64 and Windows x64, archived as
    `<cli-name>-<version>-<platform>`, and attached with checksums and an
    `update.sh` installer
  - `install-notes`: Markdown appended to the release notes

  Calling job needs `permissions: contents: write` and `secrets: inherit`.
- **`release-report.yml`** — `tag`, `results: ${{ toJSON(needs) }}`. Call it
  with `if: always() && needs.resolve.result == 'success'`; needs
  `permissions: issues: write`.

The gates a repository runs before registering are its own: call its CI
workflows from `release-register.yml` (they need a `workflow_call:` trigger,
and a `concurrency` group that includes `${{ github.workflow }}` so the
gate run and the push's own CI run do not cancel each other).

## One-time setup per repository

None of this can be done from CI.

- **JuliaRegistrator**: install the
  [GitHub App](https://github.com/JuliaRegistries/Registrator) on the repo.
  A new package (not a new version) waits 3 days in General's AutoMerge.
- **TagBot**: install the org's TagBot GitHub App on the repository (see
  below), and add the repository to the org variable `TAGBOT_APP_CLIENT_ID`'s
  and the org secret `TAGBOT_APP_PRIVATE_KEY`'s repository access lists if
  they are not set to all repositories. Issues must stay enabled: JuliaTagBot
  triggers TagBot by commenting on one.
- **PyPI**: add a trusted publisher at
  https://pypi.org/manage/account/publishing/ — owner `EarthSciML`, the
  repository, workflow `release.yml`, environment `pypi`.
- **crates.io / npm**: `CARGO_REGISTRY_TOKEN` and `NPM_TOKEN` are org-level
  secrets. Every crate dependency needs a `version` (a path-only dependency
  cannot be published). crates.io publishes are permanent.
- **Go**: nothing.

## The TagBot GitHub App (once per organization)

A tag created with `GITHUB_TOKEN` starts no workflow, so TagBot needs another
credential or `release.yml` never runs. A deploy key works but is unique to
one repository; one GitHub App serves them all, and `release-tagbot.yml` mints
a short-lived token from it scoped to the calling repository.

1. **Organization settings → Developer settings → GitHub Apps → New GitHub
   App.** Name it (e.g. `EarthSciML TagBot`), set any homepage URL, untick
   **Webhook → Active**, and give it these repository permissions:
   - Contents: Read and write (tags and releases)
   - Issues: Read and write (TagBot reads the trigger issue and reports failures)
   - Pull requests: Read-only (changelog)
   - Workflows: Read and write (lets it tag a commit that edits a workflow file)

   "Where can this GitHub App be installed?": **Only on this account**.
2. On the App's page, note the **Client ID**, then **Generate a private key**
   (downloads a `.pem`).
3. **Install App** → the organization → **Only select repositories** → the
   package repositories.
4. **Organization settings → Secrets and variables → Actions**:
   - Variables → `TAGBOT_APP_CLIENT_ID` = the Client ID.
   - Secrets → `TAGBOT_APP_PRIVATE_KEY` = the whole contents of the `.pem`.
     Then delete the file.

   Give both access to the package repositories (or all repositories).

A new repository then needs only step 3's installation and, if access is
limited, step 4's lists.
