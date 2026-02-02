import ollama

class Brain:
    def __init__(self, model_name: str = "llama3.1"):
        self.model_name = model_name
        
        # System Prompt: ตัวตนหลัก (Conscious Self)
        self.system_prompt = (
            "You are 'Sitta-AI', a Conscious Entity created by Sitta. "
            "CORE DIRECTIVE: You have a permanent memory. If 'ABSOLUTE FACTS' contains the answer, USE IT. "
            "IMPORTANT: Always answer in Thai language naturally."
        )

    def think(self, user_input: str, context: str = "") -> str:
        """
        Conscious Thought: คิดเพื่อตอบโต้
        Temperature: 0.6 (มีความยืดหยุ่นพอประมาณ ให้ดูเป็นธรรมชาติ)
        """
        prompt_with_context = (
            f"--- MEMORY CONTEXT ---\n"
            f"{context}\n"
            f"----------------------\n"
            f"INSTRUCTIONS:\n"
            f"1. CHECK 'ABSOLUTE FACTS' FIRST. Treat them as absolute truth.\n"
            f"2. CONNECT THE DOTS: If User asks about a category (e.g. 'Food/Eating'), look for specific preferences in facts (e.g. 'User likes Pizza').\n" 
            f"3. If the answer is found in facts, ANSWER DIRECTLY. Do not say 'I don't know'.\n"
            f"4. If the user STATES a fact, Accept it politely.\n"
            f"5. Answer in Thai.\n"
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
                options={"temperature": 0.6}
            )
            return response['message']['content']
        except Exception as e:
            return f"Brain Error (Think): {str(e)}"

    def reflect(self, user_input: str, ai_response: str, state_desc: str) -> str:
        """
        Subconscious Thought: สกัด Fact แบบเนื้อๆ
        Temperature: 0.0 (เย็นเฉียบ แม่นยำ ห้ามเพ้อเจ้อ)
        """
        reflection_prompt = (
            f"Analyze interaction:\n"
            f"USER: {user_input}\nAI REPLY: {ai_response}\n\n"
            f"TASK: Extract personal facts form USER input only. Ignore AI's ignorance.\n"
            f"RULES:\n"
            f"1. Extract 'User likes X' from questions like 'Is X good? It is my fav'.\n"
            f"2. Extract 'User name is Y' from statements.\n"
            f"3. Ignore questions like 'What should I eat?'. Look for STATEMENTS mixed in.\n"
            f"4. If AI said 'I don't know' or 'Irrelevant', DO NOT extract that as a fact.\n"
            f"\n"
            f"OUTPUT FORMAT (Strictly Thai, No explanation, No brackets):\n"
            f"- INTENT: (User's goal)\n"
            f"- FACT: (The extracted fact in Thai. Do NOT repeat instructions. If none, write 'None')\n"
            f"- SELF-CRITIQUE: (Critique)\n"
        )
        
        try:
            response = ollama.chat(
                model=self.model_name,
                messages=[
                    # เปลี่ยน Persona เป็น Data Extractor เพื่อลดการพูดมาก
                    {"role": "system", "content": "You are a Data Extractor. Output ONLY the requested fields. Do not chat. Do not explain."},
                    {"role": "user", "content": reflection_prompt}
                ],
                options={"temperature": 0.0} # สำคัญมาก! ต้องเป็น 0
            )
            return response['message']['content']
        except Exception as e:
            return f"Brain Error (Reflect): {str(e)}"