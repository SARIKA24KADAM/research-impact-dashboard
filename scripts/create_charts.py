"""Create static PNG previews from the fictional operational sample."""
import csv
from collections import defaultdict
from pathlib import Path
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/"data"/"synthetic"; OUT=ROOT/"reports"/"figures"; OUT.mkdir(parents=True,exist_ok=True)
def read(name):
    with (DATA/name).open(encoding="utf-8-sig",newline="") as f: return list(csv.DictReader(f))
projects,themes=read("projects.csv"),read("themes.csv"); theme_name={r["ThemeID"]:r["ThemeName"] for r in themes}; project_theme={r["ProjectID"]:theme_name[r["ThemeID"]] for r in projects}
budget,spend,commitments=defaultdict(float),defaultdict(float),defaultdict(float)
for r in read("budgets.csv"):
    if r["FiscalYear"]=="2025": budget[project_theme[r["ProjectID"]]]+=float(r["ApprovedBudgetCAD"])
for r in read("expenditures.csv"):
    if r["FiscalYear"]=="2025": spend[project_theme[r["ProjectID"]]]+=float(r["AmountCAD"])
for r in read("commitments.csv"):
    if r["Status"]=="Active": commitments[project_theme[r["ProjectID"]]]+=float(r["AmountCAD"])
names=list(theme_name.values()); fig,ax=plt.subplots(figsize=(10,5.4)); x=list(range(len(names))); w=.25
ax.bar([i-w for i in x],[budget[n]/1e6 for n in names],w,label="Approved budget")
ax.bar(x,[commitments[n]/1e6 for n in names],w,label="Active commitments")
ax.bar([i+w for i in x],[spend[n]/1e6 for n in names],w,label="2025 expenditure")
ax.set_xticks(x,names,rotation=15,ha="right"); ax.set_ylabel("CAD (millions)"); ax.set_title("Fictional portfolio finance by theme"); ax.legend(frameon=False,ncols=3); ax.grid(axis="y",alpha=.2); fig.tight_layout(); fig.savefig(OUT/"budget_by_theme.png",dpi=180,bbox_inches="tight"); plt.close(fig)
actuals=[r for r in read("kpi_actuals.csv") if r["KPIID"]=="K01"]; series=defaultdict(list)
for r in actuals: series[r["PeriodEnd"][:7]].append(float(r["ActualValue"]))
periods=sorted(series); means=[sum(series[p])/len(series[p]) for p in periods]
fig,ax=plt.subplots(figsize=(10,4.8)); ax.plot(periods,means,marker="o",color="#177E89",linewidth=2); ax.axhline(75,color="#D1495B",linestyle="--",label="Illustrative target (75)"); ax.set_title("Fictional prototype readiness: quarterly portfolio average"); ax.set_ylabel("Readiness points (0-100)"); ax.set_xlabel("Quarter end"); ax.tick_params(axis="x",rotation=45); ax.legend(frameon=False); ax.grid(alpha=.2); fig.tight_layout(); fig.savefig(OUT/"kpi_trend.png",dpi=180,bbox_inches="tight"); plt.close(fig)
counts=defaultdict(int)
for r in read("milestones.csv"): counts[r["Status"]]+=1
labels=["Complete","On Track","At Risk","Overdue"]; fig,ax=plt.subplots(figsize=(7,4.8)); bars=ax.bar(labels,[counts[s] for s in labels],color=["#2A9D8F","#8AB17D","#E9C46A","#E76F51"]); ax.bar_label(bars,padding=3); ax.set_title("Fictional milestone status"); ax.set_ylabel("Milestones"); ax.spines[["top","right"]].set_visible(False); ax.grid(axis="y",alpha=.2); fig.tight_layout(); fig.savefig(OUT/"milestone_status.png",dpi=180,bbox_inches="tight"); plt.close(fig)
print(f"Wrote three PNG charts to {OUT}")

# Public country series is intentionally charted on its own, separate from the demo program.
public_path = ROOT / "data" / "public" / "global-data-on-sustainable-energy.csv"
with public_path.open(encoding="utf-8-sig", newline="") as f:
    public_rows = [r for r in csv.DictReader(f) if r["Entity"] == "Canada"]
public_rows = sorted(public_rows, key=lambda r: int(r["Year"]))
years = [int(r["Year"]) for r in public_rows]
renewable_share = [float(r["Renewable energy share in the total final energy consumption (%)"]) if r["Renewable energy share in the total final energy consumption (%)"] else float("nan") for r in public_rows]
fig, ax = plt.subplots(figsize=(9, 4.8))
ax.plot(years, renewable_share, color="#4C956C", marker="o", markersize=3, linewidth=1.8)
ax.set_title("Canada: renewable share of final energy consumption")
ax.set_ylabel("Percent")
ax.set_xlabel("Year")
ax.grid(alpha=.2)
fig.tight_layout()
fig.savefig(OUT / "canada_renewable_share.png", dpi=180, bbox_inches="tight")
plt.close(fig)
print("Wrote one separately attributed public-data chart.")
