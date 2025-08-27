import sqlite3
import pandas as pd
FILE = "C:/Users/hanky/OneDrive/Desktop/서울대학교/IDEA 연구실/LLM/Friendli AI/data/1_국내체류외국인.xlsx"
TBL_RAW = "1_tb_resident_foreigners"
Q_TBL = '"' + TBL_RAW + '"'

if FILE.lower().endswith(".xlsx"):
    df = pd.read_excel(FILE)
else:
    df = pd.read_csv(FILE, encoding="utf-8-sig", low_memory=False)

con = sqlite3.connect(":memory:")
df.to_sql(TBL_RAW, con, index=False)

sql = '''
WITH yearly_march AS (
  SELECT
    "p_year" AS year,
    COALESCE(SUM(CAST("cnt" AS INT)), 0) AS cnt
  FROM {Q_TBL}
  WHERE UPPER(TRIM("category")) IN ('장기체류거소', '장기체류등록')
    AND "p_month" = 3
    AND "p_year" BETWEEN 2023 AND 2025
  GROUP BY "p_year"
  ORDER BY "p_year"
)
SELECT
  year,
  cnt,
  ROUND(
    100.0 * (cnt - LAG(cnt, 1) OVER (ORDER BY year)) 
    / NULLIF(LAG(cnt, 1) OVER (ORDER BY year), 0),
    2
  ) AS growth_rate_pct
FROM yearly_march
ORDER BY year
'''.format(Q_TBL=Q_TBL)

out = pd.read_sql_query(sql, con)
print(out.to_csv(index=False))