// Power Query template. Keep missing submissions separate from numeric zero.
let
    Source = Csv.Document(File.Contents(pDataFolder & "\kpi_actuals.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    Types = Table.TransformColumnTypes(Headers, {{"ActualID", type text}, {"ProjectID", type text}, {"KPIID", type text}, {"PeriodStart", type date}, {"PeriodEnd", type date}, {"ActualValue", type number}, {"TargetValue", type number}, {"SubmissionStatus", type text}, {"IsFictional", type logical}}),
    ValidKeys = Table.SelectRows(Types, each [ProjectID] <> null and [KPIID] <> null and [PeriodEnd] <> null)
in
    ValidKeys
