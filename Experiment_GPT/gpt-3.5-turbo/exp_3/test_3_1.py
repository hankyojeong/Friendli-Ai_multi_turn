import sqlite3
import pandas as pd

# [S1] PRELUDE (payload 값 그대로; placeholder 금지)
FILE = r"3_외국인근로자.xlsx"
TBL_RAW = "3_tb_foreign_workers_permit"
Q_TBL   = '"' + TBL_RAW + '"'

# [S2] LOAD
import os
if not os.path.isabs(FILE) and not os.path.exists(FILE):
    for _p in [FILE, os.path.join("data", FILE), os.path.join("..","data",FILE),
               os.path.join("..", FILE), os.path.join("..","..","data",FILE)]:
        if os.path.exists(_p):
            FILE = _p; break

def _try_read(p):
    lo = p.lower()
    if lo.endswith((".xlsx",".xls")):
        try: return pd.read_excel(p)
        except Exception:
            csvp = os.path.splitext(p)[0]+".csv"
            if os.path.exists(csvp):
                return pd.read_csv(csvp, encoding="utf-8-sig", low_memory=False)
            raise
    return pd.read_csv(p, encoding="utf-8-sig", low_memory=False)

df = _try_read(FILE)
con = sqlite3.connect(":memory:")
df.to_sql(TBL_RAW, con, index=False)

# [S3] SQL —— 반드시 2단계(지연 포맷)
sql_template = '''
SELECT base_ym, SUM(cnt) as total_foreign_workers
FROM {Q_TBL}
GROUP BY base_ym
ORDER BY base_ym
'''
sql = sql_template.format(Q_TBL=Q_TBL)

out = pd.read_sql_query(sql, con)
print(out.to_csv(index=False))