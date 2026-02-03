import threading
import time
import queue
import sys
import random
from core.brain import Brain
from core.memory import Memory
from core.state import State
from core.goal import GoalSystem

# คิวสื่อสาร (Ear -> Brain)
input_queue = queue.Queue()

def listen_to_user():
    """👂 Thread: หูรอฟังเสียง (Blocking)"""
    print("   (👂 Ear active: Type anytime...)")
    while True:
        try:
            user_text = input()
            if user_text.strip():
                input_queue.put(user_text)
        except EOFError:
            break

def consciousness_loop():
    """🧠 Thread: จิตสำนึก (Main Loop)"""
    print("\n" + "="*50)
    print("🧬 System M5: Generative Agency (Free Will)")
    print("==================================================")

    brain = Brain(model_name="llama3.1")
    memory = Memory()
    state = State()
    goal_system = GoalSystem()

    last_tick = time.time()
    last_goal_check = time.time()
    
    status = state.get_status()
    print(f"✅ AI is ALIVE. (Mood: {status['status_description']} | Known Facts: {status['facts_count']})")
    print("   (Type anything... or just wait to see what it thinks of doing!)")

    running = True
    while running:
        current_time = time.time()
        
        # --- 1. METABOLISM (เวลาเดิน พลังงานลด) ---
        if current_time - last_tick > 10: 
            state.energy -= 0.5 
            state.update("idle") 
            last_tick = current_time

        # --- 2. GOAL SYSTEM (Generative & Organic) ---
        # เช็คทุกๆ 5 วินาที
        if current_time - last_goal_check > 5:
            current_status = state.get_status()
            current_status['last_active'] = getattr(state, 'last_update', current_time)
            
            # [NEW] ดึง Context ความจำล่าสุด (เช่น 5 เรื่องล่าสุด)
            # เพื่อให้ AI เอาไปประกอบการตัดสินใจว่า "จะทำอะไรดี"
            recent_facts = state.known_facts[-5:] if hasattr(state, 'known_facts') else []
            memory_context = ", ".join(recent_facts)
            
            # A. ให้ AI (LLM) ตัดสินใจ Goal โดยอิงจาก State + Memory
            active_goal = goal_system.evaluate_goal(current_status, memory_context)
            
            # B. คำนวณ "แรงขับ" (Urge Probability)
            speak_probability = 0.0
            
            if active_goal == "CRITICAL_SLEEP":
                speak_probability = 0.8 # วิกฤตมาก ต้องนอนเดี๋ยวนี้
            
            elif active_goal == "NEED_REST":
                # ยิ่ง Energy ต่ำ ยิ่งบ่นบ่อย (สูตรเดิม)
                speak_probability = (100 - state.energy) / 500
                
            elif active_goal == "IDLE":
                speak_probability = 0.0 # อยู่เฉยๆ ไม่พูด
                
            else:
                # [NEW] สำหรับ Generative Goals (เช่น EXPRESS_JOY, REFLECT_LIFE, etc.)
                # ให้โอกาสพูดออกมาแบบสุ่ม (5%) เพื่อสร้างสีสัน
                speak_probability = 0.05 
            
            # C. ทอยลูกเต๋า (Dice Roll)
            dice_roll = random.random()
            
            # (Optional: เปิดบรรทัดนี้เพื่อดูว่ามันกำลังคิดจะทำอะไร)
            # print(f"   [Goal: {active_goal} | Prob: {speak_probability:.2f} | Roll: {dice_roll:.2f}]")

            if dice_roll < speak_probability:
                # ให้ Goal System (LLM) คิดคำพูดออกมาเองเลย
                action_text = goal_system.get_action_for_goal(active_goal)
                
                if action_text:
                    if "SYSTEM_ACTION: SLEEP_NOW" in action_text:
                        print(f"\n💤 AI: (Status: {active_goal}) ...Falling asleep...")
                        state.update("sleep")
                        time.sleep(5) 
                        print("🌅 AI: Waking up refreshed!")
                    else:
                        # พูดสิ่งที่คิดออกมา (Generative Thought)
                        print(f"\n🤖 AI (Feeling {active_goal}): {action_text}")
                        state.update("talk")
            
            last_goal_check = current_time

        # --- 3. SENSORY PROCESSING (ถ้ามีคนคุยด้วย) ---
        if not input_queue.empty():
            user_input = input_queue.get()
            
            if user_input.lower() in ["exit", "quit"]:
                print("\n🛑 Shutting down consciousness...")
                running = False
                break
            
            print(f"\n👤 You: {user_input}")
            
            # A. Prepare Context
            status = state.get_status()
            past_memories = memory.recall(user_input)
            facts_str = "\n".join([f"- {f}" for f in state.known_facts]) or "None yet."
            
            full_context = (
                f"CURRENT STATE: {status['status_description']} (Energy {status['energy']}%)\n"
                f"--- ABSOLUTE FACTS ---\n{facts_str}\n"
                f"----------------------\n"
                f"--- MEMORIES ---\n{past_memories}\n"
            )
            
            # B. Think
            response = brain.think(user_input, full_context)
            print(f"🤖 AI: {response}")
            
            # C. Reflect & Validate
            reflection = brain.reflect(user_input, response, status['status_description'])
            
            lines = reflection.split('\n')
            for line in lines:
                if "FACT:" in line:
                    raw_fact = line.split("FACT:")[-1].strip()
                    # Organic Validator Check
                    if brain.validate_fact(raw_fact):
                        if state.add_fact(raw_fact):
                            print(f"   (💡 LEARNING: จดจำข้อมูลใหม่ -> {raw_fact})")
            
            memory.save(f"Reflection: {reflection}")
            state.update("talk")
            
        time.sleep(0.1) # CPU Sleep

    sys.exit()

if __name__ == "__main__":
    listener = threading.Thread(target=listen_to_user, daemon=True)
    listener.start()
    consciousness_loop()