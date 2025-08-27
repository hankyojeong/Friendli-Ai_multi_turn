import sqlite3
import pandas as pd
FILE = "C:/Users/hanky/OneDrive/Desktop/서울대학교/IDEA 연구실/LLM/Friendli AI/data/3_외국인근로자.xlsx"
TBL_RAW = "3_tb_foreign_workers_permit"
Q_TBL = '"' + TBL_RAW + '"'

# load
df = pd.read_excel(FILE)
con = sqlite3.connect(":memory:")
df.to_sql(TBL_RAW, con, index=False)

# SQL: 월별 추이
sql = '''
SELECT
  SUBSTR(TRIM("base_ym"),1,4) AS year,
  SUBSTR(TRIM("base_ym"),6,2) AS month,
  COALESCE(SUM(CAST("cnt" AS INT)), 0) AS cnt
FROM {Q_TBL}
GROUP BY SUBSTR(TRIM("base_ym"),1,4), SUBSTR(TRIM("base_ym"),6,2)
ORDER BY year, month
'''.format(Q_TBL=Q_TBL)

out = pd.read_sql_query(sql, con)
print(out.to_csv(index=False))