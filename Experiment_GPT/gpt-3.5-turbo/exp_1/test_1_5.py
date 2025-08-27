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
WITH base_data AS (
  SELECT
    p_year,
    p_month,
    SUM(CAST(cnt AS INT)) AS total_cnt
  FROM {Q_TBL}
  WHERE category IN ('장기체류거소', '장기체류등록')
    AND (p_year || '-' || substr('00' || p_month, -2, 2)) BETWEEN '2023-03' AND '2025-03'
  GROUP BY p_year, p_month
)

SELECT
  B.p_year AS year,
  B.total_cnt AS resident_foreigners_count,
  ROUND((B.total_cnt - COALESCE(L.total_cnt, 0)) / COALESCE(L.total_cnt, 1) * 100, 2) AS growth_rate
FROM base_data B
LEFT JOIN base_data L ON B.p_year = L.p_year + 1 AND B.p_month = L.p_month
WHERE B.p_month = 3
ORDER BY B.p_year
'''.format(Q_TBL=Q_TBL)

out = pd.read_sql_query(sql, con)
print(out.to_csv(index=False))