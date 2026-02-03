"""
Layer 6: Emotion Simulator (ความรู้สึก)

NOT real emotion, but functional state machine that:
1. Accelerates decisions
2. Weights priorities  
3. Modulates behavior

Key emotions:
- CURIOSITY: Drives exploration
- FEAR: Triggers caution
- SATISFACTION: Enables rest
- FRUSTRATION: Triggers strategy change
- CONFUSION: Slows down, requests clarification

Without emotions: AI is cold and purely logical
With emotions: AI has natural decision weights and exploration drive
"""

import json
import time
import os
from typing import Dict, List, Any, Optional
from enum import Enum

class EmotionState(Enum):
    """Functional emotions affecting decision-making."""
    NEUTRAL = "neutral"
    CURIOUS = "curious"
    FEARFUL = "fearful"
    SATISFIED = "satisfied"
    FRUSTRATED = "frustrated"
    CONFUSED = "confused"
    DETERMINED = "determined"


class Emotion:
    """A functional emotion with intensity and effects."""
    def __init__(self, emotion_type: EmotionState, intensity: float = 0.5):
        self.emotion_type = emotion_type
        self.intensity = max(0.0, min(1.0, intensity))  # 0.0-1.0
        self.triggered_at = time.time()
        self.trigger_source = ""  # What caused this?
        self.duration = 300  # How long it lasts (seconds)
    
    def is_active(self) -> bool:
        """Check if emotion is still active."""
        age = time.time() - self.triggered_at
        return age < self.duration
    
    def decay(self) -> float:
        """Emotion naturally decays over time."""
        age = time.time() - self.triggered_at
        decay_factor = max(0.0, 1.0 - (age / self.duration))
        self.intensity *= decay_factor
        return self.intensity
    
    def get_decision_modifier(self) -> Dict[str, float]:
        """How this emotion modifies decision-making (0.5 = neutral, 2.0 = extreme)."""
        modifiers = {
            "exploration_weight": 0.5,  # How likely to explore
            "safety_weight": 0.5,       # Caution level
            "speed_weight": 0.5,        # Urgency
            "patience_weight": 0.5      # Willing to wait/think
        }
        
        if self.emotion_type == EmotionState.CURIOUS:
            modifiers["exploration_weight"] = 1.0 + (self.intensity * 1.0)
            modifiers["patience_weight"] = 1.0 + (self.intensity * 0.5)
            
        elif self.emotion_type == EmotionState.FEARFUL:
            modifiers["safety_weight"] = 1.0 + (self.intensity * 2.0)
            modifiers["speed_weight"] = 0.5 + (self.intensity * 1.5)
            modifiers["exploration_weight"] = 0.5 - (self.intensity * 0.3)
            
        elif self.emotion_type == EmotionState.SATISFIED:
            modifiers["patience_weight"] = 1.0 + (self.intensity * 1.0)
            modifiers["speed_weight"] = 0.5 - (self.intensity * 0.3)
            
        elif self.emotion_type == EmotionState.FRUSTRATED:
            modifiers["speed_weight"] = 1.0 + (self.intensity * 1.5)
            modifiers["patience_weight"] = 0.5 - (self.intensity * 0.5)
            # Might try different strategy
            modifiers["strategy_change_likelihood"] = self.intensity
            
        elif self.emotion_type == EmotionState.CONFUSED:
            modifiers["speed_weight"] = 0.3  # Slow down
            modifiers["patience_weight"] = 2.0  # Take time
            modifiers["safety_weight"] = 1.5  # Be careful
        
        return modifiers
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "emotion": self.emotion_type.value,
            "intensity": round(self.intensity, 2),
            "triggered_at": self.triggered_at,
            "source": self.trigger_source,
            "active": self.is_active()
        }


class EmotionalSystem:
    """
    Manages functional emotions affecting AI decision-making.
    Emotions are NOT feelings, but decision accelerators.
    """
    
    def __init__(self, checkpoint_path: str = "./data/emotions.json"):
        self.checkpoint_path = checkpoint_path
        self.emotions: List[Emotion] = []
        self.mood = 0.5  # 0.0 = negative, 1.0 = positive
        self.arousal = 0.5  # 0.0 = calm, 1.0 = excited
        self.emotion_history = []  # Track emotions over time
        self.load()
    
    def trigger_emotion(self, emotion_type: EmotionState, intensity: float, 
                       source: str = "") -> Emotion:
        """Trigger an emotion (or reinforce if already active)."""
        # Check if emotion already active
        for e in self.emotions:
            if e.emotion_type == emotion_type and e.is_active():
                # Reinforce: increase intensity
                e.intensity = min(1.0, e.intensity + intensity * 0.3)
                return e
        
        # Create new emotion
        emotion = Emotion(emotion_type, intensity)
        emotion.trigger_source = source
        self.emotions.append(emotion)
        
        # Log
        self.emotion_history.append({
            "timestamp": time.time(),
            "emotion": emotion_type.value,
            "intensity": intensity,
            "source": source
        })
        
        self._update_mood_arousal()
        self.save()
        return emotion
    
    def trigger_curiosity(self, topic: str, interest_level: float = 0.6) -> None:
        """Trigger curiosity about something."""
        self.trigger_emotion(
            EmotionState.CURIOUS,
            interest_level,
            f"Curious about: {topic}"
        )
    
    def trigger_fear(self, risk: str, severity: float = 0.7) -> None:
        """Trigger fear about a risk."""
        self.trigger_emotion(
            EmotionState.FEARFUL,
            severity,
            f"Fear of: {risk}"
        )
    
    def trigger_satisfaction(self, accomplishment: str, magnitude: float = 0.7) -> None:
        """Trigger satisfaction about accomplishment."""
        self.trigger_emotion(
            EmotionState.SATISFIED,
            magnitude,
            f"Satisfied with: {accomplishment}"
        )
    
    def trigger_frustration(self, obstacle: str, difficulty: float = 0.6) -> None:
        """Trigger frustration about obstacle."""
        self.trigger_emotion(
            EmotionState.FRUSTRATED,
            difficulty,
            f"Frustrated by: {obstacle}"
        )
    
    def trigger_confusion(self, issue: str, severity: float = 0.5) -> None:
        """Trigger confusion about something."""
        self.trigger_emotion(
            EmotionState.CONFUSED,
            severity,
            f"Confused about: {issue}"
        )
    
    def get_decision_weights(self) -> Dict[str, float]:
        """
        Get current decision weights based on active emotions.
        Higher values = more weight to that factor.
        """
        weights = {
            "exploration": 0.5,
            "safety": 0.5,
            "speed": 0.5,
            "patience": 0.5
        }
        
        # Apply modifiers from all active emotions
        for emotion in self.emotions:
            if emotion.is_active():
                emotion.decay()
                modifiers = emotion.get_decision_modifier()
                weights["exploration"] *= modifiers.get("exploration_weight", 1.0)
                weights["safety"] *= modifiers.get("safety_weight", 1.0)
                weights["speed"] *= modifiers.get("speed_weight", 1.0)
                weights["patience"] *= modifiers.get("patience_weight", 1.0)
        
        # Normalize
        total = sum(weights.values())
        if total > 0:
            weights = {k: v/total for k, v in weights.items()}
        
        return weights
    
    def _update_mood_arousal(self) -> None:
        """Update mood and arousal based on active emotions."""
        positive_emotions = 0
        negative_emotions = 0
        total_arousal = 0
        
        for emotion in self.emotions:
            if not emotion.is_active():
                continue
            
            if emotion.emotion_type in [EmotionState.SATISFIED, EmotionState.CURIOUS]:
                positive_emotions += emotion.intensity
            elif emotion.emotion_type in [EmotionState.FRUSTRATED, EmotionState.FEARFUL]:
                negative_emotions += emotion.intensity
            
            if emotion.emotion_type in [EmotionState.FRUSTRATED, EmotionState.CURIOUS, EmotionState.FEARFUL]:
                total_arousal += emotion.intensity
        
        # Update mood (weighted average)
        self.mood = (positive_emotions - negative_emotions) / 2.0 + 0.5
        self.mood = max(0.0, min(1.0, self.mood))
        
        # Update arousal
        self.arousal = total_arousal / 3.0 if (positive_emotions + negative_emotions) > 0 else 0.5
        self.arousal = max(0.0, min(1.0, self.arousal))
    
    def get_emotional_state(self) -> Dict[str, Any]:
        """Get current emotional status."""
        active = [e for e in self.emotions if e.is_active()]
        
        return {
            "mood": round(self.mood, 2),
            "arousal": round(self.arousal, 2),
            "active_emotions": [e.to_dict() for e in active],
            "decision_weights": self.get_decision_weights(),
            "mood_description": self._describe_mood()
        }
    
    def _describe_mood(self) -> str:
        """Human-readable mood description."""
        if self.mood > 0.7 and self.arousal > 0.6:
            return "EXCITED"
        elif self.mood > 0.7:
            return "CONTENT"
        elif self.mood > 0.5 and self.arousal < 0.4:
            return "PEACEFUL"
        elif self.mood > 0.5:
            return "NEUTRAL"
        elif self.mood > 0.3 and self.arousal > 0.6:
            return "ANXIOUS"
        elif self.mood > 0.3:
            return "DISCOURAGED"
        else:
            return "DISTRESSED"
    
    def get_recommended_action(self) -> str:
        """What should AI do based on current emotions?"""
        state = self.get_emotional_state()
        
        # Get strongest active emotion
        if not state["active_emotions"]:
            return "Continue normally"
        
        strongest = state["active_emotions"][0]
        emotion = strongest["emotion"]
        
        if emotion == "curious":
            return "Explore and ask questions about the topic"
        elif emotion == "fearful":
            return "Verify assumptions and check for risks before proceeding"
        elif emotion == "satisfied":
            return "Take time to reflect on accomplishment"
        elif emotion == "frustrated":
            return "Try a different approach or ask for help"
        elif emotion == "confused":
            return "Ask for clarification and slow down"
        else:
            return "Proceed with caution"
    
    def cleanup_inactive(self) -> None:
        """Remove emotions that have fully decayed."""
        self.emotions = [e for e in self.emotions if e.is_active()]
        self._update_mood_arousal()
    
    def save(self) -> None:
        """Persist emotional state."""
        try:
            os.makedirs(os.path.dirname(self.checkpoint_path), exist_ok=True)
            data = {
                "current_emotions": [e.to_dict() for e in self.emotions],
                "mood": self.mood,
                "arousal": self.arousal,
                "emotion_history": self.emotion_history[-100:],  # Keep last 100
                "saved_at": time.time()
            }
            with open(self.checkpoint_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ Failed to save emotions: {e}")
    
    def load(self) -> None:
        """Load emotional state."""
        if os.path.exists(self.checkpoint_path):
            try:
                with open(self.checkpoint_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.mood = data.get("mood", 0.5)
                    self.arousal = data.get("arousal", 0.5)
                    self.emotion_history = data.get("emotion_history", [])
                    # Note: emotions are not fully restored as they decay over time
            except Exception as e:
                print(f"⚠️ Failed to load emotions: {e}")

