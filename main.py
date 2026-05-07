from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import HTMLResponse

app = FastAPI(title="Stock Search")

# Sample data simulating what yfinance returns for Indian & US stocks.
# In production (outside this sandbox), replace fetch_stock() with yfinance calls.
MOCK_STOCKS = {
    "RELIANCE": {
        "symbol": "RELIANCE.NS", "name": "Reliance Industries Limited",
        "exchange": "NSE", "currency": "INR", "price": 2987.55, "change_pct": 1.23,
        "prev_close": 2950.80, "open": 2960.00, "day_high": 2998.00, "day_low": 2945.10,
        "week52_high": 3217.90, "week52_low": 2220.30, "volume": 8432100,
        "market_cap": 20230000000000, "pe_ratio": 26.4, "eps": 113.2,
        "dividend_yield": 0.0035, "sector": "Energy", "industry": "Oil & Gas Integrated",
    },
    "TCS": {
        "symbol": "TCS.NS", "name": "Tata Consultancy Services Limited",
        "exchange": "NSE", "currency": "INR", "price": 3812.40, "change_pct": -0.54,
        "prev_close": 3833.10, "open": 3825.00, "day_high": 3840.00, "day_low": 3798.50,
        "week52_high": 4592.25, "week52_low": 3311.00, "volume": 2340500,
        "market_cap": 13820000000000, "pe_ratio": 29.1, "eps": 131.1,
        "dividend_yield": 0.018, "sector": "Technology", "industry": "Information Technology Services",
    },
    "INFY": {
        "symbol": "INFY.NS", "name": "Infosys Limited",
        "exchange": "NSE", "currency": "INR", "price": 1564.75, "change_pct": 0.87,
        "prev_close": 1551.20, "open": 1555.00, "day_high": 1572.30, "day_low": 1548.00,
        "week52_high": 1953.90, "week52_low": 1358.35, "volume": 5671200,
        "market_cap": 6510000000000, "pe_ratio": 23.7, "eps": 66.0,
        "dividend_yield": 0.025, "sector": "Technology", "industry": "Information Technology Services",
    },
    "HDFCBANK": {
        "symbol": "HDFCBANK.NS", "name": "HDFC Bank Limited",
        "exchange": "NSE", "currency": "INR", "price": 1723.60, "change_pct": 0.42,
        "prev_close": 1716.40, "open": 1718.00, "day_high": 1730.00, "day_low": 1710.50,
        "week52_high": 1880.00, "week52_low": 1363.55, "volume": 9823400,
        "market_cap": 13110000000000, "pe_ratio": 19.2, "eps": 89.8,
        "dividend_yield": 0.012, "sector": "Financial Services", "industry": "Banks—Regional",
    },
    "WIPRO": {
        "symbol": "WIPRO.NS", "name": "Wipro Limited",
        "exchange": "NSE", "currency": "INR", "price": 462.30, "change_pct": -1.10,
        "prev_close": 467.45, "open": 465.00, "day_high": 468.80, "day_low": 459.00,
        "week52_high": 572.65, "week52_low": 381.40, "volume": 6120000,
        "market_cap": 2400000000000, "pe_ratio": 21.5, "eps": 21.5,
        "dividend_yield": 0.009, "sector": "Technology", "industry": "Information Technology Services",
    },
    "AAPL": {
        "symbol": "AAPL", "name": "Apple Inc.",
        "exchange": "NASDAQ", "currency": "USD", "price": 189.30, "change_pct": 0.65,
        "prev_close": 188.07, "open": 188.50, "day_high": 190.12, "day_low": 187.80,
        "week52_high": 199.62, "week52_low": 164.08, "volume": 52340000,
        "market_cap": 2920000000000, "pe_ratio": 30.1, "eps": 6.29,
        "dividend_yield": 0.0052, "sector": "Technology", "industry": "Consumer Electronics",
    },
}


def fetch_stock(symbol: str) -> dict:
    key = symbol.upper().replace(".NS", "").replace(".BO", "")
    if key not in MOCK_STOCKS:
        raise HTTPException(
            status_code=404,
            detail=f"'{symbol}' not found. Try: RELIANCE, TCS, INFY, HDFCBANK, WIPRO, AAPL"
        )
    return MOCK_STOCKS[key]


@app.get("/api/stock")
def search_stock(symbol: str = Query(..., description="Stock ticker, e.g. RELIANCE, TCS, INFY")):
    return fetch_stock(symbol)


@app.get("/", response_class=HTMLResponse)
def ui():
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Stock Search</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: 'Segoe UI', sans-serif; background: #0f172a; color: #e2e8f0; min-height: 100vh; display: flex; flex-direction: column; align-items: center; padding: 40px 16px; }
  h1 { font-size: 2rem; font-weight: 700; color: #38bdf8; margin-bottom: 8px; }
  p.sub { color: #94a3b8; margin-bottom: 8px; font-size: 0.95rem; }
  p.hint { color: #475569; margin-bottom: 28px; font-size: 0.82rem; }
  .search-bar { display: flex; gap: 10px; width: 100%; max-width: 520px; margin-bottom: 32px; }
  input { flex: 1; padding: 12px 16px; border-radius: 10px; border: 1px solid #334155; background: #1e293b; color: #e2e8f0; font-size: 1rem; outline: none; }
  input:focus { border-color: #38bdf8; }
  button { padding: 12px 24px; border-radius: 10px; background: #38bdf8; color: #0f172a; font-weight: 700; border: none; cursor: pointer; font-size: 1rem; }
  button:hover { background: #7dd3fc; }
  #card { width: 100%; max-width: 520px; background: #1e293b; border-radius: 16px; padding: 28px; display: none; }
  .header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px; }
  .name { font-size: 1.2rem; font-weight: 700; }
  .symbol { font-size: 0.8rem; color: #94a3b8; margin-top: 2px; }
  .price-block { text-align: right; }
  .price { font-size: 1.8rem; font-weight: 800; }
  .change.up { color: #4ade80; } .change.down { color: #f87171; }
  .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 20px; }
  .stat { background: #0f172a; border-radius: 10px; padding: 12px 16px; }
  .stat-label { font-size: 0.72rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px; }
  .stat-value { font-size: 1rem; font-weight: 600; }
  #error { color: #f87171; margin-top: 4px; margin-bottom: 8px; display: none; font-size: 0.9rem; max-width: 520px; }
  .badge { display: inline-block; font-size: 0.72rem; background: #334155; border-radius: 6px; padding: 2px 8px; margin-top: 4px; color: #94a3b8; }
  .mock-note { font-size: 0.72rem; color: #475569; margin-top: 20px; }
</style>
</head>
<body>
<h1>Stock Search</h1>
<p class="sub">Search NSE, BSE, or US stocks by ticker symbol</p>
<p class="hint">Demo tickers: RELIANCE · TCS · INFY · HDFCBANK · WIPRO · AAPL</p>
<div class="search-bar">
  <input id="sym" placeholder="e.g. RELIANCE, TCS, INFY" onkeydown="if(event.key==='Enter')search()">
  <button onclick="search()">Search</button>
</div>
<div id="error"></div>
<div id="card"></div>
<script>
function fmt(n, dec=2) { return n != null ? Number(n).toLocaleString('en-IN', {maximumFractionDigits: dec}) : '—'; }
function fmtCap(n, cur) {
  if (!n) return '—';
  const sym = cur === 'USD' ? '$' : '₹';
  if (n >= 1e12) return sym + (n/1e12).toFixed(2) + 'T';
  if (n >= 1e9)  return sym + (n/1e9).toFixed(2) + 'B';
  return sym + (n/1e6).toFixed(2) + 'M';
}
async function search() {
  const sym = document.getElementById('sym').value.trim();
  if (!sym) return;
  const err = document.getElementById('error');
  const card = document.getElementById('card');
  err.style.display = 'none'; card.style.display = 'none';
  try {
    const res = await fetch('/api/stock?symbol=' + encodeURIComponent(sym));
    if (!res.ok) { const d = await res.json(); throw new Error(d.detail); }
    const d = await res.json();
    const cur = d.currency === 'INR' ? '₹' : (d.currency === 'USD' ? '$' : d.currency + ' ');
    const chg = d.change_pct;
    const chgStr = chg != null ? (chg >= 0 ? '+' : '') + chg + '%' : '—';
    card.innerHTML = `
      <div class="header">
        <div>
          <div class="name">${d.name}</div>
          <div class="symbol">${d.symbol}</div>
          ${d.sector ? '<span class="badge">' + d.sector + '</span>' : ''}
        </div>
        <div class="price-block">
          <div class="price">${cur}${fmt(d.price)}</div>
          <div class="change ${chg >= 0 ? 'up' : 'down'}">${chgStr}</div>
        </div>
      </div>
      <div class="grid">
        <div class="stat"><div class="stat-label">Day High</div><div class="stat-value">${cur}${fmt(d.day_high)}</div></div>
        <div class="stat"><div class="stat-label">Day Low</div><div class="stat-value">${cur}${fmt(d.day_low)}</div></div>
        <div class="stat"><div class="stat-label">52W High</div><div class="stat-value">${cur}${fmt(d.week52_high)}</div></div>
        <div class="stat"><div class="stat-label">52W Low</div><div class="stat-value">${cur}${fmt(d.week52_low)}</div></div>
        <div class="stat"><div class="stat-label">P/E Ratio</div><div class="stat-value">${fmt(d.pe_ratio)}</div></div>
        <div class="stat"><div class="stat-label">EPS</div><div class="stat-value">${cur}${fmt(d.eps)}</div></div>
        <div class="stat"><div class="stat-label">Volume</div><div class="stat-value">${fmt(d.volume, 0)}</div></div>
        <div class="stat"><div class="stat-label">Market Cap</div><div class="stat-value">${fmtCap(d.market_cap, d.currency)}</div></div>
        <div class="stat"><div class="stat-label">Div Yield</div><div class="stat-value">${d.dividend_yield ? (d.dividend_yield*100).toFixed(2)+'%' : '—'}</div></div>
        <div class="stat"><div class="stat-label">Exchange</div><div class="stat-value">${d.exchange}</div></div>
      </div>
      <div class="mock-note">* Demo data — connect yfinance for live prices</div>`;
    card.style.display = 'block';
  } catch(e) { err.textContent = '⚠ ' + e.message; err.style.display = 'block'; }
}
</script>
</body>
</html>"""
