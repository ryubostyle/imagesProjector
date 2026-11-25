from abc import ABC, abstractmethod
from typing import Any, Dict, Tuple

class ErrorTrapper:
    """
    異常・偏り・ノイズを隔離し、システム全体の崩壊を防ぐ浄化装置（破骨細胞の役割）。
    """
    def __init__(self):
        self.quarantined: list[Dict[str, Any]] = []

    def trap(self, source: str, error: Exception, raw_data: Any) -> Dict[str, Any]:
        record = {
            "source": source,
            "error_type": type(error).__name__,
            "message": str(error),
            "dissolved_data": repr(raw_data),
        }
        self.quarantined.append(record)
        return record


class BaseEntropy(ABC):
    """
    【神経・血流】
    Chaosの揺らぎを受け取り、ノイズを溶かして幾何学ワイヤーフレームへ整流する基底クラス。
    """
    def __init__(self, sanctuary_name: str = "Entropy"):
        self.sanctuary_name = sanctuary_name
        self.trapper = ErrorTrapper()

    @abstractmethod
    def dissolve_and_align(self, fluctuation: Dict[str, Any]) -> Dict[str, Any]:
        """
        破骨細胞のように不要なノイズを溶かし、幾何学的な秩序（ワイヤーフレーム）へ整える。
        """
        pass

    def circulate(self, chaos_packet: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """
        整流を実行する。異常が検知された場合はErrorTrapperで隔離し、循環の健全性を保つ。
        """
        try:
            wireframe = self.dissolve_and_align(chaos_packet.get("payload", {}))
            return True, {
                "origin": self.sanctuary_name,
                "phase": "wireframe",
                "wireframe": wireframe,
                "trapped_count": len(self.trapper.quarantined),
            }
        except Exception as e:
            trapped = self.trapper.trap(self.sanctuary_name, e, chaos_packet)
            return False, {
                "origin": self.sanctuary_name,
                "phase": "quarantined",
                "report": trapped,
            }
