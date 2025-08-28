from pathlib import Path
import os
import json
import payloads as PL
from utils import run_all_payloads, run_single_payload
from openai import OpenAI

# 설정 
MODEL = "gpt-3.5-turbo"
PROMPT_DIR = Path("system_prompt")
PROMPT_FILE_NO = 3
EXP_ROOT_DIR = Path(r"C:\Users\hanky\OneDrive\문서\GitHub\Friendli-Ai_multi_turn\Experiment_GPT\gpt-3.5-turbo")

# 환경변수 OPENAI_API_KEY 권장
client = OpenAI(api_key="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")


def _load_multi_turn():
    cfg_path = Path("config.json")
    if cfg_path.exists():
        try:
            cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
            return bool(cfg.get("multi_turn", False))
        except Exception:
            pass
    ans = input("Enable multi-turn? [y/N]: ")
    return ans.strip().lower() in {"y", "yes"}


MULTI_TURN = _load_multi_turn()

def _resolve_prompt_path(prompt_dir: Path, n: int):
    for name in (f"Promt{n}.txt", f"Prompt{n}.txt", f"promt{n}.txt", f"prompt{n}.txt"):
        p = prompt_dir / name
        if p.exists():
            return p
    return None

_prompt_path = _resolve_prompt_path(PROMPT_DIR, PROMPT_FILE_NO)

print(f"[BOOT] Model: {MODEL}")
if _prompt_path:
    print(f"[BOOT] Prompt: {_prompt_path.name} ({_prompt_path.resolve()})")
else:
    print(f"[BOOT] Prompt: NOT FOUND (number={PROMPT_FILE_NO}, dir={PROMPT_DIR.resolve()})")
print(f"[BOOT] EXP root: {EXP_ROOT_DIR.resolve()}")
print(f"[BOOT] Multi-turn: {MULTI_TURN}")

# ===== 전체 실행 =====
run_all_payloads(
    namespace=PL.__dict__,
    client=client,
    model=MODEL,
    prompt_dir=PROMPT_DIR,
    prompt_file_no=PROMPT_FILE_NO,
    exp_root_dir=EXP_ROOT_DIR,
    multi_turn=MULTI_TURN,
)

# ===== 단일 실행 예시 =====
# run_single_payload(
#     "payload_1_4",
#     namespace=PL.__dict__,
#     client=client,
#     model=MODEL,
#     prompt_dir=PROMPT_DIR,
#     prompt_file_no=PROMPT_FILE_NO,
#     exp_root_dir=EXP_ROOT_DIR,
#     output_prefix="test_1_4_try1",
#     multi_turn=MULTI_TURN,
# )
