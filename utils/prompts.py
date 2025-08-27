import re
from pathlib import Path

_REPLACEMENTS = {
    "\u2026": "...",
    "\u201C": '"', "\u201D": '"',
    "\u2018": "'", "\u2019": "'",
}

def _read_prompt_text(prompt_dir: Path, n: int) -> str:
    cands = [f"Prompt{n}.txt", f"Promt{n}.txt", f"prompt{n}.txt", f"promt{n}.txt"]
    for name in cands:
        p = (prompt_dir / name)
        if p.exists():
            return p.read_text(encoding="utf-8-sig")
    raise FileNotFoundError(f"Prompt file not found for n={n} in {prompt_dir}")

def generate_system_prompt(payload: dict, prompt_dir: Path, prompt_file_no: int) -> str:
    raw = _read_prompt_text(prompt_dir, prompt_file_no)
    for k, v in _REPLACEMENTS.items():
        raw = raw.replace(k, v)
    def _sub_payload(m: re.Match) -> str:
        key = m.group(1)
        return str(payload.get(key, ""))
    # {payload["..."]} 또는 {payload['...']}만 치환 ({{Q_TBL}} 등은 보존)
    out = re.sub(r'\{payload\[\s*["\']([^"\']+)["\']\s*\]\}', _sub_payload, raw)
    return out
