// Power Query template. Set pDataFolder to the local data/synthetic directory.
let
    Source = Csv.Document(File.Contents(pDataFolder & "\projects.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    Types = Table.TransformColumnTypes(Headers, {{"ProjectID", type text}, {"ProjectName", type text}, {"ThemeID", type text}, {"OwnerID", type text}, {"StartDate", type date}, {"PlannedEndDate", type date}, {"ProjectStatus", type text}, {"Priority", type text}}),
    ValidKeys = Table.SelectRows(Types, each [ProjectID] <> null and Text.Trim([ProjectID]) <> "")
in
    ValidKeys
