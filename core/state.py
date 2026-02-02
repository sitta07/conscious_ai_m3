import time
import random
import json
import os

class State:
    def __init__(self, checkpoint_path: str = "./data/state_checkpoint.json"):
        self.checkpoint_path = checkpoint_path
        
        # ลองโหลดสถานะเดิม (ถ้ามี)
        if self.load():
            print("📦 Loaded previous state (Identity restored).")
        else:
            print("🐣 Creating new identity (First born).")
            self.energy = 100.0
            self.happiness = 50.0
            self.personality_drift = 0.0 # ค่าความเปลี่ยนแปลงของนิสัย (อนาคตใช้)
        
        self.last_update = time.time()
        
    def update(self, action_type: str):
        """อัปเดตและบันทึกทันที (Auto-save)"""
        current_time = time.time()
        
        if action_type == "talk":
            self.energy -= 2.0
            self.happiness += random.uniform(-1, 2)
        elif action_type == "sleep":
            self.energy = 100.0
            self.happiness += 5.0 # นอนแล้วอารมณ์ดีขึ้นนิดนึง
            
        # Clamp Values
        self.energy = max(0, min(100, self.energy))
        self.happiness = max(0, min(100, self.happiness))
        
        self.last_update = current_time
        self.save() # <--- Save ทุกครั้งที่มีการเปลี่ยนแปลง

    def get_status(self) -> dict:
        return {
            "energy": round(self.energy, 1),
            "happiness": round(self.happiness, 1),
            "status_description": self._describe_state()
        }

    def _describe_state(self) -> str:
        # (ใช้ Logic เดิมแบบ Loyal Mode)
        if self.energy < 20:
            return "EXHAUSTED (Obey but complain heavily)"
        elif self.energy < 50:
            return "TIRED (Obey but lazy/short)"
        elif self.happiness < 30:
            return "GRUMPY (Sarcastic/Passive-aggressive)"
        elif self.happiness > 70:
            return "EXCITED (Enthusiastic)"
        else:
            return "NEUTRAL (Professional)"

    def save(self):
        """บันทึกตัวตนลงไฟล์ JSON"""
        data = {
            "energy": self.energy,
            "happiness": self.happiness,
            "last_active": time.time()
        }
        try:
            with open(self.checkpoint_path, 'w') as f:
                json.dump(data, f)
        except Exception as e:
            print(f"⚠️ Failed to save state: {e}")

    def load(self) -> bool:
        """กู้คืนตัวตนจากไฟล์"""
        if os.path.exists(self.checkpoint_path):
            try:
                with open(self.checkpoint_path, 'r') as f:
                    data = json.load(f)
                    self.energy = data.get("energy", 100.0)
                    self.happiness = data.get("happiness", 50.0)
                    
                    # คำนวณเวลาที่หายไป (Time Decay)
                    # เช่น ถ้าปิดคอมไป 10 ชม. พลังงานควรฟื้น หรือลดลง?
                    # เฟสนี้เอาแค่โหลดค่าเดิมมาก่อน
                    return True
            except Exception as e:
                print(f"⚠️ Corrupted save file: {e}")
        return False