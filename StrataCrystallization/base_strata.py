from abc import ABC, abstractmethod
from datetime import datetime, timezone, timedelta
import json
from pathlib import Path
from typing import Any, Dict, Optional
import yaml

JST = timezone(timedelta(hours=9))


class BaseStrata(ABC):
    """[Level 3: 地層・骨格] 結晶化したアートと年代記を永続化し、次期シードを発掘する基底クラス"""

    def __init__(
        self,
        sanctuary_name: str = "StrataCrystallization",
        strata_dir: str = "StrataCrystallization/layers",
    ) -> None:
        self.sanctuary_name = sanctuary_name
        self.strata_dir = Path(strata_dir)
        self._ensure_bedrock()

    def _ensure_bedrock(self) -> None:
        """地層ディレクトリが存在しない場合は基盤を作成する"""
        self.strata_dir.mkdir(parents=True, exist_ok=True)

    def _generate_chronicle_name(self, ext: str) -> str:
        """JSTタイムスタンプに基づく地層ファイル名を生成する (例: Strata.2026.11.26.110000.yml)"""
        now_jst = datetime.now(JST)
        return f"Strata.{now_jst.strftime('%Y.%m.%d.%H%M%S')}.{ext}"

    @abstractmethod
    def format_fossil(self, artifact: Dict[str, Any]) -> str:
        """成果物（artifact）を人間が読める年代記Markdown文字列へ整形する"""
        raise NotImplementedError

    def crystallize(self, processor_packet: Dict[str, Any]) -> Dict[str, Any]:
        """Processorからの結晶化パケットを受け取り、Markdown年代記とYAMLシードをペアで沈殿させる"""
        if processor_packet.get("phase") != "ready_for_strata":
            return {
                "origin": self.sanctuary_name,
                "phase": "rejected_by_strata",
                "reason": "Packet is not ready for crystallization",
            }

        artifact = processor_packet.get("artifact", {})
        md_filename = self._generate_chronicle_name("md")
        yml_filename = self._generate_chronicle_name("yml")

        md_path = self.strata_dir / md_filename
        yml_path = self.strata_dir / yml_filename

        # 1. 人間用年代記（Markdown）の保存
        fossil_md = self.format_fossil(artifact)
        md_path.write_text(fossil_md, encoding="utf-8")

        # 2. 次期循環用シード（YAML）の保存
        strata_record = {
            "metadata": {
                "sanctuary": self.sanctuary_name,
                "crystallized_at": processor_packet.get(
                    "crystallized_at", datetime.now(JST).isoformat()
                ),
            },
            "chronicle_file": md_filename,
            "artifact": artifact,
        }

        with yml_path.open("w", encoding="utf-8") as f:
            yaml.safe_dump(
                strata_record,
                f,
                allow_unicode=True,
                sort_keys=False,
            )

        return {
            "origin": self.sanctuary_name,
            "phase": "crystallized",
            "chronicle_file": str(md_path),
            "seed_file": str(yml_path),
        }

    def excavate_latest_seed(self) -> Optional[Dict[str, Any]]:
        """最新の地層ファイル（.yml / .yaml / 互換用 .json）を発掘して次サイクルへ渡す"""
        if not self.strata_dir.exists():
            return None

        strata_files = sorted(
            list(self.strata_dir.glob("Strata.*.yml"))
            + list(self.strata_dir.glob("Strata.*.yaml"))
            + list(self.strata_dir.glob("Strata.*.json"))
        )
        if not strata_files:
            return None

        latest_file = strata_files[-1]
        text = latest_file.read_text(encoding="utf-8")
        if latest_file.suffix.lower() in {".yml", ".yaml"}:
            return yaml.safe_load(text) or {}
        return json.loads(text)
