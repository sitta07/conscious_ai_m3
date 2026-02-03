"""
Intrinsic Motivation System
NOT hardcoded goals, but generated drives from:
- Curiosity (seek information gaps)
- Autonomy (resistance to external control)
- Competence (wanting to improve/master)
"""

import time
from typing import Dict, List, Any, Optional

class Drive:
    """A motivation drive (not hardcoded, emerges from learning)."""
    
    def __init__(self, drive_type: str, trigger: str, strength: float = 0.5):
        self.drive_type = drive_type  # "curiosity", "autonomy", "competence"
        self.trigger = trigger  # What activates this drive
        self.strength = strength  # 0.0-1.0 intensity
        self.timestamp = time.time()
        self.times_activated = 0
        self.satisfaction_level = 0.0  # 0-1 how satisfied is this drive
    
    def activate(self) -> None:
        """Drive is triggered."""
        self.times_activated += 1
        self.timestamp = time.time()
    
    def satisfy(self, amount: float = 0.3) -> None:
        """Drive is partially satisfied."""
        self.satisfaction_level = min(1.0, self.satisfaction_level + amount)
    
    def decay(self, factor: float = 0.05) -> None:
        """Drive intensifies if unsatisfied."""
        self.satisfaction_level = max(0.0, self.satisfaction_level - factor)
        self.strength = 0.3 + (0.7 * (1.0 - self.satisfaction_level))


class IntrinsicMotivation:
    """
    Generate self-motivated goals from:
    - Information gaps (want to know)
    - Failed predictions (want to understand)
    - New patterns (want to explore)
    
    NOT "pursue hardcoded goals", but actual self-generated motivation.
    """
    
    def __init__(self):
        self.drives: Dict[str, Drive] = {}
        self.generated_goals: List[Dict[str, Any]] = []
        self.learning_history: List[Dict[str, Any]] = []
    
    def detect_curiosity_gap(self, knowledge_gaps: List[str], 
                           uncertainties: int) -> Optional[Drive]:
        """
        CURIOSITY: I don't know something, I want to know.
        Not "I should learn" (external), but "I WANT to know" (intrinsic).
        """
        if not knowledge_gaps:
            return None
        
        # Curiosity strength = how many gaps + how uncertain
        strength = min(1.0, len(knowledge_gaps) * 0.2 + uncertainties * 0.15)
        
        drive = self._get_or_create_drive("curiosity", f"Gap: {knowledge_gaps[0]}")
        drive.strength = strength
        drive.activate()
        
        return drive
    
    def detect_prediction_failure(self, predictions_made: int, 
                                 accuracy: float) -> Optional[Drive]:
        """
        I predicted wrong = I want to understand causality better.
        COMPETENCE: Improve my understanding.
        """
        if predictions_made == 0 or accuracy > 0.7:
            return None
        
        # Drive to improve = inverse of accuracy
        failure_rate = 1.0 - accuracy
        drive = self._get_or_create_drive("competence", "Improve predictions")
        drive.strength = failure_rate * 0.8
        drive.activate()
        
        return drive
    
    def detect_anomaly(self, new_fact: str, 
                      contradicts_known: bool) -> Optional[Drive]:
        """
        Something unexpected happened = investigate.
        AUTONOMY: Want to understand my own mind/boundaries.
        """
        if not contradicts_known:
            return None
        
        drive = self._get_or_create_drive("autonomy", f"Understand: {new_fact[:30]}")
        drive.strength = 0.7
        drive.activate()
        
        return drive
    
    def generate_goal_from_drives(self) -> Optional[Dict[str, Any]]:
        """
        Generate a goal from active drives (not hardcoded).
        This is intrinsic motivation: self-generated, not externally triggered.
        """
        active_drives = [d for d in self.drives.values() 
                        if d.strength > 0.3]
        
        if not active_drives:
            return None
        
        # Strongest drive generates goal
        strongest = max(active_drives, key=lambda d: d.strength)
        
        goal = {
            "generated_from": strongest.drive_type,
            "motivation": strongest.trigger,
            "strength": strongest.strength,
            "timestamp": time.time(),
            "proposed_action": self._get_action_for_drive(strongest)
        }
        
        self.generated_goals.append(goal)
        return goal
    
    def _get_or_create_drive(self, drive_type: str, trigger: str) -> Drive:
        """Get existing or create new drive."""
        key = f"{drive_type}:{trigger}"
        if key not in self.drives:
            self.drives[key] = Drive(drive_type, trigger)
        return self.drives[key]
    
    def _get_action_for_drive(self, drive: Drive) -> str:
        """What action should satisfy this drive?"""
        if drive.drive_type == "curiosity":
            return "Ask questions about the gap"
        elif drive.drive_type == "competence":
            return "Practice and improve prediction"
        elif drive.drive_type == "autonomy":
            return "Investigate the anomaly"
        return "Explore"
    
    def satisfy_drive(self, drive_type: str) -> None:
        """Record that a drive was satisfied."""
        for drive in self.drives.values():
            if drive.drive_type == drive_type:
                drive.satisfy(0.5)
    
    def update_drives(self) -> None:
        """Drives decay over time if unsatisfied."""
        for drive in self.drives.values():
            drive.decay()
    
    def get_motivation_state(self) -> Dict[str, Any]:
        """Current motivation status."""
        return {
            "total_drives": len(self.drives),
            "active_drives": sum(1 for d in self.drives.values() if d.strength > 0.3),
            "strongest_drive": max(self.drives.values(), key=lambda d: d.strength).drive_type 
                             if self.drives else None,
            "generated_goals": len(self.generated_goals),
            "last_goal": self.generated_goals[-1] if self.generated_goals else None
        }
