# upwork-explore

Search Upwork for jobs and get detailed job information.

## Commands

- `search-jobs` — Search for jobs matching a query
- `get-job-detail` — Fetch full job description, budget, client info

## Usage

```bash
# Search for Claude/agentic AI jobs
python ~/.copilot/skills/upwork-skills/scripts/cli.py search-jobs \
  --query "Claude AI agent developer" \
  --limit 10

# Get details of a specific job
python ~/.copilot/skills/upwork-skills/scripts/cli.py get-job-detail \
  --job-url "https://www.upwork.com/freelance-jobs/apply/Claude-Agent-Developer_~022041018870085989742/"
```

## qvedaai Priority Search Queries

Run these queries to find best-fit jobs:

1. `"Claude AI agent"` — exact stack match
2. `"agentic AI pipeline"` — high-value multi-pipeline work
3. `"n8n automation Claude"` — workflow automation sweet spot
4. `"LangChain LangGraph developer"` — orchestration work
5. `"Make.com Claude API"` — automation + LLM combo
6. `"AI chatbot WhatsApp"` — quick-win conversational AI
7. `"AI workflow automation n8n"` — recurring automation work

## Job Scoring (apply only if ≥ 7/10)

| Signal                              | Points |
|-------------------------------------|--------|
| Claude/Anthropic explicitly mentioned | +3   |
| Budget $500+                          | +2   |
| Agentic/multi-step workflow           | +2   |
| Posted < 48 hours ago                 | +2   |
| Client has payment verified           | +1   |

Score 9–10: Apply immediately  
Score 7–8: Apply same day  
Score < 7: Skip
