// Power Query template. Set pDataFolder to the local data/synthetic directory.
let
    Source = Csv.Document(File.Contents(pDataFolder & "\expenditures.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    Types = Table.TransformColumnTypes(Headers, {{"ExpenditureID", type text}, {"ProjectID", type text}, {"TransactionDate", type date}, {"FiscalYear", Int64.Type}, {"AmountCAD", Currency.Type}, {"Category", type text}, {"Status", type text}}),
    Posted = Table.SelectRows(Types, each [Status] = "Posted"),
    ValidAmounts = Table.SelectRows(Posted, each [AmountCAD] >= 0)
in
    ValidAmounts
