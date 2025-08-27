import sqlite3
import pandas as pd
FILE = "C:/Users/hanky/OneDrive/Desktop/서울대학교/IDEA 연구실/LLM/Friendli AI/data/2_장기체류외국인_지역별_현황.csv"
TBL_RAW = "2_tb_long_term_foreigners_by_region"
Q_TBL = '"' + TBL_RAW + '"'

# load
if FILE.lower().endswith(".xlsx"):
    df = pd.read_excel(FILE)
else:
    df = pd.read_csv(FILE, encoding="utf-8-sig", low_memory=False)

con = sqlite3.connect(":memory:")
df.to_sql(TBL_RAW, con, index=False)

# SQL: 202504 기준 경기화성시의 연령대별 통계
sql = '''
SELECT
  TRIM("age") AS age,
  COALESCE(SUM(CAST("cnt" AS INT)), 0) AS cnt
FROM {Q_TBL}
WHERE REPLACE(REPLACE(REPLACE(TRIM("base_ym"), '-', ''), '_', ''), '.', '') = '202504'
  AND (UPPER(TRIM("sido")) = '경기' OR UPPER(TRIM("sido")) LIKE '경기%')
  AND (UPPER(TRIM("sigungu")) = '화성' OR UPPER(TRIM("sigungu")) LIKE '화성%')
GROUP BY TRIM("age")
ORDER BY TRIM("age")
'''.format(Q_TBL=Q_TBL)

out = pd.read_sql_query(sql, con)
print(out.to_csv(index=False))