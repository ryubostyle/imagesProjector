from abc import ABC, abstractmethod
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, Optional
import json

JST = timezone(timedelta(hours=9))

class BaseStrata(ABC):
    """
    【地層・骨格】
    Processorから届いた結晶の種（ready_for_strata）を受け取り、
    時の経過にも風化しない永続的な記録と作品地層を刻む基底クラス。
    """
    def __init__(
        self,
        sanctuary_name: str = "StrataCrystallization",
        strata_dir: str = "StrataCrystallization/layers"
    ):
        self.sanctuary_name = sanctuary_name
        self.strata_dir = Path(strata_dir)

    def _ensure_bedrock(self) -> None:
        """
        地層を刻むための基盤ディレクトリ（岩盤）が存在することを保証する。
        """
        self.strata_dir.mkdir(parents=True, exist_ok=True)

    def _generate_chronicle_name(self, prefix: str = "Strata", ext: str = "md") -> str:
        """
        JST（Asia/Tokyo）のタイムスタンプに基づくドット区切りの地層ファイル名を生成する。
        例: Strata.2026.11.25.141800.md
        """
        now = datetime.now(JST)
        stamp = now.strftime("%Y.%m.%d.%H%M%S")
        return f"{prefix}.{stamp}.{ext}"

    @abstractmethod
    def format_fossil(self, artifact: Dict[str, Any], metadata: Dict[str, Any]) -> str:
        """
        具現化された作品とメタデータを、永続的な地層テキスト（Markdown等）へ整形する。
        """
        pass

    def crystallize(self, processor_packet: Dict[str, Any], prefix: str = "Strata") -> Dict[str, Any]:
        """
        Processorからのパケットを検証し、無機質の地層ファイルとして沈殿・定着させる。
        """
        if processor_packet.get("phase") != "ready_for_strata":
            return {
                "origin": self.sanctuary_name,
                "phase": "unsettled",
                "reason": f"Invalid phase: {processor_packet.get('phase')}",
            }

        self._ensure_bedrock()

        now_iso = datetime.now(JST).isoformat()
        artifact = processor_packet.get("artifact", {})
        metadata = {
            "sanctuary": self.sanctuary_name,
            "crystallized_at": processor_packet.get("crystallized_at", now_iso),
            "deposited_at": now_iso,
        }

        # 1. 記録・物語としての地層（Markdown）を刻む
        md_filename = self._generate_chronicle_name(prefix=prefix, ext="md")
        md_path = self.strata_dir / md_filename
        fossil_content = self.format_fossil(artifact, metadata)
        md_path.write_text(fossil_content, encoding="utf-8")

        # 2. 次なる循環（Chaos）が再利用できる構造化データ（JSON）も同時に沈殿させる
        json_filename = md_filename.replace(".md", ".json")
        json_path = self.strata_dir / json_filename
        strata_record = {
            "metadata": metadata,
            "artifact": artifact,
            "chronicle_file": md_filename,
        }
        json_path.write_text(
            json.dumps(strata_record, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

        return {
            "origin": self.sanctuary_name,
            "phase": "crystallized",
            "chronicle_path": str(md_path),
            "seed_path": str(json_path),
            "deposited_at": now_iso,
        }

    def excavate_latest_seed(self) -> Optional[Dict[str, Any]]:
        """
        最新の地層から結晶データを発掘し、次なる Chaos（零点）の新たな種として還元する。
        """
        if not self.strata_dir.exists():
            return None

        json_files = sorted(self.strata_dir.glob("*.json"))
        if not json_files:
            return None

        latest_file = json_files[-1]
        return json.loads(latest_file.read_text(encoding="utf-8"))
