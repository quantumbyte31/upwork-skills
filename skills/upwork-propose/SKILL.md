# upwork-propose

Submit proposals to Upwork jobs with customized cover letters and bids.

## Commands

- `submit-proposal` — Submit a proposal to a specific job URL
- `list-proposals` — List all active proposals

## Usage

```bash
python ~/.copilot/skills/upwork-skills/scripts/cli.py submit-proposal \
  --job-url "https://www.upwork.com/freelance-jobs/apply/Claude-Agent-Developer_~022041018870085989742/" \
  --cover-letter "..." \
  --bid 65
```

## Cover Letter Rules (STRICTLY ENFORCED — Anti-Generic-AI Detection)

- Max 80 words total
- Open with the client's specific pain, not "I am excited..."
- Mention the exact technology from the job post (Claude, n8n, etc.)
- One specific proof point (delivered X similar system, built X in Y days)
- End with a soft ask: "Can I send a quick breakdown of how I'd approach this?"
- NO em dashes (—), no bullet points, no sycophantic openers
- Contractions always: "don't", "I've", "we've"

## Cover Letter Template

```
[Client's core ask restated in 1 sentence]. We've built [X similar specific thing] using [exact tech from job post] — happy to share that as a reference.

For this project, [1-line specific approach]. Can scope and deliver in [realistic timeline]. Can I send a quick breakdown?

— insight@qvedaai.com | qvedaai.com
```

## Bid Strategy

| Job Budget  | Bid Rate  |
|-------------|-----------|
| Fixed $500- | $400–$500 |
| Fixed $1K+  | 80–90% of budget |
| Hourly      | $45–$65/hr |
| $5K+        | $4,500+ (don't undersell) |
