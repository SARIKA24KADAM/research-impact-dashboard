"""Generate a source-controlled Power BI Project for this repository."""
import csv, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PROJECT="ResearchImpact"
REPORT=ROOT/f"{PROJECT}.Report"
MODEL=ROOT/f"{PROJECT}.SemanticModel"
RAW="https://raw.githubusercontent.com/SARIKA24KADAM/research-impact-dashboard/main/data/synthetic/"

FILES={"themes":"themes.csv","owners":"owners.csv","projects":"projects.csv","kpi_definitions":"kpi_definitions.csv","budgets":"budgets.csv","commitments":"commitments.csv","expenditures":"expenditures.csv","kpi_actuals":"kpi_actuals.csv","milestones":"milestones.csv","reporting_obligations":"reporting_obligations.csv","research_outputs":"research_outputs.csv","risks":"risks.csv","corrective_actions":"corrective_actions.csv","dq_issues":"dq_issues.csv"}
TYPES={"ApprovedBudgetCAD":("Currency.Type","decimal"),"AmountCAD":("Currency.Type","decimal"),"FiscalYear":("Int64.Type","int64"),"Year":("Int64.Type","int64"),"ActualValue":("type number","double"),"TargetValue":("type number","double"),"IsFictional":("type logical","boolean")}
DATES={"StartDate","PlannedEndDate","TransactionDate","ApprovedDate","CommitmentDate","DueDate","ActualDate","PeriodStart","PeriodEnd","ReportingPeriodEnd","ReceivedDate","PublicationDate","OpenedDate"}
def write(p,obj):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(obj if isinstance(obj,str) else json.dumps(obj,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
def headers(file):
    with (ROOT/"data"/"synthetic"/file).open(encoding="utf-8-sig",newline="") as f:return next(csv.reader(f))
def dtype(col):
    if col in TYPES:return TYPES[col][1]
    if col in DATES:return "dateTime"
    return "string"
def mtype(col):return TYPES.get(col,("type text",))[0] if col not in DATES else "type date"
def query(file,cols):
    pairs=", ".join("{"+json.dumps(c)+", "+mtype(c)+"}" for c in cols)
    return ["let",f'    Source = Csv.Document(Web.Contents("{RAW+file}"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),',"    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),",f'    Typed = Table.TransformColumnTypes(Headers, {{{pairs}}}, "en-CA")',"in","    Typed"]

measures={
"budgets":[("Approved Budget CAD","SUM(budgets[ApprovedBudgetCAD])","$#,##0;($#,##0);$#,##0"),("Budget Remaining CAD","[Approved Budget CAD] - [Actual Expenditure CAD]","$#,##0;($#,##0);$#,##0"),("Budget Utilization %","DIVIDE([Actual Expenditure CAD], [Approved Budget CAD])","0.0%")],
"expenditures":[("Actual Expenditure CAD",'CALCULATE(SUM(expenditures[AmountCAD]), expenditures[Status] = "Posted")',"$#,##0;($#,##0);$#,##0")],
"commitments":[("Active Commitments CAD",'CALCULATE(SUM(commitments[AmountCAD]), commitments[Status] = "Active")',"$#,##0;($#,##0);$#,##0")],
"projects":[("Active Projects",'CALCULATE(DISTINCTCOUNT(projects[ProjectID]), projects[ProjectStatus] = "Active")',"#,##0")],
"reporting_obligations":[("Expected Reports","COUNTROWS(reporting_obligations)","#,##0"),("On-time Reports",'CALCULATE(COUNTROWS(reporting_obligations), reporting_obligations[Status] = "On Time")',"#,##0"),("On-time Reporting %","DIVIDE([On-time Reports], [Expected Reports])","0.0%")],
"research_outputs":[("Recorded Research Outputs","COUNTROWS(research_outputs)","#,##0")],"risks":[("Open Risks",'CALCULATE(COUNTROWS(risks), risks[Status] = "Open")',"#,##0")],"dq_issues":[("Open Data Quality Issues",'CALCULATE(COUNTROWS(dq_issues), dq_issues[Status] = "Open")',"#,##0")],
"milestones":[("Milestone Count","COUNTROWS(milestones)","#,##0")],"kpi_actuals":[("Average KPI Actual","AVERAGE(kpi_actuals[ActualValue])","0.0"),("Prototype Readiness",'CALCULATE(AVERAGE(kpi_actuals[ActualValue]), kpi_actuals[KPIID] = "K01")',"0.0")]
}
model_tables=[]
for table,file in FILES.items():
    cols=headers(file); columns=[]
    for col in cols:
        t=dtype(col); c={"name":col,"dataType":t,"sourceColumn":col,"summarizeBy":"sum" if t in {"int64","double","decimal"} else "none"}
        if col.endswith("CAD"):c["formatString"]="$#,##0;($#,##0);$#,##0"
        columns.append(c)
    item={"name":table,"columns":columns,"partitions":[{"name":table,"mode":"import","source":{"type":"m","expression":query(file,cols)}}]}
    if table in measures:item["measures"]=[{"name":n,"expression":e,"formatString":fmt} for n,e,fmt in measures[table]]
    model_tables.append(item)

public_m=['let','    Source = Csv.Document(Web.Contents("https://raw.githubusercontent.com/SARIKA24KADAM/research-impact-dashboard/main/data/public/global-data-on-sustainable-energy.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),','    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),','    Canada = Table.SelectRows(Headers, each [Entity] = "Canada"),','    Selected = Table.SelectColumns(Canada, {"Entity", "Year", "Renewable energy share in the total final energy consumption (%)"}),','    Renamed = Table.RenameColumns(Selected, {{"Entity", "Country"}, {"Renewable energy share in the total final energy consumption (%)", "RenewableShare"}}),','    Typed = Table.TransformColumnTypes(Renamed, {{"Country", type text}, {"Year", Int64.Type}, {"RenewableShare", type number}}, "en-CA")','in','    Typed']
model_tables.append({"name":"public_energy_context","columns":[{"name":"Country","dataType":"string","sourceColumn":"Country","summarizeBy":"none"},{"name":"Year","dataType":"int64","sourceColumn":"Year","summarizeBy":"none"},{"name":"RenewableShare","dataType":"double","sourceColumn":"RenewableShare","summarizeBy":"average","formatString":"0.0"}],"partitions":[{"name":"public_energy_context","mode":"import","source":{"type":"m","expression":public_m}}]})
rels=[]
def rel(name,many,mcol,one,ocol):rels.append({"name":name,"fromTable":many,"fromColumn":mcol,"toTable":one,"toColumn":ocol,"crossFilteringBehavior":"oneDirection","isActive":True})
rel("Projects_Themes","projects","ThemeID","themes","ThemeID");rel("Projects_Owners","projects","OwnerID","owners","OwnerID")
rel("KPIActuals_Projects","kpi_actuals","ProjectID","projects","ProjectID");rel("KPIActuals_Definitions","kpi_actuals","KPIID","kpi_definitions","KPIID")
for fact in ("budgets","commitments","expenditures","milestones","reporting_obligations","research_outputs","risks","corrective_actions","dq_issues"):rel(f"{fact}_Projects",fact,"ProjectID","projects","ProjectID")
rel("Actions_Risks","corrective_actions","RiskID","risks","RiskID")
model={"compatibilityLevel":1600,"model":{"culture":"en-CA","sourceQueryCulture":"en-CA","defaultPowerBIDataSourceVersion":"powerBI_V3","dataAccessOptions":{"legacyRedirects":True,"returnErrorValuesAsNull":True},"discourageImplicitMeasures":False,"annotations":[],"expressions":[],"functions":[],"perspectives":[],"roles":[],"relationships":rels,"tables":model_tables}}
write(MODEL/"definition.pbism",{"$schema":"https://developer.microsoft.com/json-schemas/fabric/item/semanticModel/definitionProperties/1.0.0/schema.json","version":"4.0","settings":{"qnaEnabled":False}})
write(MODEL/"model.bim",model)
write(ROOT/f"{PROJECT}.pbip",{"$schema":"https://developer.microsoft.com/json-schemas/fabric/pbip/pbipProperties/1.0.0/schema.json","version":"1.0","artifacts":[{"report":{"path":f"{PROJECT}.Report"}}],"settings":{"enableAutoRecovery":True}})
write(REPORT/"definition.pbir",{"$schema":"https://developer.microsoft.com/json-schemas/fabric/item/report/definitionProperties/2.0.0/schema.json","version":"4.0","datasetReference":{"byPath":{"path":f"../{PROJECT}.SemanticModel"}}})
write(REPORT/"definition"/"version.json",{"$schema":"https://developer.microsoft.com/json-schemas/fabric/item/report/definition/versionMetadata/1.0.0/schema.json","version":"2.0.0"})
write(REPORT/"definition"/"report.json",{"$schema":"https://developer.microsoft.com/json-schemas/fabric/item/report/definition/report/3.0.0/schema.json","themeCollection":{"baseTheme":{"name":"CY24SU10","reportVersionAtImport":"5.61","type":"SharedResources"}}})

pages=[
("Overview","Executive overview",[("clusteredColumnChart","Portfolio finance by theme",[("Category","Column","themes","ThemeName","themes.ThemeName"),("Y","Measure","budgets","Approved Budget CAD","budgets.Approved Budget CAD"),("Y","Measure","expenditures","Actual Expenditure CAD","expenditures.Actual Expenditure CAD")]),("clusteredBarChart","Active projects by theme",[("Category","Column","themes","ThemeName","themes.ThemeName"),("Y","Measure","projects","Active Projects","projects.Active Projects")])]),
("Finance","Finance and delivery",[("clusteredColumnChart","Budget and expenditure by project",[("Category","Column","projects","ProjectName","projects.ProjectName"),("Y","Measure","budgets","Approved Budget CAD","budgets.Approved Budget CAD"),("Y","Measure","expenditures","Actual Expenditure CAD","expenditures.Actual Expenditure CAD")]),("clusteredBarChart","Milestones by status",[("Category","Column","milestones","Status","milestones.Status"),("Y","Measure","milestones","Milestone Count","milestones.Milestone Count")])]),
("KPIHealth","KPI and reporting health",[("lineChart","Prototype readiness by quarter",[("Category","Column","kpi_actuals","PeriodEnd","kpi_actuals.PeriodEnd"),("Y","Measure","kpi_actuals","Prototype Readiness","kpi_actuals.Prototype Readiness")]),("clusteredColumnChart","On-time submissions by quarter",[("Category","Column","reporting_obligations","ReportingPeriodEnd","reporting_obligations.ReportingPeriodEnd"),("Y","Measure","reporting_obligations","On-time Reports","reporting_obligations.On-time Reports")])]),
("ResearchContext","Research and public context",[("clusteredColumnChart","Research outputs by type",[("Category","Column","research_outputs","OutputType","research_outputs.OutputType"),("Y","Measure","research_outputs","Recorded Research Outputs","research_outputs.Recorded Research Outputs")]),("lineChart","Canada renewable energy share (public context)",[("Category","Column","public_energy_context","Year","public_energy_context.Year"),("Y","Column","public_energy_context","RenewableShare","public_energy_context.RenewableShare")])])]
page_ids=["Overview_01","Finance_02","KPIHealth_03","ResearchContext_04"]
write(REPORT/"definition"/"pages"/"pages.json",{"$schema":"https://developer.microsoft.com/json-schemas/fabric/item/report/definition/pagesMetadata/1.0.0/schema.json","pageOrder":page_ids,"activePageName":page_ids[0]})
for (slug,title,visuals),pid in zip(pages,page_ids):
    root=REPORT/"definition"/"pages"/pid
    write(root/"page.json",{"$schema":"https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.1.0/schema.json","name":pid,"displayName":title,"displayOption":"FitToPage","height":720,"width":1280})
    for i,(kind,vtitle,fields) in enumerate(visuals,1):
        qs={}
        for role,ft,entity,prop,qref in fields:
            field={"Column":{"Expression":{"SourceRef":{"Entity":entity}},"Property":prop}} if ft=="Column" else {"Measure":{"Expression":{"SourceRef":{"Entity":entity}},"Property":prop}}
            qs.setdefault(role,[]).append({"field":field,"queryRef":qref,"nativeQueryRef":prop,"active":True})
        vid=f"{slug}_Visual_{i:02}"
        visual={"$schema":"https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.9.0/schema.json","name":vid,"position":{"x":30+(i-1)*615,"y":60,"z":i*1000,"height":570,"width":590,"tabOrder":i},"visual":{"visualType":kind,"query":{"queryState":{role:{"projections":vals} for role,vals in qs.items()}},"objects":{},"visualContainerObjects":{"title":[{"properties":{"text":{"expr":{"Literal":{"Value":json.dumps("'"+vtitle+"'")}}}}}]}}}
        write(root/"visuals"/vid/"visual.json",visual)

gitignore=ROOT/".gitignore"; current=gitignore.read_text(encoding="utf-8") if gitignore.exists() else ""
for item in ("**/.pbi/localSettings.json","**/.pbi/cache.abf"):
    if item not in current:current+=("\n" if current and not current.endswith("\n") else "")+item+"\n"
write(gitignore,current)
print(f"Created {PROJECT}.pbip with 15 model tables and 4 report pages")

