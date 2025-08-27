import sqlite3
import pandas as pd
FILE = "C:/Users/hanky/OneDrive/Desktop/서울대학교/IDEA 연구실/LLM/Friendli AI/data/1_국내체류외국인.xlsx"
TBL_RAW = "1_tb_resident_foreigners"
Q_TBL = '"' + TBL_RAW + '"'

# load
if FILE.lower().endswith(".xlsx"):
    df = pd.read_excel(FILE)
else:
    df = pd.read_csv(FILE, encoding="utf-8-sig", low_memory=False)

con = sqlite3.connect(":memory:")
df.to_sql(TBL_RAW, con, index=False)

# SQL: March 2023~2025 장기체류 합계와 전기 증감률
sql = '''
WITH yearly AS (
  SELECT
    CAST("p_year" AS INT) AS year,
    COALESCE(SUM(CAST("cnt" AS INT)), 0) AS total
  FROM {Q_TBL}
  WHERE
    UPPER(TRIM("category")) IN ('장기체류거소', '장기체류등록')
    AND CAST("p_month" AS INT) = 3
    AND CAST("p_year" AS INT) BETWEEN 2023 AND 2025
  GROUP BY CAST("p_year" AS INT)
)
SELECT
  y.year,
  y.total,
  (SELECT y2.total FROM yearly y2 WHERE y2.year = y.year - 1) AS prev,
  (y.total - (SELECT y2.total FROM yearly y2 WHERE y2.year = y.year - 1)) AS diff,
  COALESCE(
    ROUND(
      (y.total * 100.0 / NULLIF((SELECT y2.total FROM yearly y2 WHERE y2.year = y.year - 1), 0) - 100),
      2
    ),
    0
  ) AS growth_rate
FROM yearly y
ORDER BY year
'''.format(Q_TBL=Q_TBL)

out = pd.read_sql_query(sql, con)
print(out.to_csv(index=False))