# upwork-lead-apply

End-to-end workflow: takes a lead from the Excel tracker → finds the matching Upwork job → drafts a custom cover letter → submits the proposal → updates the Excel "Sent?" column.

## Full Workflow

```
1. Read Excel (qvedaai_leads.xlsx) — find rows where Sent? = "Not Sent" AND Channel = "Upwork"
2. For each lead:
   a. search-jobs with the prospect name or job title keywords
   b. get-job-detail on the matching result
   c. Draft cover letter using upwork-propose rules
   d. submit-proposal with cover letter + bid
   e. Update Excel: Sent? → "Sent", Date Sent → today
3. Report session summary
```

## Usage

```bash
# Step 1: Check login
python ~/.copilot/skills/upwork-skills/scripts/cli.py check-login

# Step 2: Search for a specific known posting
python ~/.copilot/skills/upwork-skills/scripts/cli.py get-job-detail \
  --job-url "https://www.upwork.com/freelance-jobs/apply/..."

# Step 3: Submit
python ~/.copilot/skills/upwork-skills/scripts/cli.py submit-proposal \
  --job-url "..." \
  --cover-letter "..." \
  --bid 500
```

## Priority Leads to Apply (from Excel, May 2026)

| Lead                              | Budget | Priority |
|-----------------------------------|--------|----------|
| AI Agentic Pipeline Dev (6x)      | $8,000 | 🔴 TODAY |
| AI License Verification Tool      | $5,000 | 🔴 TODAY |
| Claude AI Agent Developer         | TBD    | 🔴 TODAY |
| AI Automation Engineer — Claude   | TBD    | 🔴 TODAY |
| GTM Automation (Clay+Claude+SF)   | TBD    | 🟡 TODAY |
| Make.com + Claude API Developer   | TBD    | 🟡 TODAY |
| AI WhatsApp CRM Bot               | $675   | 🟢 TODAY |

## Rate for Proposal Updates to Excel

After submitting, update Excel:
```python
# Use openpyxl to set K column (Sent?) = "Sent", L column = today's date
```
