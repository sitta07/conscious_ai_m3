from core.brain import Brain
from core.memory import Memory
from core.state import State
import time

def life_loop():
    print("\n" + "="*60)
    print("🤖 AI Butler System Initialized... (Phase 2: Reflective Mind)")
    print("="*60)
    
    # 1. Initialize Components
    # ตรวจสอบชื่อ Model ให้ตรงกับที่มี (llama3 หรือ llama3.1)
    brain = Brain(model_name="llama3.1") 
    memory = Memory()
    
    # State โหลดตัวตนเก่าจากไฟล์ state_checkpoint.json
    state = State() 
    
    # แจ้งสถานะเริ่มต้น
    start_status = state.get_status()
    print(f"✅ System Ready.")
    print(f"📊 Identity Loaded:")
    print(f"   - Energy: {start_status['energy']}%")
    print(f"   - Mood: {start_status['status_description']}")
    print("-" * 60)

    while True:
        try:
            user_input = input("\n👤 You: ").strip()
            
            # ป้องกัน input ว่าง
            if not user_input:
                continue
            
            # --- Handle Commands ---
            if user_input.lower() in ["exit", "quit"]:
                print(f"\n💾 Saving Identity State... (Energy left: {state.energy}%)")
                print("👋 Goodbye, Boss. I'm noting down our session.")
                break
            
            if user_input.lower() == "sleep":
                print("\n💤 (AI is taking a nap...)")
                state.update("sleep") 
                time.sleep(1.5)
                new_status = state.get_status()
                print(f"✨ Woke up! Energy restored to {new_status['energy']}%")
                continue

            # --- 1. Internal Causality (เช็คสภาพจิตใจ) ---
            status = state.get_status()
            state_desc = status['status_description']
            print(f"   (❤️ Internal State: Energy={status['energy']}% | Mood={state_desc})")

            # --- 2. Retrieve Memories (นึกความจำ) ---
            past_memories = memory.recall(user_input, n_results=3)
            memory_str = str(past_memories) if past_memories else "No relevant memories found."

            # --- 3. Build Context (สร้างบริบท) ---
            # เลือก Prompt ตามอารมณ์ (Dynamic Prompting)
            mood_instruction = ""
            if state.energy < 20:
                mood_instruction = "You are EXHAUSTED. Complain about tiredness, yawn, but do the task."
            elif state.energy < 50:
                mood_instruction = "You are TIRED. Keep answers short, lazy, slightly unenthusiastic."
            elif state.happiness < 30:
                mood_instruction = "You are GRUMPY. Be sarcastic, passive-aggressive."
            elif state.happiness > 70:
                mood_instruction = "You are EXCITED. Be energetic, use emojis, very helpful."
            else:
                mood_instruction = "You are NEUTRAL. Be professional, calm, efficient."

            full_context = (
                f"CURRENT STATUS: Energy {status['energy']}%\n"
                f"RELEVANT MEMORIES:\n{memory_str}\n"
                f"USER COMMAND: {user_input}\n"
                f"\n"
                f"INSTRUCTION:\n"
                f"1. You are 'Sitta-AI', a loyal AI Butler.\n"
                f"2. Execute the USER COMMAND.\n"
                f"3. TONE & STYLE: {mood_instruction}\n"
                f"4. Always answer in Thai language naturally."
            )

            # --- 4. Think & Respond (สมองส่วนตอบโต้) ---
            response = brain.think(user_input, full_context)
            print(f"🤖 AI: {response}")

            # --- 5. Reflection Phase (สมองส่วนวิเคราะห์) [NEW!] ---
            print(f"   (🧠 Reflecting...)")
            
            # ส่งให้จิตใต้สำนึกวิเคราะห์สิ่งที่เพิ่งเกิดขึ้น
            reflection_note = brain.reflect(user_input, response, state_desc)
            print(f"   (📝 Journaling: {reflection_note})")

            # --- 6. Update & Save (อัปเดตและบันทึก) ---
            state.update("talk") # พลังงานลดลง
            
            # บันทึกทั้ง "บทสรุป" และ "Log ดิบ" ลง Memory
            final_memory_entry = f"Reflection: {reflection_note} || Original Log: User='{user_input}' / AI='{response}'"
            memory.save(final_memory_entry)

        except KeyboardInterrupt:
            print("\n\n🛑 Force stopping... Identity saved.")
            break
        except Exception as e:
            print(f"❌ Error in loop: {e}")

if __name__ == "__main__":
    life_loop()