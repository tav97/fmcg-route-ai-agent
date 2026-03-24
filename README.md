# 🚛 FMCG Route AI Agent — Demo

Companion code and interactive demo for the article:
**"Building a Rule-Based AI Agent for FMCG Route Optimization"**

A deterministic, heuristic-based AI agent that schedules FMCG deliveries using a 5-step rule-based engine — no ML required.

## 🌐 Live Demo

**Live Demo at: 👉 https://tav97.github.io/fmcg-route-ai-agent/**

> After forking/pushing to GitHub, enable GitHub Pages (Settings → Pages → Branch: `main` → Root `/`) and replace `YOUR-USERNAME` with your GitHub username above.

---

## 📂 Files

| File | Description |
|------|-------------|
| `index.html` | Fully self-contained interactive UI — runs in any browser, no setup needed |
| `delivery_demand.csv` | Sample dataset with 10 synthetic outlets |
| `route_optimizer_agent.py` | Python version of the same solver (no dependencies) |

---

## 🚀 Run Locally

**Option 1: Browser (zero setup)**
Just open `index.html` directly in Chrome, Safari, or Firefox.

**Option 2: Python script**
```bash
python3 route_optimizer_agent.py
```
No pip installs required — uses Python standard library only.

---

## 🧠 The 5-Step AI Agent Pipeline

| Step | Logic |
|------|-------|
| 1 | **Demand Signal** — compute `weeks_of_cover = stock / offtake`; flag outlets < 2.5 wks as URGENT |
| 2 | **Zone Clustering** — group outlets by geographic zone (North/East/South/Central) |
| 3 | **Greedy Load Building** — prioritize URGENT → WATCH; fill trucks to 85% capacity |
| 4 | **Nearest-Neighbour Routing** — sequence stops by closest unvisited from warehouse |
| 5 | **Dispatch Plan Output** — auditable plan with truck, zone, stops, cases, utilization % |

---

## 📤 Upload Your Own Data

Click **Upload CSV** in the demo UI. Your file must match this schema:

| Column | Type | Description |
|--------|------|-------------|
| `outlet_id` | string | Unique store identifier |
| `zone` | string | North / East / South / Central |
| `current_inventory_stock` | number | Units in stockroom |
| `average_weekly_offtake` | number | Units sold per week |
| `order_quantity_cases` | number | Cases requested for delivery |
| `lat` | number | Latitude |
| `lon` | number | Longitude |

Download [`delivery_demand.csv`](./delivery_demand.csv) as a starting template.
