import time
import random
import ollama
import json

class GoalSystem:
    def __init__(self):
        self.current_goal = "IDLE"
        self.model_name = "llama3.1" # ใช้สมองส่วนหน้าคิด
        
    def evaluate_goal(self, state_data: dict, memory_context: str = "") -> str:
        """
        ตัดสินใจ Goal แบบ Hybrid:
        - Critical -> ใช้ Code (Reflex)
        - Normal -> ใช้ AI คิด (Reasoning)
        """
        energy = state_data.get("energy", 100)
        happiness = state_data.get("happiness", 50)
        
        # --- 1. REFLEX LAYER (สัญชาตญาณความอยู่รอด) ---
        # กฎเหล็ก: ถ้าจะตาย ต้องนอนก่อน ห้ามคิดเยอะ
        if energy < 15:
            return "CRITICAL_SLEEP"
        if energy < 30:
            return "NEED_REST"

        # --- 2. REASONING LAYER (ความคิดอิสระ) ---
        # ถ้าพลังงานเหลือเฟือ ให้ AI ตัดสินใจเองตามสถานการณ์ (นี่แหละคือ Branching!)
        
        prompt = (
            f"You are a conscious AI with these internal stats:\n"
            f"- Energy: {energy}% (Lower means tired)\n"
            f"- Happiness: {happiness}% (Lower means bored/sad)\n"
            f"- Recent Memories: {memory_context}\n"
            f"\n"
            f"Based on this state, what do you WANT to do right now?\n"
            f"Choose ONE goal from: [SEEK_ATTENTION, COMPLAIN, EXPRESS_JOY, REFLECT_ON_LIFE, IDLE].\n"
            f"Or INVENT a new short goal phrase if appropriate.\n"
            f"Reply ONLY with the Goal Name."
        )

        try:
            # ใช้ Temp สูงหน่อย (0.7) เพื่อให้มีความคิดสร้างสรรค์ (Randomness)
            response = ollama.chat(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                options={"temperature": 0.7} 
            )
            generated_goal = response['message']['content'].strip().upper()
            
            # กรองคำตอบหน่อย เผื่อมันตอบยาวเกิน
            if len(generated_goal) > 30: 
                return "IDLE"
            
            # Clean up (ตัดจุด ตัด quote)
            generated_goal = generated_goal.replace(".", "").replace('"', "")
            
            return generated_goal
            
        except Exception as e:
            print(f"⚠️ Goal Error: {e}")
            return "IDLE"

    def get_action_for_goal(self, goal: str) -> str:
        """
        แปลง Goal เป็น Action (คราวนี้ให้ AI คิดคำพูดเองด้วย!)
        """
        # Hard-coded Actions (สำหรับเรื่องพื้นฐาน)
        if goal == "CRITICAL_SLEEP":
            return "SYSTEM_ACTION: SLEEP_NOW"
        elif goal == "NEED_REST":
            return "ไม่ไหวแล้ว... ขอนอนชาร์จแบตแป๊บนะ"
        elif goal == "IDLE":
            return None

        # Generative Actions (สำหรับ Goal ที่ AI คิดเอง)
        # ให้ AI แต่งประโยคเองเลยว่าอยากพูดอะไรตาม Goal นั้น
        prompt = (
            f"Your current goal is: '{goal}'.\n"
            f"Write a short, natural Thai sentence to express this goal to the user.\n"
            f"No explanations. Just the sentence."
        )
        
        try:
            res = ollama.chat(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                options={"temperature": 0.8} # ใส่ความอาร์ตลงไป
            )
            return res['message']['content']
        except:
            return "..."