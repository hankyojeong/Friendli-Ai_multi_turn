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

# SQL: 202504 기준 경기 화성시, table_nm=4(연령대)인 데이터의 연령대별 합계
sql = '''
SELECT
  CASE
    WHEN "age" BETWEEN '0' AND '9' THEN '0~9세'
    WHEN "age" BETWEEN '10' AND '19' THEN '10~19세'
    WHEN "age" BETWEEN '20' AND '29' THEN '20~29세'
    WHEN "age" BETWEEN '30' AND '39' THEN '30~39세'
    WHEN "age" BETWEEN '40' AND '49' THEN '40~49세'
    WHEN "age" BETWEEN '50' AND '59' THEN '50~59세'
    WHEN "age" BETWEEN '60' AND '69' THEN '60~69세'
    WHEN "age" BETWEEN '70' AND '79' THEN '70~79세'
    WHEN "age" >= '80' THEN '80세이상'
    ELSE '기타'
  END AS age_range,
  COALESCE(SUM(CAST("cnt" AS INT)), 0) AS cnt
FROM {Q_TBL}
WHERE UPPER(TRIM("table_nm")) = '4'
  AND (
    UPPER(TRIM("sido")) IN ('경기','경기도') OR 
    UPPER(TRIM("sido")) LIKE '경기%'
  )
  AND (
    UPPER(TRIM("sigungu")) IN ('화성','화성시') OR 
    UPPER(TRIM("sigungu")) LIKE '화성%'
  )
  AND REPLACE(REPLACE(REPLACE(TRIM("base_ym"),'-',''),'_',''),'.','') = '202504'
GROUP BY age_range
ORDER BY 
  CASE age_range
    WHEN '0~9세' THEN 1
    WHEN '10~19세' THEN 2
    WHEN '20~29세' THEN 3
    WHEN '30~39세' THEN 4
    WHEN '40~49세' THEN 5
    WHEN '50~59세' THEN 6
    WHEN '60~69세' THEN 7
    WHEN '70~79세' THEN 8
    WHEN '80세이상' THEN 9
    ELSE 10
  END
'''.format(Q_TBL=Q_TBL)

out = pd.read_sql_query(sql, con)
print(out.to_csv(index=False))