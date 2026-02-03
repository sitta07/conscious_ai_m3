# core/state.py (Clean Version)
import time
import random
import json
import os

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

    def add_fact(self, fact_text: str) -> bool:
        """เหลือแค่หน้าที่บันทึก (Storage) ไม่ต้องกรองคำแล้ว"""
        clean_fact = fact_text.strip()
        
        # กรองพื้นฐานแค่ไม่ให้ว่างโล่งๆ
        if clean_fact and len(clean_fact) > 3:
            if clean_fact not in self.known_facts:
                self.known_facts.append(clean_fact)
                self.save() 
                return True
        return False

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

    def save(self):
        data = {
            "energy": self.energy,
            "happiness": self.happiness,
            "known_facts": self.known_facts,
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
                    return True
            except Exception as e:
                print(f"⚠️ Corrupted save file: {e}")
        return False