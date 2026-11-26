import importlib
from pathlib import Path
import re
import sys
from typing import Any, Dict, List, Optional
import yaml

from Chaos.base_chaos import BaseChaos
from Entropy.base_entropy import BaseEntropy
from Processor.base_processor import BaseProcessor
from StrataCrystallization.base_strata import BaseStrata


# =========================================================
# 1. Chaos（零点・感覚器）：対話ドラフト・地層シードの感知
# =========================================================
class DialogueQuantumChaos(BaseChaos):
    def find_seed_in_chaos(self, explicit_path: Optional[str] = None) -> Optional[Path]:
        """Chaos/seeds/ から投入された対話ドラフトやシードを探す"""
        if explicit_path:
            p = Path(explicit_path)
            if not p.exists():
                raise FileNotFoundError(f"指定されたシードが見つかりません: {p}")
            return p

        seeds_dir = Path("Chaos/seeds")
        if seeds_dir.exists():
            candidates = sorted(
                list(seeds_dir.glob("*.md"))
                + list(seeds_dir.glob("*.yml"))
                + list(seeds_dir.glob("*.yaml"))
            )
            if candidates:
                return candidates[-1]
        return None

    def perceive(self, raw_input: Any) -> Dict[str, Any]:
        # ケースA: 過去の地層（Strata）からの継承シード
        if isinstance(raw_input, dict) and "artifact" in raw_input:
            artifact = raw_input["artifact"]
            prev_gen = artifact.get("generation", 1)
            theme = artifact.get("theme", "Quantum-Okinawa-Horizon")
            return {
                "mode": "strata_inheritance",
                "generation": prev_gen + 1,
                "theme": theme,
                "raw_dialogue": (
                    f"# {theme}（第{prev_gen + 1}世代継承）\n\n"
                    f"## 継承の章：地層からの再励起\n"
                    f"### 結晶の記憶\n"
                    f"語り手：前世代（第{prev_gen}世代）で結晶化した『{theme}』の記憶を受け継ぎ、さらなる細目へと練り上げる。\n"
                ),
                "source_file": raw_input.get("chronicle_file", "Previous-Strata"),
            }

        # ケースB: Chaos/seeds/ からのファイル入力（.md または .yml）
        if isinstance(raw_input, Path):
            text = raw_input.read_text(encoding="utf-8")
            if raw_input.suffix.lower() in {".yml", ".yaml"}:
                data = yaml.safe_load(text) or {}
                if data.get("anomaly_flag") is True:
                    return {
                        "mode": "external_yaml",
                        "generation": 1,
                        "theme": data.get("theme", "Anomalous-Seed"),
                        "raw_dialogue": "",
                        "source_file": raw_input.name,
                    }
                theme = data.get("theme", raw_input.stem)
                dialogue = data.get("raw_dialogue") or data.get("raw_impulse", "")
                if dialogue and not str(dialogue).startswith("#"):
                    dialogue = f"# {theme}\n\n## 序章：揺らぎの感知\n### 核となる衝動\n語り手：{dialogue}\n"
                return {
                    "mode": "external_yaml",
                    "generation": 1,
                    "theme": theme,
                    "raw_dialogue": str(dialogue),
                    "source_file": raw_input.name,
                }

            # Markdown対話ドラフト（.md）の場合
            title_match = re.search(r"^#\s+(.+)$", text, flags=re.MULTILINE)
            theme = title_match.group(1).strip() if title_match else raw_input.stem
            return {
                "mode": "dialogue_draft",
                "generation": 1,
                "theme": theme,
                "raw_dialogue": text,
                "source_file": raw_input.name,
            }

        # ケースC: 完全な零点起動（シードも地層も空の場合）
        default_theme = "Quantum-Okinawa-Horizon"
        return {
            "mode": "zero_point_genesis",
            "generation": 1,
            "theme": default_theme,
            "raw_dialogue": (
                f"# {default_theme}\n\n"
                "## 第一章：零点の呼吸\n"
                "### 混沌からの創世\n"
                "語り手：静かなデジタルの海に最初の波紋が広がり、四つの聖域が自律の呼吸を始める。\n"
            ),
            "source_file": "Genesis-Zero-Point",
        }


# =========================================================
# 2. Entropy（神経・破骨細胞）：不純物除去＆「お題＞章＞節＞文」カスケード
# =========================================================
class CascadeGeometricEntropy(BaseEntropy):
    NOISE_PATTERNS = (
        "出典を入力",
        "コピーしました",
        "Thinking Process:",
    )

    def dissolve_and_align(self, fluctuation: Dict[str, Any]) -> Dict[str, Any]:
        raw_text = fluctuation.get("raw_dialogue", "")
        theme = fluctuation.get("theme", "無題の対話録")
        gen = fluctuation.get("generation", 1)

        # 1. 破骨細胞フィルタ（空行とノイズの除去）
        cleaned_lines: List[str] = []
        for line in raw_text.splitlines():
            stripped = line.strip()
            if not stripped:
                continue
            if any(noise in stripped for noise in self.NOISE_PATTERNS):
                continue
            cleaned_lines.append(stripped)

        if not cleaned_lines:
            raise ValueError("有効な対話テキストが存在しません（ノイズまたは空白のみのため隔離）。")

        # 2. カスケード構造化（お題 > 章 > 節 > 文）
        cascade: Dict[str, Any] = {
            "theme": theme,
            "chapters": [],
        }

        current_chapter: Dict[str, Any] = {"chapter_title": "序章：零点の呼吸", "sections": []}
        current_section: Dict[str, Any] = {"section_title": "導入", "sentences": []}

        for line in cleaned_lines:
            if line.startswith("# "):
                continue
            elif line.startswith("## "):
                if current_section["sentences"]:
                    current_chapter["sections"].append(current_section)
                if current_chapter["sections"]:
                    cascade["chapters"].append(current_chapter)

                current_chapter = {"chapter_title": line[3:].strip(), "sections": []}
                current_section = {"section_title": "本節", "sentences": []}
            elif line.startswith("### "):
                if current_section["sentences"]:
                    current_chapter["sections"].append(current_section)
                current_section = {"section_title": line[4:].strip(), "sentences": []}
            else:
                speaker = "語り手"
                utterance = line
                if "：" in line:
                    sp, ut = line.split("：", 1)
                    speaker = sp.strip(" *")
                    utterance = ut.strip()
                elif ":" in line and not line.startswith("http"):
                    sp, ut = line.split(":", 1)
                    speaker = sp.strip(" *")
                    utterance = ut.strip()

                sub_sentences = [s + "。" for s in utterance.split("。") if s.strip()]
                if not sub_sentences:
                    sub_sentences = [utterance]

                for s in sub_sentences:
                    current_section["sentences"].append({
                        "speaker": speaker,
                        "text": s,
                    })

        if current_section["sentences"]:
            current_chapter["sections"].append(current_section)
        if current_chapter["sections"]:
            cascade["chapters"].append(current_chapter)

        if not cascade["chapters"]:
            raise ValueError("章・節・文のカスケード構造を抽出できませんでした（見出しのみの不完全入力）。")

        vertices = (gen % 8) + 3
        return {
            "generation": gen,
            "theme": theme,
            "structure": f"{vertices}-gon_wireframe",
            "cascade": cascade,
            "source_file": fluctuation.get("source_file"),
        }


# =========================================================
# 3. Processor（心臓・骨芽細胞）：工程別パイプ化＆演出定着
# =========================================================
class ScenarioLightProcessor(BaseProcessor):
    VOICE_PROFILES = {
        "琉坊さとし": {"voice": "ja-JP-KeitaNeural", "rate": "+5%", "tone": "philosophical_calm"},
        "Gemini嬢": {"voice": "ja-JP-NanamiNeural", "rate": "+12%", "tone": "clear_insightful"},
        "語り手": {"voice": "ja-JP-AoiNeural", "rate": "+8%", "tone": "poetic_narration"},
    }

    def materialize(self, wireframe: Dict[str, Any]) -> Dict[str, Any]:
        gen = wireframe.get("generation", 1)
        theme = wireframe.get("theme", "無題")
        structure = wireframe.get("structure", "4-gon_wireframe")
        cascade = wireframe.get("cascade", {})
        spectrum = "Okinawa-Azure-Gold" if gen % 2 == 1 else "Deep-Quantum-Indigo"

        pipes: List[Dict[str, Any]] = []
        pipe_index = 1

        for ch_idx, chapter in enumerate(cascade.get("chapters", []), start=1):
            for sec_idx, section in enumerate(chapter.get("sections", []), start=1):
                cues = []
                for sent in section.get("sentences", []):
                    speaker = sent["speaker"]
                    profile = self.VOICE_PROFILES.get(speaker, self.VOICE_PROFILES["語り手"])
                    cues.append({
                        "speaker": speaker,
                        "text": sent["text"],
                        "audio_directive": profile,
                    })

                pipes.append({
                    "pipe_id": f"PIPE-{pipe_index:02d}",
                    "stage": f"第{ch_idx}章 / 第{sec_idx}節",
                    "chapter": chapter["chapter_title"],
                    "section": section["section_title"],
                    "visual_prompt": (
                        f"Sacred geometry {structure}, theme '{theme}', "
                        f"scene '{chapter['chapter_title']} - {section['section_title']}', "
                        f"illuminated by {spectrum} quantum light, 8k"
                    ),
                    "dialogue_cues": cues,
                })
                pipe_index += 1

        return {
            "generation": gen,
            "theme": theme,
            "structure": structure,
            "light_spectrum": spectrum,
            "total_pipes": len(pipes),
            "cascade_tree": cascade,
            "scenario_pipes": pipes,
            "source_file": wireframe.get("source_file"),
        }


# =========================================================
# 4. StrataCrystallization（地層・骨格）：年代記(.md) & YAML結晶化
# =========================================================
class ScenarioChronicleStrata(BaseStrata):
    def format_fossil(self, artifact: Dict[str, Any]) -> str:
        lines = [
            f"# Strata Chronicle — Generation {artifact.get('generation')}: {artifact.get('theme')}",
            "",
            f"- **Source File:** `{artifact.get('source_file')}`",
            f"- **Geometry Structure:** `{artifact.get('structure')}`",
            f"- **Light Spectrum:** `{artifact.get('light_spectrum')}`",
            f"- **Total Pipes:** `{artifact.get('total_pipes')}`",
            "",
            "## シナリオ・パイプライン構成",
        ]
        for pipe in artifact.get("scenario_pipes", []):
            lines.append(f"### {pipe['pipe_id']}｜{pipe['chapter']}（{pipe['section']}）")
            lines.append(f"- **Visual Prompt:** `{pipe['visual_prompt']}`")
            for cue in pipe["dialogue_cues"]:
                lines.append(f"  - **{cue['speaker']}**: {cue['text']}")
            lines.append("")
        return "\n".join(lines)


# =========================================================
# 第4の零点：自律循環サイクルの実行
# =========================================================
def run_autonomous_cycle(explicit_seed_path: Optional[str] = None) -> None:
    # __init__.py のトポロジ定義を読み込んで連携を確認
    chaos_mod = importlib.import_module("Chaos")
    entropy_mod = importlib.import_module("Entropy")
    processor_mod = importlib.import_module("Processor")
    strata_mod = importlib.import_module("StrataCrystallization")

    print("=== [imagesProjector] 自律循環サイクル起動 ===")
    print(
        f"[Topology] {chaos_mod.SANCTUARY_NAME} -> {chaos_mod.NEXT_SANCTUARY} -> "
        f"{entropy_mod.NEXT_SANCTUARY} -> {processor_mod.NEXT_SANCTUARY} -> {strata_mod.NEXT_SANCTUARY}"
    )

    chaos = DialogueQuantumChaos(sanctuary_name=chaos_mod.SANCTUARY_NAME)
    entropy = CascadeGeometricEntropy(sanctuary_name=entropy_mod.SANCTUARY_NAME)
    processor = ScenarioLightProcessor(sanctuary_name=processor_mod.SANCTUARY_NAME)
    strata = ScenarioChronicleStrata(sanctuary_name=strata_mod.SANCTUARY_NAME)

    # Step 1: 入力ソースの決定（明示指定 ＞ Chaos/seeds内の新規ドラフト ＞ 既存地層の継承 ＞ 零点起動）
    seed_path = chaos.find_seed_in_chaos(explicit_seed_path)
    if seed_path is not None:
        print(f"[Chaos] 外部シード/ドラフトを感知: {seed_path}")
        raw_input: Any = seed_path
    else:
        latest_strata = strata.excavate_latest_seed()
        if latest_strata is not None:
            print(f"[Chaos] 既存地層から記憶を発掘: {latest_strata.get('chronicle_file')}")
            raw_input = latest_strata
        else:
            print("[Chaos] 未踏の地層のため零点（Genesis）から起動します")
            raw_input = None

    # Step 2: Chaos（感覚器）
    chaos_packet = chaos.emit_fluctuation(raw_input)
    print(
        f"[Chaos] 揺らぎ抽出完了 -> Theme: '{chaos_packet['payload']['theme']}' "
        f"(Mode: {chaos_packet['payload']['mode']})"
    )

    # Step 3: Entropy（破骨細胞フィルタ ＋ カスケード整流）
    is_aligned, entropy_packet = entropy.circulate(chaos_packet)
    if not is_aligned:
        print(f"[Entropy / 破骨細胞] 不純物を検知・隔離しました: {entropy_packet['report']}")
        skipped = processor.pulse(entropy_packet)
        print(f"[Processor] 代謝スキップ確認 -> {skipped['phase']}")
        sys.exit(1)

    chapters_count = len(entropy_packet["wireframe"]["cascade"]["chapters"])
    print(
        f"[Entropy] カスケード整流完了 -> {entropy_packet['wireframe']['structure']} "
        f"({chapters_count}章構成)"
    )

    # Step 4: Processor（工程別パイプ化 ＋ 演出定着）
    processor_packet = processor.pulse(entropy_packet)
    print(
        f"[Processor] パイプ化・演出定着完了 -> "
        f"{processor_packet['artifact']['total_pipes']}本のパイプ生成 "
        f"({processor_packet['artifact']['light_spectrum']})"
    )

    # Step 5: StrataCrystallization（YAML & Markdown 結晶化）
    result = strata.crystallize(processor_packet)
    print(f"[Strata] 結晶化完了 -> Markdown: {result['chronicle_file']}")
    if "seed_file" in result:
        print(f"[Strata] 次期設計図YAML -> {result['seed_file']}")
    print("=== サイクル正常終了 ===")


if __name__ == "__main__":
    arg_seed = sys.argv[1] if len(sys.argv) > 1 else None
    run_autonomous_cycle(arg_seed)
