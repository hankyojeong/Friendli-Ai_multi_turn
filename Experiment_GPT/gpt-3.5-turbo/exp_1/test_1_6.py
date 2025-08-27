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
WITH BaseData AS (
  SELECT
    p_year,
    p_month,
    COALESCE(SUM(CAST(cnt AS INT)), 0) AS total_cnt
  FROM {Q_TBL}
  WHERE UPPER(TRIM(category)) IN ('장기체류거소', '장기체류등록')
  GROUP BY p_year, p_month
)
SELECT
  curr.p_year AS year,
  curr.p_month AS month,
  curr.total_cnt AS total_count,
  (curr.total_cnt - COALESCE(prev.total_cnt, 0)) / COALESCE(prev.total_cnt, 0) AS growth_rate
FROM BaseData AS curr
LEFT JOIN BaseData AS prev ON curr.p_year = prev.p_year + 1 AND curr.p_month = prev.p_month
WHERE (curr.p_year >= 2023 AND curr.p_year <= 2025) AND curr.p_month = 1
'''

out = pd.read_sql_query(sql, con)
print(out.to_csv(index=False))