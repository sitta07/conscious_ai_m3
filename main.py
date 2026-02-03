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
from core.metacognition import MetaCognition
from core.world_model import WorldModel
from core.emotions import EmotionalSystem, EmotionState
from core.timeline_memory import TimelineMemory
from core.motivation import IntrinsicMotivation

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
    """🧠 Thread: จิตสำนึก (Main Loop) - FULL 7-LAYER CONSCIOUSNESS"""
    print("\n" + "="*70)
    print("🧬 SYSTEM M7: 7-Layer Consciousness Engine")
    print("="*70)
    print("Layers: 1.Introspection | 2.Identity | 3.Timeline | 4.Values |")
    print("        5.Meta-cognition | 6.Emotions | 7.World-Model")
    print("="*70)

    # Initialize ALL consciousness systems (7 layers)
    brain = Brain(model_name="llama3.1")
    memory = Memory()
    state = State()
    goal_system = GoalSystem()
    episode_log = EpisodeLog()
    
    # NEW: Layer 2 - Persistent Identity
    identity_model = IdentityModel()
    
    # NEW: Layer 5 - Meta-cognition (knowing unknowns)
    metacognition = MetaCognition()
    
    # NEW: Layer 7 - World Model (predict & simulate)
    world_model = WorldModel()
    
    # NEW: Layer 6 - Emotion Simulator (decision acceleration)
    emotions = EmotionalSystem()
    
    # NEW: Layer 3 - Timeline Memory (past/present/future)
    timeline = TimelineMemory()
    
    # NEW: Intrinsic Motivation (self-generated goals, not hardcoded)
    intrinsic = IntrinsicMotivation()

    last_tick = time.time()
    last_goal_check = time.time()
    last_introspection = time.time()
    last_emotion_decay = time.time()
    introspection_interval = 180  # Every 3 minutes
    
    # Initialize meta_status (will be updated during introspection)
    meta_status = metacognition.get_epistemic_status()
    
    status = state.get_status()
    print(f"\n✅ AI is ALIVE")
    print(f"   Energy: {status['energy']}% | Mood: {status['status_description']}")
    print(f"   Identity Coherence: {state.get_identity_coherence():.2f}/1.0")
    print(f"   Known Facts: {status['facts_count']}")
    print(f"   Emotional State: {emotions.get_emotional_state()['mood_description']}")
    print(f"\n   (Type anything... or wait to see what I think...)\n")

    running = True
    while running:
        current_time = time.time()
        
        # === LAYER 6: EMOTIONAL DECAY ===
        if current_time - last_emotion_decay > 5:
            emotions.cleanup_inactive()
            last_emotion_decay = current_time
        
        # === LAYER 1 + 5: INTROSPECTION WITH META-COGNITION ===
        if current_time - last_introspection > introspection_interval:
            print("\n" + "="*60)
            print("🤔 INTROSPECTION TIME... (Meta-cognition enabled)")
            print("="*60)
            
            # Check for knowledge gaps
            meta_status = metacognition.get_epistemic_status()
            print(f"📚 Knowledge Status: {meta_status['knowledge_gaps']} gaps, "
                  f"{meta_status['high_priority_gaps']} are high-priority")
            
            # A. Generate self-narrative (Layer 1)
            narrative = brain.introspect(state.known_facts, len(episode_log.episodes))
            print(f"🧠 Self-Narrative: {narrative}\n")
            identity_model.record_narrative(narrative, len(episode_log.episodes))
            
            # B. Detect contradictions with causal analysis (Layer 1 + 5)
            contradictions = brain.detect_contradictions(state.known_facts)
            if contradictions:
                print(f"⚠️ INTERNAL CONFLICTS:")
                for c in contradictions:
                    print(f"   - {c}")
                    timeline.record_regret("Contradictory beliefs", "didn't investigate", "verify beliefs")
            
            # C. Meta-cognitive assessment (Layer 5)
            print(f"🧭 Meta-Cognitive Assessment:")
            print(f"   - Uncertainties: {meta_status['uncertainties']}")
            print(f"   - Low-confidence beliefs: {meta_status['low_confidence_beliefs']}")
            print(f"   - Times corrected myself: {meta_status['learning_events']}")
            
            # D. World model insight (Layer 7)
            world_summary = world_model.get_world_summary()
            print(f"🌍 World Model:")
            print(f"   - Entities tracked: {world_summary['entities_known']}")
            print(f"   - Causal rules learned: {world_summary['causal_rules']}")
            print(f"   - Active predictions: {world_summary['active_predictions']}")
            print(f"   - Prediction accuracy: {world_summary['recent_prediction_accuracy']:.0%}")
            
            # E. Timeline insight (Layer 3)
            timeline_summary = timeline.get_timeline_summary(24)
            print(f"📅 Timeline Memory (last 24h):")
            print(f"   - Events recorded: {timeline_summary['events_in_period']}")
            print(f"   - Lessons learned: {len(timeline_summary['key_lessons'])}")
            print(f"   - Regrets to learn from: {timeline_summary['regrets_to_learn_from']}")
            
            # F. INTRINSIC MOTIVATION (generate self-driven goals)
            intrinsic.detect_curiosity_gap(
                [g['topic'] for g in meta_status.get('knowledge_gaps', [])],
                meta_status.get('uncertainties', 0)
            )
            intrinsic.detect_prediction_failure(
                world_summary['active_predictions'],
                world_summary['recent_prediction_accuracy']
            )
            
            generated_goal = intrinsic.generate_goal_from_drives()
            if generated_goal:
                print(f"💡 SELF-GENERATED MOTIVATION (not hardcoded):")
                print(f"   Drive: {generated_goal['generated_from']}")
                print(f"   Because: {generated_goal['motivation']}")
                print(f"   Action: {generated_goal['proposed_action']}")
            else:
                print(f"✓ All drives satisfied - no new motivation")
            
            # G. Identity drift (Layer 2)
            drift = identity_model.get_identity_drift()
            if identity_model.detect_major_shift(threshold=0.6):
                print(f"🚨 Major identity shift detected! Drift: {drift:.2f}")
                timeline.record_event("identity", f"Major personality shift: {drift:.2f}")
            
            print("="*60 + "\n")
            last_introspection = current_time

        # === LAYERS 3 + 6: ANTICIPATION & EMOTIONAL PREDICTION ===
        if current_time - last_goal_check > 30:
            # Use world model to anticipate next state
            current_desc = f"Energy {state.energy:.1f}%, {state._describe_state()}"
            predictions = world_model.predict_next_state(current_desc)
            
            if predictions:
                for pred in predictions:
                    print(f"🔮 Anticipation: {pred.prediction} "
                          f"({pred.confidence:.0%} confident)")
            
            # Emotional decision weighting
            emotion_state = emotions.get_emotional_state()
            decision_weights = emotion_state["decision_weights"]
            
            # Goal evaluation with emotional modulation
            current_status = state.get_status()
            active_goal = goal_system.evaluate_goal(current_status, "")
            
            speak_probability = 0.05
            if active_goal == "CRITICAL_SLEEP":
                speak_probability = 0.8
                emotions.trigger_fear("exhaustion", 0.7)
            elif active_goal == "NEED_REST":
                speak_probability = (100 - state.energy) / 500
                emotions.trigger_satisfaction("resting well", 0.5)
            
            # Apply emotional modulation
            if emotion_state["mood"] > 0.6:
                emotions.trigger_curiosity("current interaction", 0.5)
                speak_probability *= 1.2
            elif emotion_state["mood"] < 0.4:
                emotions.trigger_frustration("difficult situation", 0.6)
                speak_probability *= 0.7
            
            print(f"   [Goal: {active_goal} | Emotional State: "
                  f"{emotion_state['mood_description']} | "
                  f"Speak Prob: {speak_probability:.2f}]")
            
            last_goal_check = current_time

        # === LAYER 3: TIMELINE MEMORY & LEARNING ===
        if not input_queue.empty():
            user_input = input_queue.get()
            
            if user_input.lower() in ["exit", "quit"]:
                print("\n🛑 Consciousness shutting down...")
                running = False
                break
            
            print(f"\n👤 You: {user_input}")
            
            # Record in timeline
            timeline.record_event("interaction", user_input[:50])
            
            # Episode setup
            episode = Episode(f"ep_{len(episode_log.episodes)}", time.time(), user_input)
            episode.energy_before = state.energy
            
            # === LAYER 5: CHECK CONFIDENCE BEFORE ANSWERING ===
            if "?" in user_input:
                decomposed = metacognition.problem_decomposer.decompose(user_input)
                if decomposed.get("confidence", 0) < 0.5:
                    print(f"⚠️ I'm uncertain about this ({decomposed['confidence']:.0%})")
                    if decomposed.get("unknowns"):
                        print(f"   Missing: {decomposed['unknowns'][0]}")
                    if decomposed.get("need_help"):
                        print(f"   (I should ask for help)")
                    emotions.trigger_confusion("unclear question", 0.4)
                else:
                    emotions.trigger_curiosity("interesting question", 0.6)
            
            # Context preparation
            status = state.get_status()
            past_memories = memory.recall(user_input)
            facts_str = "\n".join([f"- {f}" for f in state.known_facts]) or "None yet."
            
            full_context = (
                f"CURRENT STATE: {status['status_description']} (Energy {status['energy']}%)\n"
                f"IDENTITY COHERENCE: {state.get_identity_coherence():.2f}/1.0\n"
                f"EMOTIONAL STATE: {emotions.get_emotional_state()['mood_description']}\n"
                f"--- FACTS ---\n{facts_str}\n"
                f"--- MEMORIES ---\n{past_memories}\n"
            )
            
            # Think
            response = brain.think(user_input, full_context)
            print(f"🤖 AI: {response}")
            episode.ai_response = response
            
            # Reflect & learn
            reflection = brain.reflect(user_input, response, status['status_description'])
            episode.reflection = reflection
            
            lines = reflection.split('\n')
            for line in lines:
                if "FACT:" in line:
                    raw_fact = line.split("FACT:")[-1].strip()
                    if brain.validate_fact(raw_fact):
                        if state.add_fact(raw_fact, memory_system=memory):
                            episode.facts_extracted.append(raw_fact)
                            print(f"   (💡 LEARNING: {raw_fact})")
                            timeline.record_event("learning", raw_fact)
                            
                            # Update world model
                            if "likes" in raw_fact.lower():
                                world_model.observe_state("user", "preference", raw_fact)
            
            memory.save(f"Reflection: {reflection}")
            state.update("talk")
            
            # === LAYER 7: SIMULATE CONSEQUENCES ===
            simulation = world_model.simulate_action(f"Just heard: {user_input[:30]}")
            if not simulation.get("error"):
                print(f"   💭 Simulated outcome: {simulation.get('recommendation', 'unknown')}")
            
            episode.energy_after = state.energy
            episode_log.add_episode(episode)
            
            print(f"   📊 Coherence: {state.get_identity_coherence():.2f}/1.0 | "
                  f"Meta-gaps: {meta_status['knowledge_gaps']}")
            
        time.sleep(0.1)

    sys.exit()

if __name__ == "__main__":
    listener = threading.Thread(target=listen_to_user, daemon=True)
    listener.start()
    consciousness_loop()