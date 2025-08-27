# 1_국내체류외국인.xlsx
payload_1_1 = {
    "file_name": "1_국내체류외국인.xlsx",
    "table_name": "1_tb_resident_foreigners",
    "description": "국내 체류하고 있는 외국인을 단기체류, 등록외국인, 외국국적동포_거소신고의 3개 카테고리로 구분하고, 각 카테고리별 외국인 수를 월별로 집계한 데이터",
    "meta_description": """
schema:
  category: str   # {'단기체류','장기체류거소','장기체류등록'}
  cnt: int        # 인원수
  p_year: int     # 예: 2022, 2023, 2024, 2025
  p_month: int    # 1~12

value_alias:
  # 질문/사용자 표현을 실제 값으로 정규화
  장기체류: ['장기체류거소','장기체류등록']   # 합산 대상으로 해석
  등록외국인: ['장기체류등록']
  외국국적동포_거소신고: ['장기체류거소']

policies:
  categories_disjoint: true        # 서로 겹치지 않음 → 합산 안전
  long_term_policy: sum            # alias가 다수이면 SUM으로 집계
  time_order: ['p_year','p_month'] # 시계열 정렬 기준

notes:
  - 숫자/특수문자로 시작하는 식별자는 SQLite에서 "..."로 인용
  - dtype 강제: cnt,p_year,p_month는 숫자형으로 캐스팅 후 사용
""",
    "user_question": "2025년 4월 기준 국내 단기 체류 외국인 수는?"
}
payload_1_2 = { **payload_1_1, "user_question": "2023년 7월 기준 국내 단기 체류 외국인 수는?" }
payload_1_3 = { **payload_1_1, "user_question": "2024년 이후 월별 장기체류 외국인수 추이는?" }
payload_1_4 = { **payload_1_1, "user_question": "2023년 월별 장기체류 외국인수 추이는?" }
payload_1_5 = { **payload_1_1, "user_question": "2023~2025년 3년간 3월 장기체류 외국인 수와 전년 대비 증감률은?" }
payload_1_6 = { **payload_1_1, "user_question": "2023~2025년 3년간 1월 장기체류 외국인 수와 전년 대비 증감률은?" }

# 2_장기체류외국인_지역별_현황.csv
payload_2_1 = {
    "file_name": "2_장기체류외국인_지역별_현황.csv",
    "table_name": "2_tb_long_term_foreigners_by_region",
    "description": "장기체류 외국인 중 등록외국인과 외국국적동포의 거소현황을 집계한 데이터. table_nm 컬럼을 기준으로 국적(1), 체류자격(2), 행정동(3), 연령대(4)로 구분되어 있음.",
    "meta_description": """
- table_nm: 원본 테이블명 (문자형) (데이터 구분용: 1.국적, 2.체류자격, 3.행정동, 4.연령대)
- sido: 시도 (문자형)
- sigungu: 시군구 (문자형)
- adong: 행정동 (문자형)
- gender: 성별 (문자형)
- age: 나이 (문자형)
- cert: 체류자격 (문자형)
- nat_nm: 국적 (문자형)
- cnt: 외국인 수 (정수형)
- base_ym: 기준년월 (문자형)
- gbn: 장기체류구분 (문자형)

value_alias:
  sido:
    경기: ['경기도', '경기']
  sigungu:
    화성: ['화성시', '화성']
  gbn:
    거소외국인: ['외국국적동포']
    등록외국인: ['등록외국인']
  age:
    age value들을보고 '0~9세', '10~19세', ..., '70~79세', '80세이상' 으로 알아서 재 분류.     

policies:
  region_match: use_upper_trim
  table_nm_age: '4'
""",
    "user_question": "2025년 4월 경기 화성시의 장기체류 외국인 연령대 분포?"
}


# 3_외국인근로자.xlsx
payload_3_1 = {
    "file_name": "3_외국인근로자.xlsx",
    "table_name": "3_tb_foreign_workers_permit",
    "description": "비전문취업(E-9) 비자를 가진 외국인 근로자의 업종/지역별 분포를 분기별로 집계한 데이터",
    "meta_description": """
- base_ym: 기준년월 (문자형)
- sido: 시도 (문자형)
- upjong: 업종 (문자형)
- cnt: 외국인 수 (정수형)

base_is_quarterly: true
quarter_policy: repeat_each_month
quarter_map:
  1Q: ['01','02','03']
  2Q: ['04','05','06']
  3Q: ['07','08','09']
  4Q: ['10','11','12']
""",
    "user_question": "(E-9)국내 외국인 근로자의 월별 추이는?"
}
