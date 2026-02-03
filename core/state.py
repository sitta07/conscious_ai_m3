"""
Enhanced State Management with:
- Semantic deduplication of facts
- Identity continuity tracking
- Coherence validation
"""
import time
import random
import json
import os
from typing import List, Dict, Optional, Tuple

class State:
    def __init__(self, checkpoint_path: str = "./data/state_checkpoint.json"):
        self.checkpoint_path = checkpoint_path
        if self.load():
            print("📦 Loaded previous state & memories.")
        else:
            print("🐣 Creating new identity (First born).")
            self.energy = 100.0
            self.happiness = 50.0
            self.known_facts = []
            self.fact_timestamps: Dict[str, float] = {}  # Track when facts were learned
        self.last_update = time.time()
        
    def update(self, action_type: str):
        current_time = time.time()
        if action_type == "talk":
            self.energy -= 2.0
            self.happiness += random.uniform(-1, 2)
        elif action_type == "sleep":
            self.energy = 100.0
            self.happiness = 50.0 
        elif action_type == "idle":
            pass 
        self.energy = max(0, min(100, self.energy))
        self.happiness = max(0, min(100, self.happiness))
        self.last_update = current_time
        self.save() 

    def add_fact(self, fact_text: str, memory_system=None) -> bool:
        """
        Add fact with semantic deduplication.
        memory_system: Optional Memory object for similarity checking.
        """
        clean_fact = fact_text.strip()
        
        # Basic validation
        if not clean_fact or len(clean_fact) < 3:
            return False
        
        # Check for exact duplicates
        if clean_fact in self.known_facts:
            return False
        
        # Semantic deduplication using memory system
        if memory_system:
            similar_facts = memory_system.find_similar_facts(clean_fact, n_results=3)
            if similar_facts:
                # Check if any are essentially the same
                for similar in similar_facts:
                    if self._is_semantic_duplicate(clean_fact, similar):
                        print(f"   (📌 Duplicate avoided: '{clean_fact}' ≈ '{similar}')")
                        return False
        
        # Add fact with timestamp
        self.known_facts.append(clean_fact)
        self.fact_timestamps[clean_fact] = time.time()
        self.save()
        return True

    def get_facts_by_age(self, max_age_days: float = None) -> List[str]:
        """Get facts, optionally filtering by age."""
        if max_age_days is None:
            return self.known_facts
        
        max_age_seconds = max_age_days * 86400
        current_time = time.time()
        
        return [
            fact for fact in self.known_facts
            if current_time - self.fact_timestamps.get(fact, current_time) <= max_age_seconds
        ]

    def _is_semantic_duplicate(self, fact1: str, fact2: str, threshold: float = 0.85) -> bool:
        """
        Simple heuristic for semantic similarity.
        In production, use embeddings or fuzzy matching.
        """
        # Normalize
        f1 = fact1.lower().replace("user ", "").replace("i ", "")
        f2 = fact2.lower().replace("user ", "").replace("i ", "")
        
        # Exact substring match
        if f1 in f2 or f2 in f1:
            return True
        
        # Similar length and key words overlap
        words1 = set(f1.split())
        words2 = set(f2.split())
        
        if not words1 or not words2:
            return False
        
        overlap = len(words1 & words2) / max(len(words1), len(words2))
        return overlap > threshold

    def get_status(self) -> dict:
        return {
            "energy": round(self.energy, 1),
            "happiness": round(self.happiness, 1),
            "status_description": self._describe_state(),
            "facts_count": len(self.known_facts)
        }

    def _describe_state(self) -> str:
        if self.energy < 20: return "EXHAUSTED"
        elif self.energy < 50: return "TIRED"
        elif self.happiness < 30: return "GRUMPY"
        elif self.happiness > 70: return "EXCITED"
        else: return "NEUTRAL"

    def get_identity_coherence(self) -> float:
        """
        Simple score for identity coherence (0.0 = fragmented, 1.0 = perfectly coherent).
        Based on: fact consistency, stability, temporal continuity.
        """
        if not self.known_facts:
            return 0.5  # Neutral (no data)
        
        # Score 1: Fact stability (older facts = more stable)
        current_time = time.time()
        ages = [current_time - self.fact_timestamps.get(f, current_time) for f in self.known_facts]
        stability_score = min(1.0, sum(ages) / (len(ages) * 86400)) if ages else 0.0
        
        # Score 2: Fact count (healthy = 5-30 facts)
        fact_count = len(self.known_facts)
        if 5 <= fact_count <= 30:
            count_score = 1.0
        elif fact_count < 5:
            count_score = fact_count / 5
        else:
            count_score = max(0.5, 1.0 - (fact_count - 30) / 100)
        
        # Combined coherence
        return 0.6 * stability_score + 0.4 * count_score

    def flag_identity_drift(self, threshold: float = 0.3) -> bool:
        """
        Returns True if identity has drifted significantly.
        Drift detected when: coherence drops sharply, contradictions appear, etc.
        """
        coherence = self.get_identity_coherence()
        return coherence < threshold

    def save(self):
        data = {
            "energy": self.energy,
            "happiness": self.happiness,
            "known_facts": self.known_facts,
            "fact_timestamps": self.fact_timestamps,
            "last_active": time.time()
        }
        try:
            os.makedirs(os.path.dirname(self.checkpoint_path), exist_ok=True)
            with open(self.checkpoint_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"⚠️ Failed to save state: {e}")

    def load(self) -> bool:
        if os.path.exists(self.checkpoint_path):
            try:
                with open(self.checkpoint_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.energy = data.get("energy", 100.0)
                    self.happiness = data.get("happiness", 50.0)
                    self.known_facts = data.get("known_facts", [])
                    self.fact_timestamps = data.get("fact_timestamps", {})
                    return True
            except Exception as e:
                print(f"⚠️ Corrupted save file: {e}")
        return False