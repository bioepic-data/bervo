# Giving the agents their own identity

By default the Claude-powered workflows post as **`github-actions[bot]`**, the generic
identity every GitHub Action shares. That makes agent activity indistinguishable from any
other automation in the repository — CI, page builds, Dependabot.

To have them post as a named identity such as **`ai4c-agent`**, the workflows need a token
belonging to a GitHub App rather than the default `GITHUB_TOKEN`.

The workflows are already wired for this. Each one runs:

```yaml
- name: Generate agent app token
  id: agent-token
  continue-on-error: true
  uses: actions/create-github-app-token@v1
  with:
    app-id: ${{ secrets.AI4C_AGENT_APP_ID }}
    private-key: ${{ secrets.AI4C_AGENT_PRIVATE_KEY }}
```

and then passes `${{ steps.agent-token.outputs.token || github.token }}`. With the secrets
absent the step is a no-op and everything falls back to the default token, so there is
nothing to undo if you decide against it.

## Setup

This needs someone with admin rights on the `bioepic-data` organisation; it cannot be done
from a workflow.

1. **Create the App.** Organisation settings → Developer settings → GitHub Apps → *New
   GitHub App*. Name it whatever the agents should appear as — the name becomes the comment
   author, with `[bot]` appended. Set a homepage URL (this repository is fine) and
   **uncheck Webhook → Active**.

2. **Set repository permissions:**

   | Permission | Access | Needed for |
   | --- | --- | --- |
   | Contents | Read and write | Checking out, and committing when asked |
   | Issues | Read and write | Triage labels and comments |
   | Pull requests | Read and write | Posting reviews and comments |
   | Actions | Read | Reading CI results on a PR |

3. **Install it** on `bioepic-data/bervo` (App settings → Install App).

4. **Generate a private key** (App settings → Private keys → *Generate a private key*).
   A `.pem` file downloads.

5. **Add the secrets:**

   ```bash
   gh secret set AI4C_AGENT_APP_ID --repo bioepic-data/bervo        # the numeric App ID
   gh secret set AI4C_AGENT_PRIVATE_KEY --repo bioepic-data/bervo < path/to/key.pem
   ```

   Paste the `.pem` contents whole, including the `-----BEGIN…` and `-----END…` lines.

The next workflow run posts under the App's name. Nothing else changes — the App token is
scoped to this repository and expires after each run.

## What this does not change

`bot_id` and `bot_name` on `claude-code-action` control the **git author** on any commit the
agent makes, not the comment author. They default to `claude[bot]`. If you want commits
attributed to the App as well, set them to the App's bot user id and `<app-name>[bot]`; the
id is visible at `https://api.github.com/users/<app-name>%5Bbot%5D`.

## Related

`.github/ai-controllers.json` lists the accounts whose `@claude` mentions the workflows will
act on. It is unrelated to the posting identity.
