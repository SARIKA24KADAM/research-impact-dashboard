"""Create deterministic, entirely fictional research-program example data."""
from __future__ import annotations
import csv, random
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "synthetic"
SEED = 24062026
rng = random.Random(SEED)

def write(name, rows):
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / name).open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)

themes = [{"ThemeID":"T01","ThemeName":"Battery Materials"},{"ThemeID":"T02","ThemeName":"Grid Electrification"},{"ThemeID":"T03","ThemeName":"Charging Infrastructure"},{"ThemeID":"T04","ThemeName":"Industrial Decarbonization"}]
owners = [{"OwnerID":f"O{i:02}","OwnerName":n,"Role":r} for i,(n,r) in enumerate([("Alex Morgan","Program Lead"),("Jordan Lee","Research Lead"),("Casey Patel","Project Manager"),("Taylor Chen","Data Steward"),("Riley Shah","Finance Partner"),("Avery Kim","Research Lead")],1)]
projects=[]
for i in range(1,13):
    start=date(2023+int((i-1)%3==0),1+((i*2)%12),1)
    projects.append({"ProjectID":f"P{i:03}","ProjectName":f"Demonstration Project {i:02}","ThemeID":themes[(i-1)%4]["ThemeID"],"OwnerID":owners[(i-1)%len(owners)]["OwnerID"],"StartDate":start.isoformat(),"PlannedEndDate":"2026-12-31","ProjectStatus":["Active","Active","At Risk","Completed"][(i-1)%4],"Priority":["High","Medium","Medium","Low"][(i-1)%4]})
kpis=[
{"KPIID":"K01","KPIName":"Prototype readiness","Unit":"points (0-100)","Frequency":"Quarterly","TargetDirection":"Higher","DefaultTarget":75,"Definition":"Illustrative readiness score; scale and rubric are fictional."},
{"KPIID":"K02","KPIName":"Research outputs","Unit":"count","Frequency":"Quarterly","TargetDirection":"Higher","DefaultTarget":2,"Definition":"Count of outputs recorded for the project and quarter."},
{"KPIID":"K03","KPIName":"Partner engagement","Unit":"engagements","Frequency":"Quarterly","TargetDirection":"Higher","DefaultTarget":3,"Definition":"Illustrative count of documented partner engagements."},
{"KPIID":"K04","KPIName":"Energy intensity reduction","Unit":"percent","Frequency":"Quarterly","TargetDirection":"Higher","DefaultTarget":8,"Definition":"Illustrative reduction from a fictional project baseline."}]
for name, data in [("themes.csv",themes),("owners.csv",owners),("projects.csv",projects),("kpi_definitions.csv",kpis)]: write(name,data)
budgets=[]
for p in projects:
    base=rng.randrange(240000,650001,10000)
    for y in range(2023,2027): budgets.append({"BudgetID":f"{p['ProjectID']}-{y}","ProjectID":p["ProjectID"],"FiscalYear":y,"ApprovedBudgetCAD":base,"ApprovedDate":f"{y}-01-15","Currency":"CAD"})
write("budgets.csv",budgets)
commitments=[]
for p in projects:
    for n in range(1,4): commitments.append({"CommitmentID":f"C-{p['ProjectID']}-{n:02}","ProjectID":p["ProjectID"],"FunderName":["Demo Public Funder","Demo Foundation","Institutional Match"][n-1],"CommitmentDate":date(2023+n-1,3*n,15).isoformat(),"AmountCAD":rng.randrange(20000,140001,5000),"Status":["Active","Active","Closed"][n-1]})
write("commitments.csv",commitments)
expenditures=[]
for p in projects:
    for q in range(12):
        y,quarter=2023+q//4,q%4+1
        expenditures.append({"ExpenditureID":f"E-{p['ProjectID']}-Q{q+1:02}","ProjectID":p["ProjectID"],"TransactionDate":date(y,quarter*3,20).isoformat(),"FiscalYear":y,"AmountCAD":rng.randrange(18000,52001,1000),"Category":["Personnel","Equipment","Travel","Materials"][q%4],"Status":"Posted"})
write("expenditures.csv",expenditures)
actuals=[]
for p in projects:
    for q in range(12):
        y,quarter=2023+q//4,q%4+1; month=quarter*3
        end=date(y,month,28 if month==2 else 30 if month in (4,6,9,11) else 31)
        for k in kpis:
            target=float(k["DefaultTarget"])
            if k["KPIID"]=="K01": value=round(min(100,48+q*3.4+rng.uniform(-7,7)),1)
            elif k["KPIID"]=="K02": value=rng.randrange(0,5)
            elif k["KPIID"]=="K03": value=rng.randrange(1,7)
            else: value=round(max(0,q*.7+rng.uniform(-1.5,2.2)),1)
            actuals.append({"ActualID":f"A-{p['ProjectID']}-{k['KPIID']}-Q{q+1:02}","ProjectID":p["ProjectID"],"KPIID":k["KPIID"],"PeriodStart":date(y,(quarter-1)*3+1,1).isoformat(),"PeriodEnd":end.isoformat(),"ActualValue":value,"TargetValue":target,"SubmissionStatus":"Received","IsFictional":"True"})
write("kpi_actuals.csv",actuals)
obligations=[]
for p in projects:
    for q in range(12):
        y,quarter=2023+q//4,q%4+1; due=date(y,quarter*3,28 if quarter==1 else 30 if quarter in (2,3) else 31)
        late=(q+int(p["ProjectID"][-1]))%7==0; received=due+timedelta(days=8 if late else -2)
        obligations.append({"ObligationID":f"R-{p['ProjectID']}-Q{q+1:02}","ProjectID":p["ProjectID"],"ReportingPeriodEnd":due.isoformat(),"DueDate":due.isoformat(),"ReceivedDate":received.isoformat(),"Status":"Late" if late else "On Time","ReportingType":"Quarterly progress"})
write("reporting_obligations.csv",obligations)
milestones=[]
for p in projects:
    for m in range(1,5):
        due=date(2024+(m-1)//2,m*3,15); state=["Complete","On Track","At Risk","Overdue"][(m+int(p["ProjectID"][-1]))%4]
        actual=due-timedelta(days=5) if state=="Complete" else None
        if state=="Overdue": due=date(2024,12,15)
        milestones.append({"MilestoneID":f"M-{p['ProjectID']}-{m:02}","ProjectID":p["ProjectID"],"MilestoneName":["Design review","Prototype build","Partner trial","Final report"][m-1],"DueDate":due.isoformat(),"ActualDate":actual.isoformat() if actual else "","Status":state,"OwnerID":p["OwnerID"],"Priority":"High" if m==4 else "Medium"})
write("milestones.csv",milestones)
outputs=[]
for i in range(1,49):
    p=projects[(i-1)%len(projects)]
    outputs.append({"OutputID":f"O-{i:03}","ProjectID":p["ProjectID"],"OutputType":["Journal article","Conference paper","Dataset","Technical report"][i%4],"Title":f"Demonstration research output {i:02}","PublicationDate":date(2023+i%3,i%12+1,15).isoformat(),"PeerReviewed":"Yes" if i%4 in (0,1) else "No","Status":"Published"})
write("research_outputs.csv",outputs)
risks=[]
for i,p in enumerate(projects,1): risks.append({"RiskID":f"RK-{i:03}","ProjectID":p["ProjectID"],"RiskCategory":["Supply chain","Schedule","Partner capacity","Data availability"][i%4],"Description":"Fictional example risk for dashboard demonstration.","Likelihood":["Low","Medium","High"][i%3],"Impact":["Medium","High","Low"][i%3],"Status":"Open" if i%3 else "Mitigated"})
write("risks.csv",risks)
actions=[]
for i,r in enumerate(risks,1): actions.append({"ActionID":f"AC-{i:03}","RiskID":r["RiskID"],"ProjectID":r["ProjectID"],"ActionDescription":"Fictional mitigation: review dependencies and agree a recovery plan.","OwnerID":projects[i-1]["OwnerID"],"DueDate":date(2025,i%12+1,20).isoformat(),"Status":"In Progress" if i%3 else "Complete"})
write("corrective_actions.csv",actions)
dq=[]
for i in range(1,17):
    p=projects[(i-1)%len(projects)]
    dq.append({"IssueID":f"DQ-{i:03}","ProjectID":p["ProjectID"],"TableName":["KPI Actuals","Milestones","Finance","Reporting"][i%4],"IssueType":["Late submission","Missing metadata","Definition clarification","Source reconciliation"][i%4],"Severity":"Medium" if i%4 else "High","Description":"Fictional issue-tracker example; not a failed generator check.","Status":"Open" if i%3 else "Resolved","OpenedDate":date(2025,i%12+1,5).isoformat(),"OwnerID":p["OwnerID"]})
write("dq_issues.csv",dq)
print(f"Generated fictional CSV tables in {OUT} using seed {SEED}.")
