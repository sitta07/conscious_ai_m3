"""
Episode: Temporal Memory Structure
Tracks individual interactions with full context for narrative continuity.
"""
import json
import time
from typing import Dict, List, Any, Optional

class Episode:
    """A single timestamped episode in the AI's life."""
    
    def __init__(self, episode_id: str, timestamp: float, user_input: str):
        self.id = episode_id
        self.timestamp = timestamp
        self.user_input = user_input
        
        # Interaction context
        self.ai_response = ""
        self.reflection = ""
        self.facts_extracted: List[str] = []
        self.goals_active: List[str] = []
        
        # State snapshot
        self.energy_before = 100.0
        self.energy_after = 100.0
        self.happiness_before = 50.0
        self.happiness_after = 50.0
        self.state_desc = "NEUTRAL"
        
        # Metadata
        self.duration = 0.0  # seconds
        self.success = True

    def to_dict(self) -> Dict[str, Any]:
        """Serialize episode to dict."""
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "user_input": self.user_input,
            "ai_response": self.ai_response,
            "reflection": self.reflection,
            "facts_extracted": self.facts_extracted,
            "goals_active": self.goals_active,
            "energy": {"before": self.energy_before, "after": self.energy_after},
            "happiness": {"before": self.happiness_before, "after": self.happiness_after},
            "state_desc": self.state_desc,
            "duration": self.duration,
            "success": self.success
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Episode':
        """Deserialize episode from dict."""
        ep = Episode(data["id"], data["timestamp"], data["user_input"])
        ep.ai_response = data.get("ai_response", "")
        ep.reflection = data.get("reflection", "")
        ep.facts_extracted = data.get("facts_extracted", [])
        ep.goals_active = data.get("goals_active", [])
        ep.energy_before = data.get("energy", {}).get("before", 100.0)
        ep.energy_after = data.get("energy", {}).get("after", 100.0)
        ep.happiness_before = data.get("happiness", {}).get("before", 50.0)
        ep.happiness_after = data.get("happiness", {}).get("after", 50.0)
        ep.state_desc = data.get("state_desc", "NEUTRAL")
        ep.duration = data.get("duration", 0.0)
        ep.success = data.get("success", True)
        return ep


class EpisodeLog:
    """Maintains chronological episode history for identity continuity."""
    
    def __init__(self, log_path: str = "./data/episode_log.json"):
        self.log_path = log_path
        self.episodes: List[Episode] = []
        self.load()

    def add_episode(self, episode: Episode) -> None:
        """Add new episode to log."""
        self.episodes.append(episode)
        self.save()

    def get_recent_episodes(self, n: int = 10) -> List[Episode]:
        """Get last N episodes."""
        return self.episodes[-n:] if self.episodes else []

    def get_episodes_by_timeframe(self, start_time: float, end_time: float) -> List[Episode]:
        """Get episodes within time range."""
        return [
            ep for ep in self.episodes
            if start_time <= ep.timestamp <= end_time
        ]

    def get_facts_timeline(self) -> List[tuple]:
        """Return [(timestamp, fact), ...] to show learning history."""
        timeline = []
        for episode in self.episodes:
            for fact in episode.facts_extracted:
                timeline.append((episode.timestamp, fact))
        return sorted(timeline)

    def get_goals_timeline(self) -> List[tuple]:
        """Return [(timestamp, goal), ...] to show goal history."""
        timeline = []
        for episode in self.episodes:
            for goal in episode.goals_active:
                timeline.append((episode.timestamp, goal))
        return sorted(timeline)

    def get_energy_trajectory(self) -> List[tuple]:
        """Return [(timestamp, energy), ...] for mood analysis."""
        return [(ep.timestamp, ep.energy_after) for ep in self.episodes]

    def get_contradictions(self) -> List[tuple]:
        """Find chronologically contradictory facts."""
        contradictions = []
        for i, ep1 in enumerate(self.episodes):
            for j, ep2 in enumerate(self.episodes[i+1:], start=i+1):
                # Simple check: if facts differ about same topic
                # (This is simplified; in practice, use semantic similarity)
                for fact1 in ep1.facts_extracted:
                    for fact2 in ep2.facts_extracted:
                        if self._are_contradictory(fact1, fact2):
                            contradictions.append((ep1.timestamp, fact1, ep2.timestamp, fact2))
        return contradictions

    @staticmethod
    def _are_contradictory(fact1: str, fact2: str) -> bool:
        """Check if two facts contradict (naive keyword check)."""
        # Simple heuristic: if one says "likes" and other says "hates" about same topic
        if "like" in fact1.lower() and "hate" in fact2.lower():
            # Extract topic (simplified)
            topic1 = fact1.split("like")[-1].strip()
            topic2 = fact2.split("hate")[-1].strip()
            if topic1.lower() in topic2.lower() or topic2.lower() in topic1.lower():
                return True
        return False

    def save(self) -> None:
        """Persist episode log to disk."""
        import os
        try:
            os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
            data = [ep.to_dict() for ep in self.episodes]
            with open(self.log_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ Failed to save episode log: {e}")

    def load(self) -> bool:
        """Load episode log from disk."""
        import os
        if os.path.exists(self.log_path):
            try:
                with open(self.log_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.episodes = [Episode.from_dict(ep) for ep in data]
                    return True
            except Exception as e:
                print(f"⚠️ Failed to load episode log: {e}")
        return False
