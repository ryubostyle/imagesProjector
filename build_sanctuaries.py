from pathlib import Path
import re


INIT_TEMPLATE = '''"""Auto-generated topological anchor for {name}."""
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
            current_target = line.split(":", 1)[1].strip().strip('"\\'')
        elif current_target == SANCTUARY_NAME and line.startswith("next:"):
            val = line.split(":", 1)[1].strip().strip('"\\'')
            return None if val in ("null", "None", "") else val
    return None


NEXT_SANCTUARY = _resolve_next_sanctuary()
NEXT_ROOT = (PROJECT_ROOT / NEXT_SANCTUARY) if NEXT_SANCTUARY else CURRENT_ROOT
'''


def parse_architecture(arch_path: Path) -> list[dict]:
    """PyYAMLが無くても動作する最小限の architecture.yml パーサー"""
    sanctuaries: list[dict] = []
    current: dict | None = None

    for raw_line in arch_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("- name:"):
            if current:
                sanctuaries.append(current)
            name = line.split(":", 1)[1].strip().strip("\"'")
            current = {"name": name, "subdirs": [], "next": None}
        elif current is not None:
            if line.startswith("subdirs:"):
                match = re.search(r"\[(.*?)\]", line)
                if match and match.group(1).strip():
                    current["subdirs"] = [
                        s.strip().strip("\"'") for s in match.group(1).split(",") if s.strip()
                    ]
            elif line.startswith("next:"):
                val = line.split(":", 1)[1].strip().strip("\"'")
                current["next"] = None if val in ("null", "None", "") else val

    if current:
        sanctuaries.append(current)
    return sanctuaries


def build_sanctuaries() -> None:
    root = Path(__file__).resolve().parent
    arch_path = root / "architecture.yml"

    if not arch_path.exists():
        raise FileNotFoundError(f"設計図が見つかりません: {arch_path}")

    sanctuaries = parse_architecture(arch_path)
    print(f"Building {len(sanctuaries)} sanctuaries from {arch_path.name}...")

    for s in sanctuaries:
        name = s["name"]
        s_dir = root / name
        s_dir.mkdir(parents=True, exist_ok=True)

        # 動的 __init__.py の配置（未作成の場合のみ書き込み、既存変更を保護）
        init_file = s_dir / "__init__.py"
        if not init_file.exists():
            init_file.write_text(INIT_TEMPLATE.format(name=name), encoding="utf-8")
            print(f"  [+] Created: {name}/__init__.py")
        else:
            print(f"  [=] Exists : {name}/__init__.py")

        # サブディレクトリと .gitkeep の作成
        for sub in s.get("subdirs", []):
            sub_dir = s_dir / sub
            sub_dir.mkdir(parents=True, exist_ok=True)
            gitkeep = sub_dir / ".gitkeep"
            if not gitkeep.exists():
                gitkeep.touch()
                print(f"  [+] Created: {name}/{sub}/.gitkeep")

    print("Done. Topological structure is ready.")


if __name__ == "__main__":
    build_sanctuaries()
