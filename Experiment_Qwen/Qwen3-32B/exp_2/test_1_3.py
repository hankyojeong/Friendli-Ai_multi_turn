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
SELECT
  CAST("p_year" AS INT) AS year,
  CAST("p_month" AS INT) AS month,
  COALESCE(SUM(CAST("cnt" AS INT)), 0) AS cnt
FROM {Q_TBL}
WHERE UPPER(TRIM("category")) IN ('장기체류거소', '장기체류등록')
  AND CAST("p_year" AS INT) >= 2024
GROUP BY CAST("p_year" AS INT), CAST("p_month" AS INT)
ORDER BY year, month
'''.format(Q_TBL=Q_TBL)

out = pd.read_sql_query(sql, con)
print(out.to_csv(index=False))