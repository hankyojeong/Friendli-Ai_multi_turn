import re, json, pandas as pd
from pathlib import Path
from .llm_client import call_llm
from .exec_utils import save_and_exec_from_llm
from .prompts import generate_system_prompt
from .paths import get_out_dirs
from typing import Optional

def _collect_payload_keys(namespace: dict) -> list[str]:
    keys = [k for k in namespace.keys() if re.fullmatch(r'payload_\d+(?:_\d+)?', k)]
    keys.sort(key=lambda s: tuple(map(int, s.split('_')[1:])))
    if not keys:
        raise RuntimeError("No payloads found (expected names like payload_1, payload_1_2, ...)")
    return keys

def _test_stem_from_varname(varname: str) -> str:
    return "test_" + varname.replace("payload_", "", 1)

def run_single_payload(
    varname: str,
    *,
    namespace: dict,
    client,
    model: str,
    prompt_dir,
    prompt_file_no: int,
    exp_root_dir,
    output_prefix: Optional[str] = None,
    max_tokens: int = 4096,
    fixed_out_dir=None,
    fixed_log_dir=None,
    multi_turn: bool = False,
):
    if fixed_out_dir is not None and fixed_log_dir is not None:
        out_dir, log_dir = fixed_out_dir, fixed_log_dir
    else:
        # ★ 단일 실행도 새 번호 자동 생성
        out_dir, log_dir, _ = get_out_dirs(exp_root_dir, prompt_file_no, reuse=False)

    payload = namespace[varname]
    qno = varname.replace("payload_", "", 1)
    test_stem = output_prefix or _test_stem_from_varname(varname)

    print(f"[RUN] Multi-turn mode: {multi_turn}")

    # 1) LLM 호출
    prompt = generate_system_prompt(payload, prompt_dir, prompt_file_no)
    chat = payload["user_question"]
    llm_answer = call_llm(
        client,
        model,
        prompt,
        chat,
        max_tokens=max_tokens,
        multi_turn=multi_turn,
    )

    # 2) 저장 & 실행
    py_path, run_stdout = save_and_exec_from_llm(llm_answer, str(out_dir / f"{test_stem}.py"))

    # 3) JSON 저장
    out_json = {
        "question": chat,
        "llm_answer": llm_answer,
        "system_prompt": prompt,
        "_runtime": {"py_path": py_path, "stdout": run_stdout},
        "_payload_var": varname,
    }
    json_path = out_dir / f"{test_stem}.json"
    json_path.write_text(json.dumps(out_json, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[JSON SAVED] {json_path.resolve()}")

    # 4) CSV append (같은 exp 폴더 하나에 계속 누적)
    row = {
        "question_no": qno,
        "question": chat,
        "sys_prompt_no": str(prompt_file_no),
        "output": run_stdout,
        "llm_answer": llm_answer,
        "정답유무": "",
    }
    csv_path = out_dir / "results.csv"
    df = pd.DataFrame([row], columns=["question_no","question","sys_prompt_no","output","llm_answer","정답유무"])
    if csv_path.exists():
        df.to_csv(csv_path, index=False, encoding="utf-8-sig", mode="a", header=False)
    else:
        df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    print(f"[CSV UPDATED] {csv_path.resolve()}")

    return {
        "payload_var": varname,
        "py_path": str(Path(py_path).resolve()),
        "json_path": str(json_path.resolve()),
        "stdout": run_stdout,
        "llm_answer": llm_answer,
        "system_prompt": prompt,
        "exp_dir": str(out_dir.resolve()),
    }

def run_all_payloads(
    *,
    namespace: dict,
    client,
    model: str,
    prompt_dir,
    prompt_file_no: int,
    exp_root_dir,
    max_tokens: int = 4096,
    multi_turn: bool = False,
):
    results = []
    out_dir, log_dir, _ = get_out_dirs(exp_root_dir, prompt_file_no, reuse=False)

    print(f"[RUN-ALL] Multi-turn mode: {multi_turn}")

    for k in _collect_payload_keys(namespace):
        try:
            r = run_single_payload(
                k,
                namespace=namespace,
                client=client,
                model=model,
                prompt_dir=prompt_dir,
                prompt_file_no=prompt_file_no,
                exp_root_dir=exp_root_dir,
                max_tokens=max_tokens,
                fixed_out_dir=out_dir,
                fixed_log_dir=log_dir,
                multi_turn=multi_turn,
            )
            results.append(r)
        except Exception as e:
            results.append({"payload_var": k, "error": repr(e)})
    return results