# upwork-auth

Manages Upwork login status and session cookies.

## Commands

- `check-login` — Verify the browser is logged into Upwork
- `delete-cookies` — Clear Upwork session (forces re-login)

## Usage

```bash
python ~/.copilot/skills/upwork-skills/scripts/cli.py check-login
```

## When to invoke

- Before any job search or proposal action
- If previous commands returned auth errors
- To verify extension is connected and working

## Troubleshooting

If `check-login` fails:
1. Ensure bridge server is running on port 9337: `lsof -i :9337`
2. Ensure Chrome extension is loaded and shows "Connected" in console
3. Open upwork.com manually in Chrome and log in
4. Re-run `check-login`
