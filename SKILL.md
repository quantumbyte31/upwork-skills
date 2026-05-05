# Upwork Skills

Automate Upwork job search, proposal submission, and profile management via a Chrome extension + local bridge server.

## Architecture

```
CLI (cli.py) ──WebSocket──> bridge_server.py (port 9337) ──WebSocket──> Chrome extension ──> Upwork DOM
```

## Setup

1. Install dependencies:
   ```bash
   cd ~/.copilot/skills/upwork-skills
   pip install websockets>=12.0
   ```

2. Start bridge server:
   ```bash
   cd ~/.copilot/skills/upwork-skills
   nohup python scripts/bridge_server.py --port 9337 >> /tmp/bridge_9337.log 2>&1 &
   ```

3. Load Chrome extension from `~/.copilot/skills/upwork-skills/extension/` (Developer mode → Load unpacked)

4. Open upwork.com in Chrome — the extension auto-connects.

## Sub-Skills

- **upwork-auth** — login status, session management
- **upwork-explore** — search jobs, get job detail
- **upwork-propose** — submit proposals with cover letter + bid
- **upwork-profile** — view and update freelancer profile
- **upwork-lead-apply** — end-to-end: take a lead from Excel → find matching job → submit proposal

## Available Commands

```bash
python scripts/cli.py check-login
python scripts/cli.py search-jobs --query "Claude AI agent" --limit 10
python scripts/cli.py get-job-detail --job-url "https://www.upwork.com/freelance-jobs/apply/..."
python scripts/cli.py submit-proposal --job-url "..." --cover-letter "..." --bid 500
python scripts/cli.py list-proposals
python scripts/cli.py my-profile
python scripts/cli.py delete-cookies
```

## Intent Routing

When user says:              → Use sub-skill:
"find jobs on Upwork"        → upwork-explore
"apply for this job"         → upwork-propose
"submit proposal"            → upwork-propose
"check my proposals"         → upwork-propose (list-proposals)
"update my profile"          → upwork-profile
"apply for all leads"        → upwork-lead-apply
"am I logged in"             → upwork-auth

## qvedaai Profile

**Title**: Agentic AI Developer & Automation Engineer  
**Stack**: Claude API, LangChain, LangGraph, n8n, Make.com, WhatsApp Business API  
**Rate**: $45–$85/hr  
**Location**: Pune, India  
**Email**: insight@qvedaai.com  
**Website**: qvedaai.com
