import sqlite3
import pandas as pd
FILE = "C:/Users/hanky/OneDrive/Desktop/서울대학교/IDEA 연구실/LLM/Friendli AI/data/1_국내체류외국인.xlsx"
TBL_RAW = "1_tb_resident_foreigners"
Q_TBL = '"' + TBL_RAW + '"'

# load
df = pd.read_excel(FILE)
con = sqlite3.connect(":memory:")
df.to_sql(TBL_RAW, con, index=False)

# SQL: 2023~2025년 1월 장기체류 외국인 수와 전년 대비 증감률
sql = '''
WITH Base AS (
  SELECT
    "p_year",
    "p_month",
    COALESCE(SUM(CAST("cnt" AS INT)),0) AS cnt
  FROM {Q_TBL}
  WHERE "category" IN ('장기체류거소','장기체류등록')
    AND ("p_year" BETWEEN 2023 AND 2025)
    AND ("p_month" = 1)
  GROUP BY "p_year", "p_month"
)
SELECT
  B1."p_year" AS year,
  B1."cnt" AS cnt,
  ROUND((B1."cnt" - B2."cnt") * 100.0 / NULLIF(B2."cnt",0), 2) AS growth_rate
FROM Base AS B1
LEFT JOIN Base AS B2 ON B1."p_year" = B2."p_year" + 1
ORDER BY year
'''.format(Q_TBL=Q_TBL)

out = pd.read_sql_query(sql, con)
print(out.to_csv(index=False))