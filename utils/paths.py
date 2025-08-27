from pathlib import Path
from typing import Optional, Union

def get_out_dirs(exp_root_dir: Path, exp_no: Optional[int], *, reuse: bool = False):
    """
    exp_root_dir/exp_{n} 디렉토리를 반환.
    - reuse=False (기본): 존재하지 않는 번호를 찾아 새 exp_{n} 생성 (자동 증가)
    - reuse=True : 주어진 n의 exp_{n}을 그대로 사용(존재하면 재사용)
    """
    n = int(exp_no or 1)

    if reuse:
        out_dir = exp_root_dir / f"exp_{n}"
    else:
        out_dir = exp_root_dir / f"exp_{n}"
        while out_dir.exists():
            n += 1
            out_dir = exp_root_dir / f"exp_{n}"

    log_dir = out_dir / "Log"
    out_dir.mkdir(parents=True, exist_ok=True)
    log_dir.mkdir(parents=True, exist_ok=True)

    print(f"[EXP] Using {out_dir}")
    return out_dir, log_dir, n

def ensure_dir(p: Union[Path, str]) -> Path:
    p = Path(p)
    p.mkdir(parents=True, exist_ok=True)
    return p