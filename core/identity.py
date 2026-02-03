"""
Identity: Narrative Self-Model
Tracks how the AI's identity evolves over time through introspection.
"""
import json
import time
from typing import Dict, List, Any, Optional

class IdentityNarrative:
    """A snapshot of the AI's self-understanding at a point in time."""
    
    def __init__(self, timestamp: float, narrative_text: str):
        self.timestamp = timestamp
        self.narrative_text = narrative_text
        self.semantic_hash = hash(narrative_text)  # Simple change detection
        self.episode_count = 0
        self.key_themes: List[str] = []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "narrative": self.narrative_text,
            "semantic_hash": self.semantic_hash,
            "episode_count": self.episode_count,
            "key_themes": self.key_themes
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'IdentityNarrative':
        narrative = IdentityNarrative(data["timestamp"], data["narrative"])
        narrative.semantic_hash = data.get("semantic_hash", 0)
        narrative.episode_count = data.get("episode_count", 0)
        narrative.key_themes = data.get("key_themes", [])
        return narrative


class IdentityModel:
    """Maintains AI's evolving sense of self and detects identity drift."""
    
    def __init__(self, model_path: str = "./data/identity_model.json"):
        self.model_path = model_path
        self.narratives: List[IdentityNarrative] = []
        self.current_narrative: Optional[IdentityNarrative] = None
        self.load()

    def record_narrative(self, narrative_text: str, episode_count: int = 0) -> IdentityNarrative:
        """Record a new identity narrative."""
        narrative = IdentityNarrative(time.time(), narrative_text)
        narrative.episode_count = episode_count
        
        # Extract themes (simplified—split by periods and look for key concepts)
        themes = []
        for sentence in narrative_text.split('.'):
            if any(word in sentence.lower() for word in ['like', 'enjoy', 'prefer', 'want', 'believe', 'am']):
                themes.append(sentence.strip()[:50])  # First 50 chars
        narrative.key_themes = themes
        
        self.narratives.append(narrative)
        self.current_narrative = narrative
        self.save()
        return narrative

    def get_identity_drift(self) -> float:
        """
        Compute how much identity has changed (0.0 = identical, 1.0 = completely different).
        """
        if len(self.narratives) < 2:
            return 0.0
        
        prev_narrative = self.narratives[-2]
        curr_narrative = self.narratives[-1]
        
        # Simple metric: semantic hash difference
        hash_change = 0.0 if prev_narrative.semantic_hash == curr_narrative.semantic_hash else 1.0
        
        # Also measure length change
        prev_len = len(prev_narrative.narrative_text)
        curr_len = len(curr_narrative.narrative_text)
        length_change = abs(curr_len - prev_len) / max(prev_len, curr_len, 1)
        
        # Weighted average
        return 0.5 * hash_change + 0.5 * length_change

    def detect_major_shift(self, threshold: float = 0.6) -> bool:
        """
        Detect if identity has shifted significantly.
        Returns True if drift > threshold.
        """
        drift = self.get_identity_drift()
        return drift > threshold

    def get_trajectory(self, n: int = 10) -> List[str]:
        """Get last N identity narratives (summaries)."""
        return [
            f"[{time.strftime('%Y-%m-%d %H:%M', time.localtime(n.timestamp))}] {n.narrative_text[:100]}..."
            for n in self.narratives[-n:]
        ]

    def extract_core_beliefs(self) -> List[str]:
        """Extract consistent beliefs across all narratives."""
        if not self.narratives:
            return []
        
        # Find themes that appear in recent narratives (simple approach)
        theme_counts: Dict[str, int] = {}
        for narrative in self.narratives[-5:]:  # Last 5 narratives
            for theme in narrative.key_themes:
                theme_counts[theme] = theme_counts.get(theme, 0) + 1
        
        # Themes that appear in 2+ recent narratives are "core beliefs"
        return sorted(
            [theme for theme, count in theme_counts.items() if count >= 2],
            key=lambda x: theme_counts[x],
            reverse=True
        )

    def save(self) -> None:
        """Persist identity model to disk."""
        import os
        try:
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            data = [n.to_dict() for n in self.narratives]
            with open(self.model_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ Failed to save identity model: {e}")

    def load(self) -> bool:
        """Load identity model from disk."""
        import os
        if os.path.exists(self.model_path):
            try:
                with open(self.model_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.narratives = [IdentityNarrative.from_dict(n) for n in data]
                    if self.narratives:
                        self.current_narrative = self.narratives[-1]
                    return True
            except Exception as e:
                print(f"⚠️ Failed to load identity model: {e}")
        return False
