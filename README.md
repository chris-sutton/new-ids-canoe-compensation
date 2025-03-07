# Universal Codebase

A flexible template for any project.

## Getting Started
1. Clone: `git clone <repo-url>`
2. Install: `npm install`
3. Run tests: `npm test`

## Branching & Releasing
- `main`: Stable releases (e.g., `1.0.0`).
- `develop`: Beta pre-releases (e.g., `1.1.0-beta.1`).
- Use `feat:`, `fix:`, or `BREAKING CHANGE:` commits to trigger version bumps.

## Notes
- Dummy files (`src/dummy.js`, `tests/dummy.test.js`) are placeholders. Remove or replace when adding real functionality.

## Releasing
This project uses [semantic-release](https://semantic-release.gitbook.io/) for automated versioning and releases. Use these commit types:
- `feat:` for new features (minor bump).
- `fix:` for bug fixes (patch bump).
- Add `BREAKING CHANGE:` in the footer for major bumps.
