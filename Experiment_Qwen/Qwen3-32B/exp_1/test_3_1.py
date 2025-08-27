import sqlite3
import pandas as pd
FILE = "C:/Users/hanky/OneDrive/Desktop/서울대학교/IDEA 연구실/LLM/Friendli AI/data/3_외국인근로자.xlsx"
TBL_RAW = "3_tb_foreign_workers_permit"
Q_TBL = '"' + TBL_RAW + '"'

if FILE.lower().endswith(".xlsx"):
    df = pd.read_excel(FILE)
else:
    df = pd.read_csv(FILE, encoding="utf-8-sig", low_memory=False)

con = sqlite3.connect(":memory:")
df.to_sql(TBL_RAW, con, index=False)

sql = '''
WITH X AS (
  SELECT 
    CAST(SUBSTR(REPLACE(REPLACE(REPLACE(TRIM("base_ym"), '-', ''), '_', ''), '.', ''), 1, 4) AS INT) AS "year",
    CAST(SUBSTR(REPLACE(REPLACE(REPLACE(TRIM("base_ym"), '-', ''), '_', ''), '.', ''), 5, 2) AS INT) AS "month",
    COALESCE(CAST("cnt" AS INT), 0) AS "cnt"
  FROM {Q_TBL}
)
SELECT 
  "year",
  "month",
  SUM("cnt") AS "cnt"
FROM X
GROUP BY "year", "month"
ORDER BY "year", "month"
'''.format(Q_TBL=Q_TBL)

out = pd.read_sql_query(sql, con)
print(out.to_csv(index=False))