# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

**bharat** (`bbm07/bharat`) is a browser-based Indian stock analysis tool. The project is intentionally minimal: no build system, no package manager, no framework. All application logic lives in a single self-contained HTML file.

## Project Structure

```
bharat/
├── stock-analyzer.html   # Main application — the entire app lives here
├── .mcp.json             # MCP server configuration (TradingView)
├── README.md             # Placeholder
└── CLAUDE.md             # This file
```

## Application: Indian Stock Fundamental Analyzer

`stock-analyzer.html` is a single-file, zero-dependency browser app for fundamental analysis of NSE/BSE-listed Indian equities.

### How it works

1. User enters an NSE symbol or company name (e.g. `RELIANCE`, `Infosys`)
2. `resolveSymbol()` tries `<INPUT>.NS` directly on Yahoo Finance; falls back to a search query to find the correct ticker
3. `fetchStockData()` pulls 11 Yahoo Finance modules in one `quoteSummary` call
4. `analyzeStock()` computes a 100-point quality score across 6 weighted categories
5. `renderResults()` builds the DOM and displays phase cards, score breakdown, strengths/risks

### Data source

- **Primary**: `https://query1.finance.yahoo.com/` (direct fetch)
- **CORS fallback**: `https://corsproxy.io/?url=<encoded>` — used automatically when direct fetch fails (e.g. browser CORS restrictions)

### 12-Phase Analysis System

| Phase | Focus | Max contribution |
|-------|-------|-----------------|
| 1 | Basic Eligibility (market cap, exchange) | — |
| 2 | Revenue Growth (3Y/5Y CAGR, QoQ) | Growth: 25 pts |
| 3 | PAT / Bottom Line | Growth: 25 pts |
| 4 | Margin Quality (EBITDA, operating, PAT, gross) | — |
| 5 | Balance Sheet (D/E, net debt, ICR, current ratio) | Balance Sheet: 20 pts |
| 6 | Cash Flow Quality (CFO, FCF, CFO/PAT) | Cash Flow: 20 pts |
| 7 | Capital Efficiency (ROCE, ROE, ROA) | Cap. Efficiency: 20 pts |
| 8 | Working Capital (current ratio, asset turnover) | — |
| 9 | Governance (promoter/institutional holding) | Governance: 10 pts |
| 10 | Valuation (PEG, P/E, EV/EBITDA, P/B) | Valuation: 5 pts |
| 11 | Composite Quality Score | — |
| 12 | Smart Money (DMA, 52W range, beta) | — |

### Scoring categories (total 100 pts)

- **Growth** — 25 pts: revenue/PAT CAGR (3Y, 5Y), quarterly YoY growth, PAT ≥ revenue growth, consistency
- **Balance Sheet** — 20 pts: D/E ratio, net cash status, interest coverage, current ratio
- **Cash Flow** — 20 pts: CFO positivity across years, CFO/PAT ratio, FCF positivity
- **Capital Efficiency** — 20 pts: ROCE, ROE, ROA
- **Governance** — 10 pts: promoter holding, institutional holding
- **Valuation** — 5 pts: PEG ratio, EV/EBITDA, PAT margin threshold

### Stock categories

The app classifies stocks into one of five buckets based on fundamentals:
- **ELITE COMPOUNDER** — low debt + high ROCE + strong growth + score ≥ 70
- **GROWTH STOCK** — default for high-growth businesses
- **VALUE PICK** — low P/E with decent growth
- **CYCLICAL** — thin EBITDA margins
- **TURNAROUND** — PAT growing much faster than revenue

### Key utility functions

- `v(obj, ...path)` — safe deep accessor; unwraps Yahoo Finance `{ raw: number }` objects
- `fmt(n)` — formats numbers in Indian notation (Cr, L Cr)
- `cagrPct(start, end, years)` — computes CAGR as a percentage
- `fetchJSON(url)` — tries direct fetch, then CORS proxy fallback

## MCP Integration

`.mcp.json` registers a local TradingView MCP server:

```json
{
  "mcpServers": {
    "tradingview": {
      "command": "node",
      "args": ["/root/tradingview-mcp/src/server.js"]
    }
  }
}
```

This server must be installed separately at `/root/tradingview-mcp/`. It provides TradingView chart/data tools accessible to Claude Code sessions.

## Development Workflow

There is no build step. To work on the app:

1. Open `stock-analyzer.html` directly in a browser (`file://` protocol)
2. Or serve it locally: `python3 -m http.server 8080` then open `http://localhost:8080/stock-analyzer.html`
3. Edit the file, reload the browser

All CSS, HTML, and JavaScript are in the single file — no separate assets or imports.

## Code Conventions

- **No framework, no dependencies** — keep it that way unless there is a compelling reason
- **Single-file architecture** — all changes go into `stock-analyzer.html`
- **Dark theme only** — the UI palette uses `#080c18` backgrounds, `#e2e8f0` text, and semantic colours (`#34d399` green, `#f87171` red, `#fbbf24` yellow, `#60a5fa` blue)
- **Indian number formatting** — always format monetary values with `fmt()` (Cr/L Cr), never raw large numbers
- **Null-safe data access** — always use `v()` when reading Yahoo Finance fields; they can be absent or wrapped in `{ raw, fmt }` objects
- **No comments** — the code is self-documenting through function and variable names; only add a comment when the reasoning is genuinely non-obvious

## Known Constraints

- **Yahoo Finance CORS**: Direct API calls may be blocked in some browser environments; `fetchJSON()` handles this by retrying via corsproxy.io
- **Data availability**: Some metrics (ICR, pledged shares, auditor notes) are not available from Yahoo Finance and are flagged as "N/A" or "Manual check needed"
- **Indian market only**: Symbol resolution assumes `.NS` (NSE) first, then `.BO` (BSE); non-Indian symbols may produce unreliable results
- **No backend**: All processing happens in the browser; there is no server, no database, no authentication

## Git Branching

- `master` — stable, merged code
- Feature work goes on `claude/<description>` branches and is merged via PR
