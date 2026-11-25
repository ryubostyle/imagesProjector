"""Auto-generated autonomous circulation entry point from architecture.yml."""
from datetime import datetime
import importlib
from pathlib import Path
import sys
from typing import Any, Dict
from zoneinfo import ZoneInfo

# 4つの聖域から基底クラスをインポート
from Chaos.base_chaos import BaseChaos
from Entropy.base_entropy import BaseEntropy
from Processor.base_processor import BaseProcessor
from StrataCrystallization.base_strata import BaseStrata

SYSTEM_NAME = "imagesProjector - Autonomous Art Pipeline"
TIMEZONE = "Asia/Tokyo"
CASCADE_ORDER = ["Chaos", "Entropy", "Processor", "StrataCrystallization"]
PROJECT_ROOT = Path(__file__).resolve().parent


# ==========================================
# 1. 各聖域の具象クラス（最小実装）
# ==========================================

class QuantumChaos(BaseChaos):
    """【零点・感覚器】地層から発掘された過去の記憶、または原初の揺らぎを感知する"""
    def perceive(self, raw_input: Any) -> Dict[str, Any]:
        if isinstance(raw_input, dict) and "artifact" in raw_input:
            # 過去の地層（JSON）から世代と本質を引き継ぐ
            prev_artifact = raw_input["artifact"]
            prev_gen = prev_artifact.get("generation", 0)
            prev_essence = prev_artifact.get("essence", "Zero-Point")
            return {
                "generation": prev_gen + 1,
                "seed_essence": f"Evolved({prev_essence})",
                "origin_source": raw_input.get("chronicle_file", "unknown_strata"),
            }
        # 地層が空（初回起動）の場合の原初の火花
        return {
            "generation": 1,
            "seed_essence": "Primordial-Fluctuation",
            "origin_source": "Genesis-Zero-Point",
        }


class GeometricEntropy(BaseEntropy):
    """【神経・血流 / 破骨細胞】ノイズを溶かして隔離し、幾何学ワイヤーフレームへ整流する"""
    def dissolve_and_align(self, fluctuation: Dict[str, Any]) -> Dict[str, Any]:
        gen = fluctuation.get("generation", 1)
        essence = fluctuation.get("seed_essence", "").strip()
        if not essence:
            raise ValueError("Empty essence detected: dissolving into ErrorTrapper.")

        # 世代ごとに変化する幾何学ワイヤーフレーム（三角形〜十角形の位相循環）
        vertices = (gen % 8) + 3
        return {
            "generation": gen,
            "essence": essence,
            "origin_source": fluctuation.get("origin_source"),
            "geometry": f"{vertices}-gon_wireframe",
            "symmetry_axis": "Oneness-Axis",
        }


class LightProcessor(BaseProcessor):
    """【心臓・意志 / 骨芽細胞】幾何学ワイヤーフレームに光エネルギーを与え作品を具現化する"""
    def materialize(self, wireframe: Dict[str, Any]) -> Dict[str, Any]:
        gen = wireframe["generation"]
        geom = wireframe["geometry"]
        essence = wireframe["essence"]
        spectrum = "Okinawa-Azure-Gold" if gen % 2 == 1 else "Deep-Quantum-Indigo"

        return {
            "generation": gen,
            "essence": essence,
            "origin_source": wireframe.get("origin_source"),
            "structure": geom,
            "light_spectrum": spectrum,
            "manifestation": f"Crystal Layer #{gen:04d} crystallized via {geom} ({spectrum})",
        }


class ChronicleStrata(BaseStrata):
    """【地層・骨格 / 無機質の結晶】具現化された作品を燃えない年代記（Markdown）として刻む"""
    def format_fossil(self, artifact: Dict[str, Any], metadata: Dict[str, Any]) -> str:
        return (
            f"# Strata Chronicle — Generation {artifact.get('generation')}\n\n"
            f"- **Deposited At (JST)**: `{metadata.get('deposited_at')}`\n"
            f"- **Inherited From**: `{artifact.get('origin_source')}`\n"
            f"- **Geometry**: `{artifact.get('structure')}`\n"
            f"- **Light Spectrum**: `{artifact.get('light_spectrum')}`\n"
            f"- **Essence**: `{artifact.get('essence')}`\n\n"
            f"## Manifestation\n"
            f"> {artifact.get('manifestation')}\n"
        )


# ==========================================
# 2. トポロジ検証 & 4聖域の円環オーケストレーション
# ==========================================

def verify_topology() -> None:
    """architecture.yml から生成された各聖域の __init__.py 経路を検証する"""
    now_str = datetime.now(ZoneInfo(TIMEZONE)).strftime("%Y.%m.%d.%H%M")
    print(f"=== {SYSTEM_NAME} ===")
    print(f"Timestamp ({TIMEZONE}): {now_str}")
    print("-" * 56)
    for name in CASCADE_ORDER:
        mod = importlib.import_module(name)
        print(f"  [Sanctuary] {mod.SANCTUARY_NAME:<22} -> next: {mod.NEXT_SANCTUARY}")
    print("-" * 56)


def run_autonomous_cycle() -> int:
    """地層からの発掘と新たな結晶化を1サイクル実行する"""
    verify_topology()

    chaos = QuantumChaos()
    entropy = GeometricEntropy()
    processor = LightProcessor()
    strata = ChronicleStrata()

    # Step 1: 地層（Strata）から最新の結晶を発掘（初回は None）
    latest_seed = strata.excavate_latest_seed()
    if latest_seed:
        print(f"⛏️  [Excavation] Inherited seed from: {latest_seed.get('chronicle_file')}")
    else:
        print("✨ [Genesis] No existing strata found. Starting from Zero-Point.")

    # Step 2: Chaos（感覚器）— 揺らぎの感知と放出
    chaos_packet = chaos.emit_fluctuation(latest_seed)
    gen = chaos_packet["payload"]["generation"]
    print(f"🌀 [Chaos] Phase -> {chaos_packet['phase']} (Generation {gen})")

    # Step 3: Entropy（神経・血流）— 浄化と幾何学ワイヤーフレームへの整流
    is_aligned, entropy_packet = entropy.circulate(chaos_packet)
    if not is_aligned:
        print(f"⚠️  [Entropy] Quarantined anomaly: {entropy_packet['report']}", file=sys.stderr)
        return 1
    print(f"🕸️  [Entropy] Phase -> {entropy_packet['phase']} ({entropy_packet['wireframe']['geometry']})")

    # Step 4: Processor（心臓・意志）— 光エネルギーの定着と具現化
    processor_packet = processor.pulse(entropy_packet)
    if processor_packet.get("phase") != "ready_for_strata":
        print(f"⚠️  [Processor] Skipped: {processor_packet.get('reason')}", file=sys.stderr)
        return 1
    print(f"💓 [Processor] Phase -> {processor_packet['phase']}")

    # Step 5: StrataCrystallization（地層・骨格）— 永続ファイル（.md / .json）への結晶化
    result = strata.crystallize(processor_packet, prefix="Strata")
    if result.get("phase") != "crystallized":
        print(f"⚠️  [Strata] Failed to deposit: {result.get('reason')}", file=sys.stderr)
        return 1

    print(f"💎 [Strata] Chronicle saved -> {result['chronicle_path']}")
    print(f"🧬 [Strata] Next seed saved -> {result['seed_path']}")
    print("✅ Autonomous cycle complete.")
    return 0


if __name__ == "__main__":
    sys.exit(run_autonomous_cycle())
