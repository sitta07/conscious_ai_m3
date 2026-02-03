import time
import random
import ollama
import json
import os
from typing import List, Optional, Tuple, Dict

class Goal:
    """Represents a single goal with metadata."""
    def __init__(self, name: str, priority: str = "normal", timestamp: float = None):
        self.name = name
        self.priority = priority
        self.timestamp = timestamp or time.time()
        self.completed = False

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "priority": self.priority,
            "timestamp": self.timestamp,
            "completed": self.completed
        }

    @staticmethod
    def from_dict(data: Dict) -> 'Goal':
        goal = Goal(data["name"], data.get("priority", "normal"), data.get("timestamp"))
        goal.completed = data.get("completed", False)
        return goal


class GoalStack:
    """Stack-based goal management with persistence."""
    
    def __init__(self, stack_path: str = "./data/goal_stack.json"):
        self.stack: List[Goal] = []
        self.stack_path = stack_path
        self.completed_goals: List[Goal] = []
        self.load()

    def push_goal(self, goal_name: str, priority: str = "normal") -> None:
        """Add goal to stack (sub-goal without forgetting parent)."""
        goal = Goal(goal_name, priority)
        self.stack.append(goal)
        self.save()
        print(f"📌 Goal pushed: {goal_name} (priority: {priority})")

    def pop_goal(self) -> Optional[Goal]:
        """Complete and remove top goal from stack."""
        if self.stack:
            goal = self.stack.pop()
            goal.completed = True
            self.completed_goals.append(goal)
            self.save()
            print(f"✅ Goal completed: {goal.name}")
            return goal
        return None

    def get_active_goal(self) -> Optional[str]:
        """Get current top goal (what am I doing?)."""
        if self.stack:
            return self.stack[-1].name
        return "IDLE"

    def has_active_goal(self) -> bool:
        """Check if there's an active goal."""
        return len(self.stack) > 0

    def get_goal_hierarchy(self) -> List[str]:
        """Get all goals from bottom to top."""
        return [g.name for g in self.stack]

    def interrupt_current_goal(self, new_goal: str) -> None:
        """Push urgent goal without removing current one."""
        self.push_goal(new_goal, priority="high")

    def resume_last_incomplete(self) -> Optional[str]:
        """Try to resume the most recent incomplete goal."""
        if self.stack:
            return self.get_active_goal()
        return None

    def clear_goals(self) -> None:
        """Clear all active goals (reset)."""
        self.stack.clear()
        self.save()

    def get_goal_duration(self, goal: Goal) -> float:
        """How long has this goal been active? (in seconds)"""
        if goal in self.stack:
            return time.time() - goal.timestamp
        return 0.0

    def save(self) -> None:
        """Persist goal stack to disk."""
        try:
            os.makedirs(os.path.dirname(self.stack_path), exist_ok=True)
            data = {
                "active_goals": [g.to_dict() for g in self.stack],
                "completed_goals": [g.to_dict() for g in self.completed_goals[-20:]]
            }
            with open(self.stack_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ Failed to save goal stack: {e}")

    def load(self) -> bool:
        """Load goal stack from disk."""
        if os.path.exists(self.stack_path):
            try:
                with open(self.stack_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.stack = [Goal.from_dict(g) for g in data.get("active_goals", [])]
                    self.completed_goals = [Goal.from_dict(g) for g in data.get("completed_goals", [])]
                    return True
            except Exception as e:
                print(f"⚠️ Failed to load goal stack: {e}")
        return False


class GoalSystem:
    def __init__(self):
        self.current_goal = "IDLE"
        self.model_name = "llama3.1"
        self.goal_stack = GoalStack()
        
    def evaluate_goal(self, state_data: dict, memory_context: str = "") -> str:
        """
        ตัดสินใจ Goal แบบ Hybrid:
        - Critical -> ใช้ Code (Reflex)
        - Resume -> ใช้ Goal Stack
        - Normal -> ใช้ AI คิด (Reasoning)
        """
        energy = state_data.get("energy", 100)
        happiness = state_data.get("happiness", 50)
        
        # --- 1. REFLEX LAYER (สัญชาตญาณความอยู่รอด) ---
        if energy < 15:
            self.goal_stack.push_goal("CRITICAL_SLEEP", priority="critical")
            return "CRITICAL_SLEEP"
        if energy < 30:
            return "NEED_REST"

        # --- 2. RESUME LAYER (ทำไม่เสร็จจากครั้งที่แล้ว?) ---
        active_goal = self.goal_stack.get_active_goal()
        if active_goal != "IDLE":
            for goal in self.goal_stack.stack:
                if goal.name == active_goal:
                    duration = self.goal_stack.get_goal_duration(goal)
                    if duration < 600:
                        return active_goal

        # --- 3. REASONING LAYER (ความคิดอิสระ) ---
        prompt = (
            f"You are a conscious AI with these internal stats:\n"
            f"- Energy: {energy}% (Lower means tired)\n"
            f"- Happiness: {happiness}% (Lower means bored/sad)\n"
            f"- Recent Memories: {memory_context}\n"
            f"- Active Goal Stack: {self.goal_stack.get_goal_hierarchy()}\n"
            f"\n"
            f"Based on this state, what do you WANT to do right now?\n"
            f"Choose ONE goal from: [SEEK_ATTENTION, COMPLAIN, EXPRESS_JOY, REFLECT_ON_LIFE, IDLE].\n"
            f"Or INVENT a new short goal phrase if appropriate.\n"
            f"Reply ONLY with the Goal Name."
        )

        try:
            response = ollama.chat(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                options={"temperature": 0.7} 
            )
            generated_goal = response['message']['content'].strip().upper()
            
            if len(generated_goal) > 30: 
                return "IDLE"
            
            generated_goal = generated_goal.replace(".", "").replace('"', "")
            
            if generated_goal != "IDLE":
                self.goal_stack.push_goal(generated_goal, priority="normal")
            
            return generated_goal
            
        except Exception as e:
            print(f"⚠️ Goal Error: {e}")
            return "IDLE"

    def get_action_for_goal(self, goal: str) -> str:
        """
        แปลง Goal เป็น Action
        """
        if goal == "CRITICAL_SLEEP":
            return "SYSTEM_ACTION: SLEEP_NOW"
        elif goal == "NEED_REST":
            return "ไม่ไหวแล้ว... ขอนอนชาร์จแบตแป๊บนะ"
        elif goal == "IDLE":
            return None

        prompt = (
            f"Your current goal is: '{goal}'.\n"
            f"Write a short, natural Thai sentence to express this goal to the user.\n"
            f"No explanations. Just the sentence."
        )
        
        try:
            res = ollama.chat(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                options={"temperature": 0.8}
            )
            return res['message']['content']
        except:
            return "..."

    def complete_current_goal(self) -> None:
        """Mark current goal as done."""
        self.goal_stack.pop_goal()