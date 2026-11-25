"""
imagesProjector - Sanctuary Builder & Topology Synchronizer
architecture.yml を読み込み、以下の責務を安全に執行する:
  1. 各聖域のディレクトリと __init__.py（位相接続トポロジ）を常に最新へ同期する
  2. base_*.py および main.py は「未存在時のみ生成」かつ「マジックコメント保護」により上書きを完全に防止する
"""
from datetime import datetime
from pathlib import Path
import sys
from typing import Any, Dict, List
from zoneinfo import ZoneInfo

try:
    import yaml
except ImportError as exc:
    print("❌ [Error] PyYAML is required. Install via `pip install pyyaml`.", file=sys.stderr)
    raise SystemExit(1) from exc

PROJECT_ROOT = Path(__file__).resolve().parent
ARCH_FILE = PROJECT_ROOT / "architecture.yml"
TIMEZONE = "Asia/Tokyo"

# このマーカーが先頭にあるファイルのみ「自動生成された初期雛形」とみなす
AUTO_GEN_MARKER = "# @auto-generated-stub: imagesProjector"

DEFAULT_SANCTUARIES = [
    "Chaos",
    "Entropy",
    "Processor",
    "StrataCrystallization",
]


def load_architecture(arch_path: Path) -> Dict[str, Any]:
    """architecture.yml を安全に読み込む"""
    if not arch_path.exists():
        print(f"⚠️  [Warning] {arch_path.name} not found. Using default 4-sanctuary topology.")
        return {"sanctuaries": DEFAULT_SANCTUARIES}

    raw_data = yaml.safe_load(arch_path.read_text(encoding="utf-8"))
    return raw_data if isinstance(raw_data, dict) else {}


def extract_sanctuary_names(arch_data: Dict[str, Any]) -> List[str]:
    """
    architecture.yml の多様な記述形式（list / dict / cascade_order）から
    聖域名の順序リストを抽出する。
    """
    if isinstance(arch_data.get("cascade_order"), list):
        return [str(x) for x in arch_data["cascade_order"]]

    raw_sanctuaries = arch_data.get("sanctuaries")
    if isinstance(raw_sanctuaries, list):
        names = []
        for item in raw_sanctuaries:
            if isinstance(item, str):
                names.append(item)
            elif isinstance(item, dict) and "name" in item:
                names.append(str(item["name"]))
        if names:
            return names
    elif isinstance(raw_sanctuaries, dict) and raw_sanctuaries:
        return [str(k) for k in raw_sanctuaries.keys()]

    return DEFAULT_SANCTUARIES


def base_filename_for(sanctuary_name: str) -> str:
    """
    聖域名に対応する基底クラスファイル名を解決する。
    StrataCrystallization -> base_strata.py
    その他 (Chaos, Entropy, Processor) -> base_<lower>.py
    """
    if sanctuary_name == "StrataCrystallization":
        return "base_strata.py"
    return f"base_{sanctuary_name.lower()}.py"


def sync_topology_file(target_path: Path, content: str) -> None:
    """
    __init__.py などの「構造の器（トポロジ）」を最新状態へ同期する（内容に変化がある場合のみ書き込み）。
    """
    target_path.parent.mkdir(parents=True, exist_ok=True)
    if target_path.exists() and target_path.read_text(encoding="utf-8") == content:
        print(f"✨ [Topology Unchanged] {target_path.relative_to(PROJECT_ROOT)}")
        return

    target_path.write_text(content, encoding="utf-8")
    print(f"🔄 [Topology Synced]    {target_path.relative_to(PROJECT_ROOT)}")


def write_protected_file(target_path: Path, stub_content: str) -> None:
    """
    main.py や base_*.py などの「生きた実装」を保護する。
    - ファイルが存在しない場合のみ初期雛形を作成する。
    - すでにファイルが存在する場合は（マーカーの有無を問わず）一切上書きしない。
    """
    target_path.parent.mkdir(parents=True, exist_ok=True)

    if target_path.exists():
        head = target_path.read_text(encoding="utf-8")[:120]
        status = "Stub Preserved" if AUTO_GEN_MARKER in head else "Custom Code Locked"
        print(f"🛡️  [{status}] {target_path.relative_to(PROJECT_ROOT)}")
        return

    full_stub = f"{AUTO_GEN_MARKER}\n{stub_content}"
    target_path.write_text(full_stub, encoding="utf-8")
    print(f"🌱 [Stub Created]       {target_path.relative_to(PROJECT_ROOT)}")


def build_sanctuaries() -> int:
    now_str = datetime.now(ZoneInfo(TIMEZONE)).strftime("%Y.%m.%d.%H%M")
    print(f"=== build_sanctuaries.py ({now_str} {TIMEZONE}) ===")

    arch_data = load_architecture(ARCH_FILE)
    sanctuaries = extract_sanctuary_names(arch_data)
    total = len(sanctuaries)

    if total == 0:
        print("❌ [Error] No sanctuaries defined.", file=sys.stderr)
        return 1

    # 1. 各聖域のディレクトリ・__init__.py（同期）・base_*.py（保護）を構築
    for idx, name in enumerate(sanctuaries):
        next_name = sanctuaries[(idx + 1) % total]
        sanctuary_dir = PROJECT_ROOT / name

        # (A) __init__.py は architecture.yml と常に同期
        init_content = (
            f'"""Auto-generated sanctuary topology from architecture.yml."""\n'
            f'SANCTUARY_NAME = "{name}"\n'
            f'SANCTUARY_INDEX = {idx}\n'
            f'NEXT_SANCTUARY = "{next_name}"\n'
            f'__all__ = ["SANCTUARY_NAME", "SANCTUARY_INDEX", "NEXT_SANCTUARY"]\n'
        )
        sync_topology_file(sanctuary_dir / "__init__.py", init_content)

        # (B) base_*.py は既存ファイルを上書きしない
        base_file = sanctuary_dir / base_filename_for(name)
        base_stub = (
            f'"""Base class definition for {name} sanctuary."""\n'
            f"# TODO: Implement Base{name} here. This file is protected from overwriting.\n"
        )
        write_protected_file(base_file, base_stub)

    # 2. 第4の零点 main.py も既存ファイルを上書きしない
    main_stub = (
        '"""Entry point for imagesProjector autonomous circulation."""\n'
        "import importlib\n\n"
        f"CASCADE_ORDER = {sanctuaries!r}\n\n"
        "if __name__ == '__main__':\n"
        "    for s in CASCADE_ORDER:\n"
        "        mod = importlib.import_module(s)\n"
        "        print(f'[Sanctuary] {mod.SANCTUARY_NAME} -> next: {mod.NEXT_SANCTUARY}')\n"
    )
    write_protected_file(PROJECT_ROOT / "main.py", main_stub)

    print("✅ Build & protection check complete.")
    return 0


if __name__ == "__main__":
    sys.exit(build_sanctuaries())
