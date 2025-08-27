import io, re, json, traceback
from pathlib import Path
from contextlib import redirect_stdout

def _extract_python_code(text: str) -> str:
    if not text:
        return ""
    m = re.search(r"```python(.*)```", text, re.DOTALL | re.IGNORECASE)
    if m:
        return m.group(1).strip()
    m = re.search(r"```(.*)```", text, re.DOTALL)
    if m:
        return m.group(1).strip()
    return text.strip()

def _resolve_to_posix(relpath: str) -> tuple[str, bool]:
    """
    상대경로를 다음 우선순위로 탐색하여 존재하면 절대경로(포워드 슬래시)로 반환.
    1) <CWD>/data/<파일명>
    2) <CWD>/data/<상대경로>
    3) <CWD>/<상대경로>
    """
    cwd = Path.cwd()
    data_dir = cwd / "data"
    p = Path(relpath)

    candidates = []
    if p.is_absolute():
        candidates = [p]
    else:
        candidates = [
            data_dir / p.name,  # data/파일명
            data_dir / p,       # data/상대경로
            cwd / p,            # CWD/상대경로
        ]

    for c in candidates:
        if c.exists():
            return c.resolve().as_posix(), True
    return relpath, False

def _rewrite_FILE_assignments(code: str) -> str:
    """
    코드 내 FILE = "..." 또는 '...' 대입을 찾아 data/에서 절대경로로 치환.
    다른 변수명은 건드리지 않음.
    """
    def _repl(m: re.Match) -> str:
        rel = m.group(2)
        abs_posix, ok = _resolve_to_posix(rel)
        if ok:
            print(f"[DATA PATH RESOLVED] FILE -> {abs_posix}")
            return f'FILE = "{abs_posix}"'
        else:
            # 못 찾으면 원본 유지(실행 시 에러 출력됨)
            print(
                "[DATA NOT FOUND] Tried:",
                (Path.cwd() / "data" / Path(rel).name).as_posix(), ",",
                (Path.cwd() / "data" / rel).as_posix(), ",",
                (Path.cwd() / rel).as_posix()
            )
            return m.group(0)

    # FILE = "..." 패턴 전부 치환
    return re.sub(
        r'^\s*FILE\s*=\s*([\'"])([^\'"]+)\1\s*$',
        _repl,
        code,
        flags=re.MULTILINE
    )

def save_and_exec_from_llm(llm_answer: str, outfile: str):
    """
    ```python ...``` 코드블록 추출 → FILE 경로 절대화 → 저장 → 실행(stdout 캡처).
    """
    code = _extract_python_code(llm_answer)

    # 1) FILE 경로 절대화(프로젝트 data/ 탐색)
    try:
        code = _rewrite_FILE_assignments(code)
    except Exception as e:
        print(f"[WARN] FILE path rewrite failed: {e}")

    # 2) 저장
    out_path = Path(outfile).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(code, encoding="utf-8")
    print(f"[SAVED] {out_path}")

    # 3) 실행
    g = {"__name__": "__main__", "__file__": str(out_path)}
    buf = io.StringIO()
    try:
        with redirect_stdout(buf):
            try:
                exec(compile(code, filename=str(out_path), mode="exec"), g, g)
            except Exception:
                print("[EXEC ERROR]")
                traceback.print_exc()
    finally:
        pass

    stdout = buf.getvalue().strip()
    print(stdout if stdout else "[INFO] 코드가 출력하지 않았습니다.")
    return str(out_path), stdout
