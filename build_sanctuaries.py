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


MAIN_TEMPLATE = '''"""Auto-generated autonomous circulation entry point from architecture.yml."""
from datetime import datetime
import importlib
from pathlib import Path
from zoneinfo import ZoneInfo

SYSTEM_NAME = {system_name!r}
TIMEZONE = {timezone!r}
CASCADE_ORDER = {cascade_order!r}
PROJECT_ROOT = Path(__file__).resolve().parent


def verify_topology() -> None:
    """architecture.yml から生成された各聖域の __init__.py 経路を検証する"""
    print(f"=== {{SYSTEM_NAME}} ===")
    print(f"Timestamp ({{TIMEZONE}}): {{datetime.now(ZoneInfo(TIMEZONE)).strftime('%Y.%m.%d.%H%M')}}")
    print("-" * 52)
    for name in CASCADE_ORDER:
        mod = importlib.import_module(name)
        print(f"  [Sanctuary] {{mod.SANCTUARY_NAME:<22}} -> next: {{mod.NEXT_SANCTUARY}}")
    print("-" * 52)


def run_cycle() -> None:
    """三位一体の循環サイクルを起動する（未実装時はトポロジ検証モードで動作）"""
    verify_topology()

    try:
        from Processor.base_processor import BaseProcessor
    except ImportError:
        print("[Info] 基底クラスがまだ未配置のため、トポロジ接続テストのみ完了しました。")
        print("       次は Chaos / Entropy / Processor の各基底クラスを実装してください。")
        return

    processor = BaseProcessor()
    processor.orchestrate_cycle()


if __name__ == "__main__":
    run_cycle()
'''


def parse_architecture(arch_path: Path) -> dict:
    """PyYAMLが無くても動作する最小限の architecture.yml パーサー"""
    meta = {
        "system": "imagesProjector",
        "timezone": "Asia/Tokyo",
        "sanctuaries": [],
    }
    current: dict | None = None

    for raw_line in arch_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("system:"):
            meta["system"] = line.split(":", 1)[1].strip().strip("\"'")
        elif line.startswith("timezone:"):
            meta["timezone"] = line.split(":", 1)[1].strip().strip("\"'")
        elif line.startswith("- name:"):
            if current:
                meta["sanctuaries"].append(current)
            name = line.split(":", 1)[1].strip().strip("\"'")
            current = {"name": name, "level": len(meta["sanctuaries"]), "subdirs": [], "next": None}
        elif current is not None:
            if line.startswith("level:"):
                current["level"] = int(line.split(":", 1)[1].strip())
            elif line.startswith("subdirs:"):
                match = re.search(r"\[(.*?)\]", line)
                if match and match.group(1).strip():
                    current["subdirs"] = [
                        s.strip().strip("\"'") for s in match.group(1).split(",") if s.strip()
                    ]
            elif line.startswith("next:"):
                val = line.split(":", 1)[1].strip().strip("\"'")
                current["next"] = None if val in ("null", "None", "") else val

    if current:
        meta["sanctuaries"].append(current)

    meta["sanctuaries"].sort(key=lambda x: x["level"])
    return meta


def build_sanctuaries() -> None:
    root = Path(__file__).resolve().parent
    arch_path = root / "architecture.yml"

    if not arch_path.exists():
        raise FileNotFoundError(f"設計図が見つかりません: {arch_path}")

    arch = parse_architecture(arch_path)
    sanctuaries = arch["sanctuaries"]
    print(f"Building {len(sanctuaries)} sanctuaries from {arch_path.name}...")

    for s in sanctuaries:
        name = s["name"]
        s_dir = root / name
        s_dir.mkdir(parents=True, exist_ok=True)

        init_file = s_dir / "__init__.py"
        if not init_file.exists():
            init_file.write_text(INIT_TEMPLATE.format(name=name), encoding="utf-8")
            print(f"  [+] Created: {name}/__init__.py")
        else:
            print(f"  [=] Exists : {name}/__init__.py")

        for sub in s.get("subdirs", []):
            sub_dir = s_dir / sub
            sub_dir.mkdir(parents=True, exist_ok=True)
            gitkeep = sub_dir / ".gitkeep"
            if not gitkeep.exists():
                gitkeep.touch()
                print(f"  [+] Created: {name}/{sub}/.gitkeep")

    # main.py の自動生成（未作成の場合のみ書き込み）
    main_file = root / "main.py"
    if not main_file.exists():
        cascade_order = [s["name"] for s in sanctuaries]
        main_code = MAIN_TEMPLATE.format(
            system_name=arch["system"],
            timezone=arch["timezone"],
            cascade_order=cascade_order,
        )
        main_file.write_text(main_code, encoding="utf-8")
        print("  [+] Created: main.py")
    else:
        print("  [=] Exists : main.py")

    print("Done. Topological structure and main.py are ready.")


if __name__ == "__main__":
    build_sanctuaries()
