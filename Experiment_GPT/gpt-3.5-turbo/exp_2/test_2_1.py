import sqlite3
import pandas as pd
FILE = "C:/Users/hanky/OneDrive/Desktop/서울대학교/IDEA 연구실/LLM/Friendli AI/data/2_장기체류외국인_지역별_현황.csv"
TBL_RAW = "2_tb_long_term_foreigners_by_region"
Q_TBL = '"' + TBL_RAW + '"'

# load
df = pd.read_csv(FILE, encoding="utf-8-sig", low_memory=False)
con = sqlite3.connect(":memory:")
df.to_sql(TBL_RAW, con, index=False)

# SQL: 2025년 4월, 경기 화성시의 장기체류 외국인 연령대 분포
sql = '''
SELECT
  TRIM("age") AS age_group,
  COALESCE(SUM(CAST("cnt" AS INT)), 0) AS foreigner_count
FROM {Q_TBL}
WHERE TRIM("base_ym") = '202504'
  AND (UPPER(TRIM("sido")) IN ('경기','경기도') OR UPPER(TRIM("sido")) LIKE '경기%')
  AND (UPPER(TRIM("sigungu")) IN ('화성','화성시') OR UPPER(TRIM("sigungu")) LIKE '화성%')
GROUP BY TRIM("age")
ORDER BY TRIM("age")
'''.format(Q_TBL=Q_TBL)

out = pd.read_sql_query(sql, con)
print(out.to_csv(index=False))