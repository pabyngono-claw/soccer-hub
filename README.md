# Soccer Prediction Hub - Cloudflare Pages Deployment

## Frontend (Cloudflare Pages)

Static HTML/CSS/JS files for the soccer prediction platform.

### Pages
- `index.html` — Global leaderboard with country filter
- `match.html` — Match detail page (preview, live score, predictions)
- `dashboard.html` — User dashboard (stats, history, upcoming matches)

---

## Configuration

**Never commit real API keys to source control!**

Replace all `YOUR_*` placeholders with actual values before deploying.

| Placeholder | Description | Where to Get |
|-------------|-------------|--------------|
| `YOUR_XANO_API_URL` | Xano API base URL | Xano Dashboard → API Groups → Base URL |
| `YOUR_XANO_API_KEY` | Xano API key (JWT) | Xano Dashboard → Settings → API Keys |
| `YOUR_MEMBERSTACK_PUBLIC_KEY` | Memberstack public key (pk_...) | Memberstack Dashboard → Setup → Public Key |
| `YOUR_AIRTABLE_API_KEY` | Airtable personal access token | Airtable → Account → Personal Access Tokens |
| `YOUR_AIRTABLE_BASE_ID` | Airtable base ID (app...) | Airtable URL: `https://airtable.com/appXXXXXXXXXXXXXX` |

---

## Deployment Options

### Option 1: Cloudflare Pages Environment Variables (Recommended)

1. In Cloudflare Pages dashboard → Settings → Environment Variables
2. Add each variable as **Secret** type:

```
XANO_API_URL = https://your-workspace.xano.io/api:your-group
XANO_API_KEY = eyJhbGciOiJIUzI1NiIs...
MEMBERSTACK_PUBLIC_KEY = pk_...
AIRTABLE_API_KEY = pat...
AIRTABLE_BASE_ID = app...
```

3. Update `index.html`, `match.html`, `dashboard.html` to read from `window.ENV` or use a build-time substitution.

### Option 2: Build-Time Substitution (GitHub Actions / Cloudflare Build)

Add a build step that replaces placeholders:

```yaml
# .github/workflows/deploy.yml
- name: Inject secrets
  run: |
    sed -i "s|YOUR_XANO_API_URL|${{ secrets.XANO_API_URL }}|g" *.html
    sed -i "s|YOUR_XANO_API_KEY|${{ secrets.XANO_API_KEY }}|g" *.html
    sed -i "s|YOUR_MEMBERSTACK_PUBLIC_KEY|${{ secrets.MEMBERSTACK_PUBLIC_KEY }}|g" *.html
    sed -i "s|YOUR_AIRTABLE_API_KEY|${{ secrets.AIRTABLE_API_KEY }}|g" *.html
    sed -i "s|YOUR_AIRTABLE_BASE_ID|${{ secrets.AIRTABLE_BASE_ID }}|g" *.html
```

### Option 3: Runtime Config (Simplest for Demo)

Create a `config.js` loaded before other scripts:

```html
<!-- In each HTML file, before other scripts -->
<script src="config.js"></script>
```

```js
// config.js - generated at deploy time or served from KV
window.ENV = {
  XANO_BASE: "https://your-workspace.xano.io/api:your-group",
  XANO_KEY: "eyJhbG...",
  MS_PUBLIC_KEY: "pk_...",
  AIRTABLE_BASE: "app...",
  AIRTABLE_TOKEN: "pat..."
};
```

Then in HTML: `const XANO_BASE = window.ENV.XANO_BASE;`

---

## Backend Services (Separate)

These run independently on your server/VPS:

| Service | Script | Schedule |
|---------|--------|----------|
| **SCOUT** | `scout.py` | Daily 6 AM UTC |
| **TRACKER** | `tracker.py` | Every 5 min |
| **JUDGE** | `judge.py` | Daily 2 AM UTC |
| **WRITER** | `writer.py` | Daily 6:30 AM UTC |
| **RANKER** | `ranker.py` | Daily 3 AM UTC |

### Required Environment Variables (Server)

```bash
export API_FOOTBALL_KEY="your-rapidapi-key"
export AIRTABLE_TOKEN="pat..."
export AIRTABLE_BASE="app..."
export XANO_KEY="eyJhbG..."
```

### Cron Setup (Linux)

```bash
# /etc/cron.d/soccer-prediction
0 6 * * * deploy python3 /opt/soccer/services/scout.py once
*/5 * * * * deploy python3 /opt/soccer/services/tracker.py once
0 2 * * * deploy python3 /opt/soccer/services/judge.py all
0 3 * * * deploy python3 /opt/soccer/services/ranker.py
0 6 * * * deploy python3 /opt/soccer/services/writer.py once
```

---

## Xano Function Updates (Manual)

### Leaderboard Global Function

Update the function powering `/leaderboard/global` to compute ranks server-side:

```sql
SELECT 
    id, email, username, country_code, points_total, 
    predictions_made, streak, is_premium,
    ROW_NUMBER() OVER (ORDER BY points_total DESC, streak DESC) AS rank_global
FROM users 
WHERE points_total IS NOT NULL
ORDER BY points_total DESC, streak DESC;
```

### Leaderboard Country Function

```sql
SELECT 
    id, email, username, country_code, points_total, 
    predictions_made, streak, is_premium,
    ROW_NUMBER() OVER (ORDER BY points_total DESC, streak DESC) AS rank_country
FROM users 
WHERE country_code = :country_code AND points_total IS NOT NULL
ORDER BY points_total DESC, streak DESC;
```

---

## Quick Start (Local Testing)

```bash
# 1. Copy config template
cp index.html index.local.html

# 2. Replace placeholders in index.local.html with real keys

# 3. Serve locally
npx serve soccer-hub

# 4. Open http://localhost:3000
```

---

## Security Notes

- ✅ No secrets in git history (use `git filter-repo` if accidentally committed)
- ✅ Use Cloudflare Pages environment variables for production
- ✅ Rotate API keys quarterly
- ✅ Restrict Xano API keys to specific IP ranges
- ✅ Airtable tokens: minimum required scopes only
- ✅ Memberstack: use separate dev/prod apps

---

## Support

- Frontend: Cloudflare Pages auto-deploys on push to `main`
- Backend: Run services on dedicated VPS with systemd
- Monitoring: Check logs at `/var/log/soccer/*.log`