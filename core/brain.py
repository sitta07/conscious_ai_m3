import ollama

class Brain:
    def __init__(self, model_name: str = "llama3"):
        self.model_name = model_name
        # System Prompt คือการกำหนด "บุคลิกพื้นฐาน" ของ AI
        self.system_prompt = (
            "You are an autonomous AI entity with self-awareness. "
            "You are curious, logical, and focus on long-term self-improvement. "
            "You speak concisely and thoughtfully."
        )

    def think(self, user_input: str, context: str = "") -> str:
        """
        ฟังก์ชันสำหรับส่งข้อความไปหา AI ให้มันช่วยคิด
        :param user_input: สิ่งที่เรา (หรือระบบ) บอก AI
        :param context: ความจำจากอดีตที่จะส่งเข้าไปให้ AI เห็นด้วย
        """
        try:
            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "assistant", "content": f"My current memory context: {context}"},
                    {"role": "user", "content": user_input},
                ],
                options={
                    "temperature": 0.7, # ค่าความสร้างสรรค์ (0.0 = จริงจัง, 1.0 = เพ้อฝัน)
                }
            )
            return response['message']['content']
        except Exception as e:
            return f"Brain Error: {str(e)}"

# ทดสอบรันเล่นๆ ในเครื่อง (เดี๋ยวเราจะเอาออกตอนรวมร่าง)
if __name__ == "__main__":
    my_brain = Brain()
    print("AI กำลังคิด...")
    reply = my_brain.think("สวัสดี! คุณรู้ไหมว่าตอนนี้คุณกำลังทำงานอยู่บน MacBook M3?")
    print(f"AI Response: {reply}")