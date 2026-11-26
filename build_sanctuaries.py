from pathlib import Path
from typing import Any, Dict, List
import yaml


def load_architecture(arch_path: Path = Path("architecture.yml")) -> Dict[str, Any]:
    """architecture.yml を読み込む"""
    if not arch_path.exists():
        raise FileNotFoundError(f"設計図が見つかりません: {arch_path}")
    with arch_path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def render_init_content(name: str, index: int, next_name: str, role: str) -> str:
    """各聖域の __init__.py に書き込むトポロジ定義コードを生成する"""
    return (
        f'"""\n'
        f"Sanctuary: {name} (Level {index})\n"
        f"Role: {role}\n"
        f"Auto-synced by build_sanctuaries.py from architecture.yml\n"
        f'"""\n\n'
        f'SANCTUARY_NAME = "{name}"\n'
        f"SANCTUARY_INDEX = {index}\n"
        f'NEXT_SANCTUARY = "{next_name}"\n\n'
        f'__all__ = ["SANCTUARY_NAME", "SANCTUARY_INDEX", "NEXT_SANCTUARY"]\n'
    )


def build_sanctuaries(arch: Dict[str, Any]) -> None:
    """設計図に基づき、4つの聖域ディレクトリ・サブディレクトリ・__init__.pyを構築する"""
    sanctuaries: List[Dict[str, Any]] = arch.get("sanctuaries", [])
    if not sanctuaries:
        print("[Builder] 警告: architecture.yml に sanctuaries が定義されていません。")
        return

    total = len(sanctuaries)
    print(f"=== [build_sanctuaries] {total}つの聖域の物質化・同期を開始 ===")

    for i, s in enumerate(sanctuaries):
        name: str = s["name"]
        index: int = s.get("index", i)
        role: str = s.get("role", "")
        subdirs: List[str] = s.get("subdirs", [])
        # 円環トポロジ（最後の聖域は最初の Chaos へ戻る）
        next_name: str = sanctuaries[(i + 1) % total]["name"]

        sanctuary_dir = Path(name)
        sanctuary_dir.mkdir(parents=True, exist_ok=True)

        # 1. __init__.py のトポロジ同期
        init_path = sanctuary_dir / "__init__.py"
        init_content = render_init_content(name, index, next_name, role)
        init_path.write_text(init_content, encoding="utf-8")
        print(f"  [Sync] {init_path} (NEXT -> {next_name})")

        # 2. サブディレクトリの生成と .gitkeep 配置
        for sub in subdirs:
            sub_path = sanctuary_dir / sub
            sub_path.mkdir(parents=True, exist_ok=True)
            gitkeep = sub_path / ".gitkeep"
            if not gitkeep.exists():
                gitkeep.touch()
            print(f"  [Dir ] {sub_path}/ 準備完了")

        # 3. 基底モジュールの存在確認（既存実装は絶対に上書きしない）
        base_module = s.get("base_module")
        if base_module:
            base_path = Path(base_module)
            if base_path.exists():
                print(f"  [Safe] {base_path} は既存実装を保護しました")
            else:
                print(f"  [Warn] {base_path} が未配置です")

    print("=== [build_sanctuaries] 全聖域の同期完了 ===")


if __name__ == "__main__":
    architecture = load_architecture()
    build_sanctuaries(architecture)
