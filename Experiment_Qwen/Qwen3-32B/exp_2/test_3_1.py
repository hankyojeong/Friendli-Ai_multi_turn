import sqlite3
import pandas as pd
FILE = "C:/Users/hanky/OneDrive/Desktop/서울대학교/IDEA 연구실/LLM/Friendli AI/data/3_외국인근로자.xlsx"
TBL_RAW = "3_tb_foreign_workers_permit"
Q_TBL = '"' + TBL_RAW + '"'

# load
if FILE.lower().endswith(".xlsx"):
    df = pd.read_excel(FILE)
else:
    df = pd.read_csv(FILE, encoding="utf-8-sig", low_memory=False)

con = sqlite3.connect(":memory:")
df.to_sql(TBL_RAW, con, index=False)

# SQL: 분기→월 전개 후 월별 집계
sql = '''
WITH quarterly_data AS (
  SELECT 
    REPLACE(REPLACE(REPLACE(TRIM("base_ym"), '-', ''), '_', ''), '.', '') AS base_ym,
    CAST("cnt" AS INT) AS cnt
  FROM {Q_TBL}
),
quarter_to_months AS (
  SELECT '1Q' AS quarter, '01' AS month UNION ALL
  SELECT '1Q', '02' UNION ALL
  SELECT '1Q', '03' UNION ALL
  SELECT '2Q', '04' UNION ALL
  SELECT '2Q', '05' UNION ALL
  SELECT '2Q', '06' UNION ALL
  SELECT '3Q', '07' UNION ALL
  SELECT '3Q', '08' UNION ALL
  SELECT '3Q', '09' UNION ALL
  SELECT '4Q', '10' UNION ALL
  SELECT '4Q', '11' UNION ALL
  SELECT '4Q', '12'
),
expanded_data AS (
  SELECT 
    q.base_ym,
    q.cnt,
    m.month
  FROM quarterly_data q
  JOIN quarter_to_months m
  ON CASE 
    WHEN SUBSTR(q.base_ym, 5, 2) IN ('01','02','03') THEN '1Q'
    WHEN SUBSTR(q.base_ym, 5, 2) IN ('04','05','06') THEN '2Q'
    WHEN SUBSTR(q.base_ym, 5, 2) IN ('07','08','09') THEN '3Q'
    ELSE '4Q'
  END = m.quarter
)
SELECT 
  CAST(SUBSTR(base_ym, 1, 4) AS INT) AS year,
  CAST(month AS INT) AS month,
  COALESCE(SUM(cnt), 0) AS cnt
FROM expanded_data
GROUP BY SUBSTR(base_ym, 1, 4), month
ORDER BY year, month
'''.format(Q_TBL=Q_TBL)

out = pd.read_sql_query(sql, con)
print(out.to_csv(index=False))