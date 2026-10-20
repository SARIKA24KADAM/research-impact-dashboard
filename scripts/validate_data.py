"""Run lightweight structural checks over the generated fictional tables."""
import csv, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/"data"/"synthetic"; OUT=ROOT/"data"/"processed"/"validation_summary.json"
def rows(name):
    with (DATA/name).open(encoding="utf-8-sig",newline="") as f: return list(csv.DictReader(f))
def dups(values): return len(values)-len(set(values))
spec={"themes.csv":"ThemeID","owners.csv":"OwnerID","projects.csv":"ProjectID","kpi_definitions.csv":"KPIID","budgets.csv":"BudgetID","commitments.csv":"CommitmentID","expenditures.csv":"ExpenditureID","kpi_actuals.csv":"ActualID","reporting_obligations.csv":"ObligationID","milestones.csv":"MilestoneID","research_outputs.csv":"OutputID","risks.csv":"RiskID","corrective_actions.csv":"ActionID","dq_issues.csv":"IssueID"}
tables={n:rows(n) for n in spec}; checks={}
for name,key in spec.items():
    vals=[r[key] for r in tables[name]]; checks[f"{name}: unique non-empty {key}"]={"passed":not any(not x for x in vals) and dups(vals)==0,"rows":len(vals),"duplicate_count":dups(vals),"empty_key_count":sum(not x for x in vals)}
project_ids={r["ProjectID"] for r in tables["projects.csv"]}
for name in ("budgets.csv","commitments.csv","expenditures.csv","kpi_actuals.csv","reporting_obligations.csv","milestones.csv","research_outputs.csv","risks.csv","corrective_actions.csv","dq_issues.csv"):
    invalid=sum(r["ProjectID"] not in project_ids for r in tables[name]); checks[f"{name}: project references resolve"]={"passed":invalid==0,"invalid_count":invalid}
for name,cols in {"budgets.csv":["ApprovedBudgetCAD"],"commitments.csv":["AmountCAD"],"expenditures.csv":["AmountCAD"],"kpi_actuals.csv":["ActualValue","TargetValue"]}.items():
    invalid=0
    for row in tables[name]:
        for col in cols:
            try: invalid += float(row[col])<0
            except (ValueError,TypeError): invalid += 1
    checks[f"{name}: numeric and non-negative {','.join(cols)}"]={"passed":invalid==0,"invalid_count":int(invalid)}
summary={"project":"Research Program Performance & Impact Reporting Dashboard","fictional_data":True,"check_count":len(checks),"passed_count":sum(bool(c["passed"]) for c in checks.values()),"all_passed":all(c["passed"] for c in checks.values()),"checks":checks}
OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"all_passed":summary["all_passed"],"passed":summary["passed_count"],"checks":summary["check_count"],"output":str(OUT)},indent=2))
if not summary["all_passed"]: raise SystemExit(1)
