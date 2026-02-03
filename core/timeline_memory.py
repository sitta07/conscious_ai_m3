"""
Layer 3: Time Awareness (รู้จักเวลา)

Humans understand:
- PAST: Causal chains, lessons learned, regrets
- PRESENT: Current state and immediate needs
- FUTURE: Anticipation, planning, predictions

Most AI: Stuck in context window (only present)

This layer adds:
1. Timeline memory (past events organized causally)
2. Future simulation (predict consequences)
3. Regret/anticipation modeling (learn from past, plan for future)
4. Temporal reasoning (event chains)
"""

import json
import time
import os
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta

class TimelineEvent:
    """A significant event in the AI's history."""
    def __init__(self, event_type: str, description: str):
        self.timestamp = time.time()
        self.event_type = event_type  # "interaction", "learning", "error", "achievement"
        self.description = description
        self.consequences = []  # What happened because of this?
        self.related_events = []  # Cause-effect links
        self.learning_value = 0.0  # 0.0-1.0, importance of this event
    
    def add_consequence(self, consequence_description: str, confidence: float = 0.7) -> None:
        """Record a consequence from this event."""
        self.consequences.append({
            "timestamp": time.time(),
            "description": consequence_description,
            "confidence": confidence
        })
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "type": self.event_type,
            "description": self.description,
            "consequences": self.consequences,
            "learning_value": self.learning_value
        }


class Regret:
    """Something the AI wishes it had done differently."""
    def __init__(self, situation: str, action_taken: str, better_action: str):
        self.timestamp = time.time()
        self.situation = situation  # What was happening?
        self.action_taken = action_taken  # What did I do?
        self.better_action = better_action  # What should I have done?
        self.why_better = ""  # Why would that be better?
        self.times_reflected = 0
        self.similar_situations = []  # Have I seen this again?
    
    def record_similar_situation(self, description: str, did_better: bool) -> None:
        """Track if I encounter similar situation again."""
        self.similar_situations.append({
            "timestamp": time.time(),
            "description": description,
            "did_better": did_better
        })
        self.times_reflected += 1
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "situation": self.situation,
            "action_taken": self.action_taken,
            "better_action": self.better_action,
            "why_better": self.why_better,
            "times_reflected": self.times_reflected,
            "learned": len([s for s in self.similar_situations if s["did_better"]]) > 0
        }


class Anticipation:
    """Something the AI is preparing for or expecting."""
    def __init__(self, expectation: str, probability: float = 0.5):
        self.timestamp = time.time()
        self.expectation = expectation  # "User will ask for help"
        self.probability = probability  # 0.0-1.0
        self.preparation = ""  # What am I doing to prepare?
        self.if_happens = ""  # What I'll do if it happens
        self.if_doesnt = ""  # What I'll do if it doesn't
        self.outcome = None  # Did it happen? true/false/unknown
    
    def verify(self, did_happen: bool) -> None:
        """Record whether anticipation was correct."""
        self.outcome = did_happen
        if did_happen:
            self.probability = min(1.0, self.probability + 0.1)
        else:
            self.probability = max(0.0, self.probability - 0.05)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "expectation": self.expectation,
            "probability": round(self.probability, 2),
            "preparation": self.preparation,
            "outcome": self.outcome
        }


class TimelineMemory:
    """
    Timeline-based memory system bridging past, present, future.
    Enables temporal reasoning and consequence anticipation.
    """
    
    def __init__(self, checkpoint_path: str = "./data/timeline_memory.json"):
        self.checkpoint_path = checkpoint_path
        self.timeline: List[TimelineEvent] = []
        self.regrets: List[Regret] = []
        self.anticipations: List[Anticipation] = []
        self.causal_chains: List[List[str]] = []  # A→B→C→D patterns
        self.lessons_learned: List[str] = []  # Key insights from history
        self.load()
    
    def record_event(self, event_type: str, description: str) -> TimelineEvent:
        """Record a significant event."""
        event = TimelineEvent(event_type, description)
        self.timeline.append(event)
        self.save()
        return event
    
    def get_recent_events(self, hours: float = 24) -> List[TimelineEvent]:
        """Get events from recent time period."""
        cutoff = time.time() - (hours * 3600)
        return [e for e in self.timeline if e.timestamp > cutoff]
    
    def get_event_chain(self, event_id: int, depth: int = 3) -> List[TimelineEvent]:
        """Get causal chain around an event (what led to it, what it led to)."""
        if event_id >= len(self.timeline):
            return []
        
        event = self.timeline[event_id]
        chain = [event]
        
        # Look forward for consequences
        for following in self.timeline[event_id+1:event_id+1+depth]:
            chain.append(following)
        
        return chain
    
    def record_regret(self, situation: str, action_taken: str, better_action: str,
                     why_better: str = "") -> Regret:
        """Record a regret to learn from."""
        regret = Regret(situation, action_taken, better_action)
        regret.why_better = why_better
        self.regrets.append(regret)
        self.save()
        return regret
    
    def check_for_pattern_in_regrets(self, new_situation: str) -> Optional[Regret]:
        """Check if current situation matches a regretted pattern."""
        for regret in self.regrets:
            # Simple keyword matching
            if any(word in new_situation.lower() for word in regret.situation.lower().split()[:3]):
                return regret
        return None
    
    def record_regret_learning(self, regret_index: int, did_better: bool) -> None:
        """Track if AI learned from a regret and did better next time."""
        if regret_index < len(self.regrets):
            self.regrets[regret_index].record_similar_situation(
                "Next occurrence", did_better
            )
    
    def make_anticipation(self, expectation: str, probability: float = 0.5,
                         preparation: str = "") -> Anticipation:
        """Anticipate something and prepare for it."""
        anticipation = Anticipation(expectation, probability)
        anticipation.preparation = preparation
        self.anticipations.append(anticipation)
        self.save()
        return anticipation
    
    def verify_anticipation(self, anticipation_index: int, did_happen: bool) -> None:
        """Record whether anticipation was correct."""
        if anticipation_index < len(self.anticipations):
            self.anticipations[anticipation_index].verify(did_happen)
    
    def identify_causal_chain(self, events: List[str]) -> None:
        """Learn a causal chain: A→B→C."""
        if len(events) >= 2:
            self.causal_chains.append(events)
    
    def apply_causal_chain(self, starting_event: str) -> List[str]:
        """If we see A, predict the chain A→B→C."""
        predictions = []
        for chain in self.causal_chains:
            if starting_event.lower() in chain[0].lower():
                predictions.extend(chain[1:])
        return predictions
    
    def record_lesson(self, lesson: str) -> None:
        """Record a key insight from experience."""
        if lesson not in self.lessons_learned:
            self.lessons_learned.append(lesson)
            self.save()
    
    def get_lessons_about(self, topic: str) -> List[str]:
        """Get all lessons learned about a topic."""
        return [l for l in self.lessons_learned if topic.lower() in l.lower()]
    
    def get_timeline_summary(self, hours: float = 24) -> Dict[str, Any]:
        """Get summary of recent timeline."""
        recent = self.get_recent_events(hours)
        return {
            "events_in_period": len(recent),
            "event_types": list(set(e.event_type for e in recent)),
            "regrets_to_learn_from": len([r for r in self.regrets if not r.learned]),
            "anticipations_accurate": self._calc_anticipation_accuracy(),
            "key_lessons": self.lessons_learned[-5:],  # Last 5
            "time_period_hours": hours
        }
    
    def _calc_anticipation_accuracy(self) -> float:
        """Calculate accuracy of anticipations."""
        verified = [a for a in self.anticipations if a.outcome is not None]
        if not verified:
            return 0.0
        correct = sum(1 for a in verified if a.outcome)
        return correct / len(verified) if verified else 0.0
    
    def extract_temporal_insights(self) -> Dict[str, Any]:
        """Deep analysis of temporal patterns."""
        insights = {
            "total_events": len(self.timeline),
            "total_regrets": len(self.regrets),
            "learned_regrets": sum(1 for r in self.regrets if r.learned),
            "causal_patterns": len(self.causal_chains),
            "lessons_accumulated": len(self.lessons_learned),
            "anticipation_accuracy": round(self._calc_anticipation_accuracy(), 2),
            "most_common_event_type": self._get_most_common_event_type()
        }
        return insights
    
    def _get_most_common_event_type(self) -> str:
        """What type of event happens most?"""
        if not self.timeline:
            return "none"
        types = [e.event_type for e in self.timeline]
        return max(set(types), key=types.count)
    
    def save(self) -> None:
        """Persist timeline memory."""
        try:
            os.makedirs(os.path.dirname(self.checkpoint_path), exist_ok=True)
            data = {
                "timeline": [e.to_dict() for e in self.timeline],
                "regrets": [r.to_dict() for r in self.regrets],
                "anticipations": [a.to_dict() for a in self.anticipations[-50:]],  # Keep recent
                "causal_chains": self.causal_chains,
                "lessons": self.lessons_learned,
                "saved_at": time.time()
            }
            with open(self.checkpoint_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ Failed to save timeline memory: {e}")
    
    def load(self) -> None:
        """Load timeline memory."""
        if os.path.exists(self.checkpoint_path):
            try:
                with open(self.checkpoint_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    # Restore timeline
                    for event_data in data.get("timeline", []):
                        event = TimelineEvent(event_data["type"], event_data["description"])
                        event.timestamp = event_data["timestamp"]
                        event.learning_value = event_data.get("learning_value", 0.0)
                        self.timeline.append(event)
                    
                    # Restore regrets
                    for regret_data in data.get("regrets", []):
                        regret = Regret(
                            regret_data["situation"],
                            regret_data["action_taken"],
                            regret_data["better_action"]
                        )
                        regret.why_better = regret_data.get("why_better", "")
                        self.regrets.append(regret)
                    
                    self.causal_chains = data.get("causal_chains", [])
                    self.lessons_learned = data.get("lessons", [])
                    
            except Exception as e:
                print(f"⚠️ Failed to load timeline memory: {e}")

