# Universal Codebase

Welcome to the Universal Codebase template! Follow these steps to get started with your new project.

## Getting Started

### 1. Clone the Repository or Use the Template

You have two options to start using this template:

- **Clone the Repository:**
  ```bash
  git clone https://github.com/your-username/universal-codebase.git
  cd universal-codebase
  ```

- **Use the Template:**
  Click the "Use this template" button on the GitHub repository page to create a new repository based on this template.

### 2. Set Up GitHub Actions Secret

To enable automated releases and other workflows, you need to set up a GitHub Actions secret:

1. **Generate a Personal Access Token (PAT):**
   - Go to your GitHub account settings.
   - Navigate to **Developer settings > Personal access tokens**.
   - Generate a new token with `repo` and `workflow` scopes.

2. **Add the Token as a Secret:**
   - Go to your new repository on GitHub.
   - Navigate to **Settings > Secrets and variables > Actions**.
   - Click **New repository secret**.
   - Name the secret `GH_TOKEN` and paste your personal access token.

### 3. Configure Repository Permissions

Ensure GitHub Actions has the necessary permissions to read and write to your repository:

1. **Repository Settings:**
   - Go to your repository on GitHub.
   - Navigate to **Settings > Actions > General**.
   - Under **Workflow permissions**, select **Read and write permissions**.

### 4. Set the Initial Version Tag

To set the initial version tag for your project:

1. **Create an Initial Tag:**
   ```bash
   git tag v0.1.0
   git push --tags
   ```
   
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
