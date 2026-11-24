"""Auto-generated topological anchor for Processor."""
from pathlib import Path

CURRENT_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_ROOT.parent
SANCTUARY_NAME = CURRENT_ROOT.name


def _resolve_next_sanctuary() -> str | None:
    arch_file = PROJECT_ROOT / "architecture.yml"
    if not arch_file.exists():
        return None
    current_target = None
    for raw_line in arch_file.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line.startswith("- name:"):
            current_target = line.split(":", 1)[1].strip().strip('"\'')
        elif current_target == SANCTUARY_NAME and line.startswith("next:"):
            val = line.split(":", 1)[1].strip().strip('"\'')
            return None if val in ("null", "None", "") else val
    return None


NEXT_SANCTUARY = _resolve_next_sanctuary()
NEXT_ROOT = (PROJECT_ROOT / NEXT_SANCTUARY) if NEXT_SANCTUARY else CURRENT_ROOT
