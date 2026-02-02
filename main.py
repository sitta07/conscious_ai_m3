import threading
import time
import queue
import sys
from core.brain import Brain
from core.memory import Memory
from core.state import State

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
    print("🧬 System M3: Awakening Consciousness Threads...")
    print("==================================================")

    brain = Brain(model_name="llama3.1")
    memory = Memory()
    state = State()

    last_tick = time.time()
    
    status = state.get_status()
    print(f"✅ AI is ALIVE. (Mood: {status['status_description']} | Known Facts: {status['facts_count']})")

    running = True
    while running:
        current_time = time.time()
        
        # --- 1. METABOLISM ---
        if current_time - last_tick > 10: 
            state.energy -= 0.5 
            state.update("idle") 
            last_tick = current_time
            
            if state.energy < 15 and state.energy % 5 == 0:
                print(f"\n🤖 AI (Muttering): ...battery low... (Energy: {state.energy}%)")

        # --- 2. SENSORY PROCESSING ---
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
            
            # ดึง Fact ที่จำได้ออกมาโชว์ให้สมองเห็น
            facts_str = "\n".join([f"- {f}" for f in state.known_facts])
            if not facts_str: facts_str = "None yet."
            
            full_context = (
                f"CURRENT STATE: {status['status_description']} (Energy {status['energy']}%)\n"
                f"--- ABSOLUTE FACTS (What you KNOW for sure) ---\n{facts_str}\n"
                f"-----------------------------------------------\n"
                f"--- FUZZY MEMORIES (Recall) ---\n{past_memories}\n"
            )
            
            # B. Think & Respond
            response = brain.think(user_input, full_context)
            print(f"🤖 AI: {response}")
            
            # C. Reflect & Learn (Active Learning Logic)
            reflection = brain.reflect(user_input, response, status['status_description'])
            
            # แกะกล่อง Fact
            lines = reflection.split('\n')
            for line in lines:
                if "FACT:" in line:
                    # ตัดคำว่า FACT: ทิ้ง เอาเนื้อหาข้างหลัง
                    raw_fact = line.split("FACT:")[-1].strip()
                    # ส่งเข้า Hippocampus (State)
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