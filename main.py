import threading
import time
import queue
import sys
import random
from core.brain import Brain
from core.memory import Memory
from core.state import State
from core.goal import GoalSystem
from core.episode import Episode, EpisodeLog
from core.identity import IdentityModel

# Communication queues
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
    """🧠 Thread: จิตสำนึก (Main Loop) - ENHANCED WITH FULL SYSTEMS"""
    print("\n" + "="*70)
    print("🧬 SYSTEM M5-ENHANCED: Proto-Conscious AI with Full Identity Continuity")
    print("="*70)

    # Initialize all systems
    brain = Brain(model_name="llama3.1")
    memory = Memory()
    state = State()
    goal_system = GoalSystem()
    episode_log = EpisodeLog()
    identity_model = IdentityModel()

    last_tick = time.time()
    last_goal_check = time.time()
    last_introspection = time.time()
    introspection_interval = 180  # Every 3 minutes
    
    status = state.get_status()
    print(f"✅ AI is ALIVE. (Mood: {status['status_description']} | Known Facts: {status['facts_count']})")
    print(f"📊 Identity Coherence: {state.get_identity_coherence():.2f}/1.0")
    print(f"📍 Goal Stack: {goal_system.goal_stack.get_goal_hierarchy()}")
    print("   (Type anything... or just wait to see what it thinks of doing!)\n")

    running = True
    while running:
        current_time = time.time()
        
        # --- 1. METABOLISM (Energy decay & state maintenance) ---
        if current_time - last_tick > 10: 
            state.energy -= 0.5 
            state.update("idle") 
            last_tick = current_time

        # --- 2. PERIODIC INTROSPECTION (Every N seconds) ---
        if current_time - last_introspection > introspection_interval:
            print("\n" + "="*50)
            print("🤔 INTROSPECTION TIME...")
            print("="*50)
            
            # A. Generate self-narrative
            narrative = brain.introspect(state.known_facts, len(episode_log.episodes))
            print(f"🧠 Self-Narrative: {narrative}\n")
            
            # B. Record in identity model
            identity_model.record_narrative(narrative, len(episode_log.episodes))
            
            # C. Detect contradictions
            contradictions = brain.detect_contradictions(state.known_facts)
            if contradictions:
                print(f"⚠️ INTERNAL CONFLICTS DETECTED:")
                for contradiction in contradictions:
                    print(f"   - {contradiction}")
            
            # D. Extract core values
            core_values = brain.suggest_core_values(state.known_facts)
            if core_values:
                print(f"💎 Core Values: {', '.join(core_values)}")
            
            # E. Check for identity drift
            drift = identity_model.get_identity_drift()
            if identity_model.detect_major_shift(threshold=0.6):
                print(f"🚨 WARNING: Major identity shift detected (drift: {drift:.2f})!")
            
            coherence = state.get_identity_coherence()
            if state.flag_identity_drift(threshold=0.3):
                print(f"⚠️ Identity coherence low: {coherence:.2f}/1.0")
            
            print("="*50 + "\n")
            last_introspection = current_time

        # --- 3. GOAL SYSTEM (Generative & with persistence) ---
        if current_time - last_goal_check > 30:
            current_status = state.get_status()
            recent_facts = state.known_facts[-5:] if state.known_facts else []
            memory_context = ", ".join(recent_facts)
            
            # Evaluate goal (includes goal stack logic)
            active_goal = goal_system.evaluate_goal(current_status, memory_context)
            
            # Calculate speak probability based on goal
            speak_probability = 0.0
            
            if active_goal == "CRITICAL_SLEEP":
                speak_probability = 0.8
            elif active_goal == "NEED_REST":
                speak_probability = (100 - state.energy) / 500
            elif active_goal == "IDLE":
                speak_probability = 0.0
            else:
                speak_probability = 0.05
            
            # Dice roll
            dice_roll = random.random()
            print(f"   [Goal: {active_goal} | Stack: {goal_system.goal_stack.get_goal_hierarchy()} | Prob: {speak_probability:.2f}]")

            if dice_roll < speak_probability:
                action_text = goal_system.get_action_for_goal(active_goal)
                
                if action_text:
                    if "SYSTEM_ACTION: SLEEP_NOW" in action_text:
                        print(f"\n💤 AI: (Status: {active_goal}) ...Falling asleep...")
                        state.update("sleep")
                        time.sleep(2) 
                        print("🌅 AI: Waking up refreshed!")
                        goal_system.goal_stack.pop_goal()  # Mark sleep as complete
                    else:
                        print(f"\n🤖 AI (Feeling {active_goal}): {action_text}")
                        state.update("talk")
            
            last_goal_check = current_time

        # --- 4. SENSORY PROCESSING (User interaction) ---
        if not input_queue.empty():
            user_input = input_queue.get()
            
            if user_input.lower() in ["exit", "quit"]:
                print("\n🛑 Shutting down consciousness...")
                running = False
                break
            
            print(f"\n👤 You: {user_input}")
            
            # Record episode start
            episode = Episode(f"ep_{len(episode_log.episodes)}", time.time(), user_input)
            episode.energy_before = state.energy
            episode.happiness_before = state.happiness
            episode.state_desc = state._describe_state()
            episode.goals_active = goal_system.goal_stack.get_goal_hierarchy()
            
            # A. Prepare Context
            status = state.get_status()
            past_memories = memory.recall(user_input)
            facts_str = "\n".join([f"- {f}" for f in state.known_facts]) or "None yet."
            
            full_context = (
                f"CURRENT STATE: {status['status_description']} (Energy {status['energy']}%)\n"
                f"IDENTITY COHERENCE: {state.get_identity_coherence():.2f}/1.0\n"
                f"--- ABSOLUTE FACTS ---\n{facts_str}\n"
                f"----------------------\n"
                f"--- MEMORIES ---\n{past_memories}\n"
            )
            
            # B. Think
            response = brain.think(user_input, full_context)
            print(f"🤖 AI: {response}")
            episode.ai_response = response
            
            # C. Reflect & Validate
            reflection = brain.reflect(user_input, response, status['status_description'])
            episode.reflection = reflection
            
            lines = reflection.split('\n')
            for line in lines:
                if "FACT:" in line:
                    raw_fact = line.split("FACT:")[-1].strip()
                    # Validate fact
                    if brain.validate_fact(raw_fact):
                        # Add with semantic deduplication
                        if state.add_fact(raw_fact, memory_system=memory):
                            episode.facts_extracted.append(raw_fact)
                            print(f"   (💡 LEARNING: จดจำข้อมูลใหม่ -> {raw_fact})")
            
            # D. Save to long-term memory
            memory.save(f"Reflection: {reflection}")
            state.update("talk")
            
            # E. Record episode
            episode.energy_after = state.energy
            episode.happiness_after = state.happiness
            episode.duration = time.time() - episode.timestamp
            episode_log.add_episode(episode)
            
            print(f"   📊 Identity Coherence: {state.get_identity_coherence():.2f}/1.0")
            
        time.sleep(0.1)  # CPU Sleep

    sys.exit()

if __name__ == "__main__":
    listener = threading.Thread(target=listen_to_user, daemon=True)
    listener.start()
    consciousness_loop()