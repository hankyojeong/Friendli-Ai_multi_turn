from pathlib import Path
import payloads as PL
from utils import make_client, run_all_payloads, run_single_payload

# 설정
MODEL = "Qwen/Qwen3-32B"
PROMPT_DIR = Path("system_prompt")
PROMPT_FILE_NO = 3
EXP_ROOT_DIR = Path(r"C:\Users\hanky\OneDrive\Desktop\서울대학교\IDEA 연구실\LLM\Friendli AI\Experiment_Qwen\Qwen3-32B")

# 환경변수 FRIENDLI_API_KEY / FRIENDLI_TEAM_ID 사용 권장
client = make_client(api_key="flp_RevIxEFxsulZASUQ2pxyioWev5YI3lJ0bn7ZarCqSWZM80", team_id="l9h8CAleMYvh")

def _resolve_prompt_path(prompt_dir: Path, n: int):
    for name in (f"Promt{n}.txt", f"Prompt{n}.txt", f"promt{n}.txt", f"prompt{n}.txt"):
        p = prompt_dir / name
        if p.exists():
            return p
    return None

_prompt_path = _resolve_prompt_path(PROMPT_DIR, PROMPT_FILE_NO)

print(f"[BOOT] Model: {MODEL}")  # 사용 모델 출력 / Using model
if _prompt_path:
    print(f"[BOOT] Prompt: {_prompt_path.name} ({_prompt_path.resolve()})")  # 사용 프롬프트 파일
else:
    print(f"[BOOT] Prompt: NOT FOUND (number={PROMPT_FILE_NO}, dir={PROMPT_DIR.resolve()})")
print(f"[BOOT] EXP root: {EXP_ROOT_DIR.resolve()}")

# ===== 2) 전체 실행 =====
run_all_payloads(
    namespace=PL.__dict__,
    client=client,
    model=MODEL,
    prompt_dir=PROMPT_DIR,
    prompt_file_no=PROMPT_FILE_NO,
    exp_root_dir=EXP_ROOT_DIR,
)

# ===== 3) 단일 실행 예시 =====
# run_single_payload_direct(
#     "payload_1_4",
#     namespace=PL.__dict__,
#     client=client,
#     model=MODEL,
#     prompt_dir=PROMPT_DIR,
#     prompt_file_no=PROMPT_FILE_NO,
#     exp_root_dir=EXP_ROOT_DIR,
#     output_prefix="test_1_4_try1",  # 옵션
# )