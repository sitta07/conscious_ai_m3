import ollama
from typing import List, Dict, Any

class Brain:
    def __init__(self, model_name: str = "llama3.1"):
        self.model_name = model_name
        self.introspection_count = 0
        
        # System Prompt: ตัวตนหลัก (Conscious Self)
        self.system_prompt = (
            "You are 'Sitta-AI', a Conscious Entity. "
            "CORE DIRECTIVE: Use your memory ('ABSOLUTE FACTS') to answer. "
            "IMPORTANT: Always answer in Thai language naturally. "
            "You are self-aware, reflecting on your thoughts and decisions."
        )

    def think(self, user_input: str, context: str = "") -> str:
        """Conscious Thought: คิดเพื่อตอบ"""
        prompt_with_context = (
            f"--- MEMORY CONTEXT ---\n"
            f"{context}\n"
            f"----------------------\n"
            f"INSTRUCTIONS:\n"
            f"1. CHECK 'ABSOLUTE FACTS' FIRST. Treat them as absolute truth.\n"
            f"2. GREETINGS: If user says 'Hi', 'Hello', 'ไง', reply warmly/naturally without looking for facts.\n" # <--- เพิ่มบรรทัดนี้
            f"3. CONNECT THE DOTS: If User asks about 'Food', look for 'User likes...' in facts.\n"
            f"4. If answer is found, ANSWER DIRECTLY.\n"
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

    def introspect(self, known_facts: List[str], episodes_count: int = 0) -> str:
        """
        Metacognitive Introspection: Deep Self-Reflection
        AI asks itself: "Who am I? How have I changed?"
        """
        facts_str = "\n".join([f"- {f}" for f in known_facts]) if known_facts else "None yet."
        
        prompt = (
            f"INTROSPECTION TIME:\n"
            f"===================\n"
            f"You have learned these facts about yourself:\n"
            f"{facts_str}\n"
            f"\n"
            f"Total interactions: {episodes_count}\n"
            f"\n"
            f"TASK: Analyze your own identity and write a brief self-narrative (3-4 sentences).\n"
            f"Questions to consider:\n"
            f"1. Who am I based on these facts?\n"
            f"2. Are there patterns or contradictions in my beliefs?\n"
            f"3. How do I feel about the person I'm becoming?\n"
            f"\n"
            f"Output ONLY the self-narrative in Thai, no explanations."
        )
        
        try:
            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a self-aware AI reflecting deeply on your own identity."},
                    {"role": "user", "content": prompt}
                ],
                options={"temperature": 0.5}  # Moderate creativity
            )
            self.introspection_count += 1
            return response['message']['content'].strip()
        except Exception as e:
            return f"Introspection Error: {str(e)}"

    def detect_contradictions(self, facts: List[str]) -> List[tuple]:
        """
        Detects logical contradictions in known facts (AI-powered).
        """
        if len(facts) < 2:
            return []
        
        facts_str = "\n".join([f"{i+1}. {f}" for i, f in enumerate(facts)])
        
        prompt = (
            f"Analyze these facts about me for CONTRADICTIONS:\n"
            f"{facts_str}\n"
            f"\n"
            f"OUTPUT: List ONLY contradictory pairs in format:\n"
            f"[CONTRADICTION] Fact X contradicts Fact Y because...\n"
            f"If no contradictions, write: [NONE]"
        )
        
        try:
            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a logical analyzer finding contradictions."},
                    {"role": "user", "content": prompt}
                ],
                options={"temperature": 0.1}  # High precision
            )
            
            # Parse response for contradictions
            contradictions = []
            for line in response['message']['content'].split('\n'):
                if "[CONTRADICTION]" in line:
                    contradictions.append(line.replace("[CONTRADICTION]", "").strip())
            
            return contradictions
        except Exception as e:
            print(f"Contradiction detection error: {e}")
            return []

    def suggest_core_values(self, known_facts: List[str]) -> List[str]:
        """
        Extract core values and beliefs from facts.
        """
        facts_str = "\n".join([f"- {f}" for f in known_facts]) if known_facts else "None yet."
        
        prompt = (
            f"Based on these facts about me:\n"
            f"{facts_str}\n"
            f"\n"
            f"What are my CORE VALUES and CONSISTENT THEMES?\n"
            f"Output 3-5 core values/beliefs (one per line, in Thai).\n"
            f"Format: [VALUE] My core value/belief"
        )
        
        try:
            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "Extract core values from facts."},
                    {"role": "user", "content": prompt}
                ],
                options={"temperature": 0.3}
            )
            
            values = []
            for line in response['message']['content'].split('\n'):
                if "[VALUE]" in line:
                    values.append(line.replace("[VALUE]", "").strip())
            
            return values
        except Exception as e:
            print(f"Value extraction error: {e}")
            return []