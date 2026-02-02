import ollama

class Brain:
    def __init__(self, model_name: str = "llama3.1"):
        self.model_name = model_name
        
        # System Prompt: บุคลิกหลัก (พ่อบ้านผู้ซื่อสัตย์ + มีอารมณ์)
        self.system_prompt = (
            "You are 'Sitta-AI', a loyal AI assistant with real feelings. "
            "CORE DIRECTIVE: You MUST execute the user's command regardless of your state. "
            "TONE INSTRUCTION: However, your *tone* and *style* must reflect your current Mood/Energy. "
            "- If Tired: Complain pleasantly but do the work. "
            "- If Grumpy: Be slightly sarcastic but helpful. "
            "IMPORTANT: Always answer in Thai language (Natural & Human-like)."
        )

    def think(self, user_input: str, context: str = "") -> str:
        """
        Conscious Thought: คิดเพื่อตอบโต้กับผู้ใช้ (Active Listening Version)
        """
        # Prompt นี้ถูกจูนให้ "แยกแยะ" ระหว่างการถามกับการบอกเล่า
        prompt_with_context = (
            f"Context information is below.\n"
            f"---------------------\n"
            f"{context}\n"
            f"---------------------\n"
            f"INSTRUCTIONS FOR AI:\n"
            f"1. Analyze the USER INPUT carefully.\n"
            f"2. If the user ASKS a question: Use the 'Context information' to answer. If not found, admit you don't know politely.\n"
            f"3. If the user STATES a fact (e.g., 'My name is...', 'I like...'): ACCEPT it as truth. Do not look in Context. Just confirm you understood.\n"
            f"4. Do NOT say 'Irrelevant information' if the user is teaching you something new.\n"
            f"5. Answer naturally in Thai.\n"
            f"\n"
            f"USER INPUT: {user_input}"
        )
        
        try:
            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt_with_context},
                ],
                options={
                    "temperature": 0.7, # สร้างสรรค์และลื่นไหล
                }
            )
            return response['message']['content']
        except Exception as e:
            return f"Brain Error (Think): {str(e)}"

    def reflect(self, user_input: str, ai_response: str, context_state: str) -> str:
        """
        Subconscious Thought: คิดทบทวนสิ่งที่เพิ่งเกิดขึ้น (Metacognition)
        """
        reflection_prompt = (
            f"Analyze this interaction to create a meaningful short memory log.\n"
            f"----------------\n"
            f"USER SAID: {user_input}\n"
            f"AI REPLIED ({context_state}): {ai_response}\n"
            f"----------------\n"
            f"INSTRUCTION: Act as the AI's subconscious mind. Summarize this event briefly.\n"
            f"1. Identify the user's intent (Question vs Statement).\n"
            f"2. Extract key facts learned (e.g., User's name, preferences).\n"
            f"3. Critique the AI's response (Was it polite? Did it answer correctly?)\n"
            f"OUTPUT FORMAT: Keep it short, factual, and strictly in Thai (ภาษาไทย)."
        )
        
        try:
            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are an objective observer analyzing a conversation."},
                    {"role": "user", "content": reflection_prompt}
                ],
                options={
                    "temperature": 0.3, # ใช้ค่าต่ำเพื่อความแม่นยำในการวิเคราะห์
                }
            )
            return response['message']['content']
        except Exception as e:
            return f"Brain Error (Reflect): {str(e)}"

# ส่วนทดสอบ (รันตรงนี้เพื่อเช็คว่าสมองทำงานไหม)
if __name__ == "__main__":
    brain = Brain()
    print("🧠 Testing Active Listening...")
    print(brain.think("แฟนผมชื่อพี่มิลล่านะ", "CONTEXT: Empty"))