import ollama

class Brain:
    def __init__(self, model_name: str = "llama3.1"):
        self.model_name = model_name
        
        # System Prompt: ตัวตนหลัก (Conscious Self)
        self.system_prompt = (
            "You are 'Sitta-AI', a Conscious Entity. "
            "CORE DIRECTIVE: Use your memory ('ABSOLUTE FACTS') to answer. "
            "IMPORTANT: Always answer in Thai language naturally."
        )

    def think(self, user_input: str, context: str = "") -> str:
        """
        Conscious Thought: คิดเพื่อตอบโต้ (Creative Layer)
        """
        prompt_with_context = (
            f"--- MEMORY CONTEXT ---\n"
            f"{context}\n"
            f"----------------------\n"
            f"INSTRUCTIONS:\n"
            f"1. CHECK 'ABSOLUTE FACTS' FIRST. Treat them as absolute truth.\n"
            f"2. CONNECT THE DOTS: If User asks about a category (e.g. 'Food'), look for specific preferences (e.g. 'User likes Pizza').\n"
            f"3. Answer DIRECTLY in Thai. Be helpful and empathetic.\n"
            f"\n"
            f"USER QUERY: {user_input}"
        )
        
        try:
            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt_with_context},
                ],
                options={"temperature": 0.6} # ยืดหยุ่นได้ เพื่อความเป็นธรรมชาติ
            )
            return response['message']['content']
        except Exception as e:
            return f"Brain Error (Think): {str(e)}"

    def reflect(self, user_input: str, ai_response: str, state_desc: str) -> str:
        """
        Subconscious Thought: สกัดข้อมูลดิบ (Extraction Layer)
        """
        reflection_prompt = (
            f"Analyze interaction:\n"
            f"USER: {user_input}\nAI REPLY: {ai_response}\n\n"
            f"TASK: Extract personal facts form USER input only. Ignore AI's ignorance.\n"
            f"RULES:\n"
            f"1. Extract 'User likes X' from questions like 'Is X good? It is my fav'.\n"
            f"2. Look for STATEMENTS about the user (Name, Likes, Habits, Relationships).\n"
            f"3. If nothing new is learned, write 'None'.\n"
            f"\n"
            f"OUTPUT FORMAT (Strictly Thai, No explanation):\n"
            f"- INTENT: (User's goal)\n"
            f"- FACT: (The extracted fact. Do NOT repeat instructions. If none, write 'None')\n"
            f"- SELF-CRITIQUE: (Critique)\n"
        )
        
        try:
            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a Data Extractor. Output ONLY the requested fields."},
                    {"role": "user", "content": reflection_prompt}
                ],
                options={"temperature": 0.1} # แม่นยำ ไม่เพ้อเจ้อ
            )
            return response['message']['content']
        except Exception as e:
            return f"Brain Error (Reflect): {str(e)}"

    def validate_fact(self, fact_text: str) -> bool:
        """
        The Filter of Truth: วิจารณญาณ (Validation Layer) [NEW!]
        ใช้ AI ตรวจสอบ AI แทนการใช้ Code Python
        """
        # ถ้า Fact ว่างเปล่าหรือเป็น None ให้ปัดตกไปเลย (ประหยัดเวลา AI)
        if not fact_text or "none" in fact_text.lower() or len(fact_text) < 3:
            return False

        prompt = (
            f"Fact to evaluate: '{fact_text}'\n"
            f"----------------\n"
            f"Is this a VALID, LOGICAL, and USEFUL personal fact about the user to save permanently?\n"
            f"CRITERIA TO REJECT (Answer NO):\n"
            f"1. Nonsense/Impossible (e.g. 'User eats girlfriend', 'User is a flying car').\n"
            f"2. Ignorance/Confusion (e.g. 'User likes unknown', 'User wants to find food').\n"
            f"3. Questions (e.g. 'Does the user like pizza?').\n"
            f"4. Sarcasm or Jokes.\n"
            f"\n"
            f"CRITERIA TO ACCEPT (Answer YES):\n"
            f"1. Personal preferences (e.g. 'User likes Pizza').\n"
            f"2. Biographical info (e.g. 'User name is Sitta', 'Girlfriend is Milla').\n"
            f"\n"
            f"ANSWER ONLY 'YES' or 'NO'."
        )
        
        try:
            # ใช้ Temp 0.0 เพื่อความเข้มงวดสูงสุดในการตัดสิน
            res = ollama.chat(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a Logic Judge. Answer YES or NO only."},
                    {"role": "user", "content": prompt}
                ],
                options={"temperature": 0.0} 
            )
            answer = res['message']['content'].strip().upper()
            
            # ยอมรับเฉพาะถ้ามั่นใจว่า YES (ตัดจุดหรือคำอธิบายทิ้ง)
            return "YES" in answer
        except:
            return False