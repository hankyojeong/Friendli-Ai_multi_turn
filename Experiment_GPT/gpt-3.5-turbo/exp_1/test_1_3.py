import sqlite3
import pandas as pd
FILE = "C:/Users/hanky/OneDrive/Desktop/서울대학교/IDEA 연구실/LLM/Friendli AI/data/1_국내체류외국인.xlsx"
TBL_RAW = "1_tb_resident_foreigners"
Q_TBL = '"' + TBL_RAW + '"'

# load
df = pd.read_excel(FILE)
con = sqlite3.connect(":memory:")
df.to_sql(TBL_RAW, con, index=False)

# SQL: 2024년 이후 월별 장기체류 외국인수 추이
sql = '''
SELECT
  "p_year" AS year,
  "p_month" AS month,
  COALESCE(SUM("cnt"),0) AS long_term_residents
FROM {Q_TBL}
WHERE "category" IN ('장기체류거소', '장기체류등록')
  AND "p_year" >= 2024
GROUP BY "p_year", "p_month"
ORDER BY "p_year", "p_month"
'''.format(Q_TBL=Q_TBL)

out = pd.read_sql_query(sql, con)
print(out.to_csv(index=False))