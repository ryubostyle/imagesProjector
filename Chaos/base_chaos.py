from abc import ABC, abstractmethod
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict

JST = timezone(timedelta(hours=9))


class BaseChaos(ABC):
    """[Level 0: 零点・感覚器] 対話ドラフトや外界の微細な揺らぎを感知し、未整流パケットとして放出する基底クラス"""

    def __init__(
        self,
        sanctuary_name: str = "Chaos",
        seeds_dir: str = "Chaos/seeds",
    ) -> None:
        self.sanctuary_name = sanctuary_name
        self.seeds_dir = Path(seeds_dir)
        self._ensure_seeds_sanctuary()

    def _ensure_seeds_sanctuary(self) -> None:
        """外部シードや対話ドラフトを受け入れる seeds ディレクトリを保証する"""
        self.seeds_dir.mkdir(parents=True, exist_ok=True)

    @abstractmethod
    def perceive(self, raw_input: Any) -> Dict[str, Any]:
        """外界の入力（ファイルパス・辞書・テキスト・None）を感知し、揺らぎのペイロードへ変換する"""
        raise NotImplementedError

    def emit_fluctuation(self, raw_input: Any = None) -> Dict[str, Any]:
        """感知した揺らぎを標準パケットへ包み、次の聖域（Entropy）へ送出する"""
        payload = self.perceive(raw_input)
        return {
            "origin": self.sanctuary_name,
            "phase": "fluctuation_emitted",
            "emitted_at": datetime.now(JST).isoformat(),
            "payload": payload,
        }
