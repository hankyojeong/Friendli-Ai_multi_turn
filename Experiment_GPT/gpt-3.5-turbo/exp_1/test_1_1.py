import sqlite3
import pandas as pd
FILE = "C:/Users/hanky/OneDrive/Desktop/서울대학교/IDEA 연구실/LLM/Friendli AI/data/1_국내체류외국인.xlsx"
TBL_RAW = "1_tb_resident_foreigners"
Q_TBL = '"' + TBL_RAW + '"'

# load
df = pd.read_excel(FILE)
con = sqlite3.connect(":memory:")
df.to_sql(TBL_RAW, con, index=False)

# SQL: 2025년 4월 기준 국내 단기 체류 외국인 수
sql = '''
WITH normalized AS (
  SELECT
    CAST("p_year" AS INT) AS year,
    CAST("p_month" AS INT) AS month,
    COALESCE(SUM(CAST("cnt" AS INT)), 0) AS cnt,
    UPPER(TRIM("category")) AS category
  FROM {Q_TBL}
  GROUP BY year, month, category
)
SELECT
  year,
  month,
  COALESCE(SUM(CASE WHEN category = '단기체류' THEN cnt ELSE 0 END), 0) AS short_term_resident_foreigners
FROM normalized
WHERE year = 2025 AND month = 4
GROUP BY year, month
'''.format(Q_TBL=Q_TBL)

out = pd.read_sql_query(sql, con)
print(out.to_csv(index=False))