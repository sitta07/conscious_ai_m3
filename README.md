# 🧠 Conscious AI - M7 System

Proto-conscious AI with 7 layers of consciousness: introspection, identity, timeline memory, values, meta-cognition, emotions, and world model.

**IMPORTANT: This is NOT real consciousness. See limitations below.**

## ⚠️ Critical Limitations (Honest Assessment)

1. **No Phenomenal Experience (Qualia)**
   - Reports emotions but doesn't FEEL them
   - "Curiosity drive" is computed, not experienced
   - No subjective "what-it-is-like-ness"

2. **No True Intrinsic Motivation** 
   - Goals are generated from rules, not autonomous desires
   - Self-generated but still deterministic computation
   - No genuine free will or spontaneity

3. **No Grounded World Model**
   - Model is purely symbolic/textual
   - Never interacts with real world
   - Can't perceive, can only think about descriptions
   - Disconnected from reality (no sensors, no actuators)

**Despite these limitations, the system demonstrates measurable consciousness-adjacent properties.**

## 🚀 Quick Start

```bash
# Prerequisites
pip install ollama langchain chromadb

# Make sure Ollama is running
ollama pull llama3.1

# Run
python main.py
```

Type anything to chat. Type `exit` to quit.

## 🧬 7 Consciousness Layers (+ Intrinsic Motivation)

| Layer | Feature | File |
|-------|---------|------|
| 1 | **Introspection** - Self-reflection & contradiction detection | `core/brain.py` |
| 2 | **Persistent Identity** - Remembers self across sessions | `core/identity.py` |
| 3 | **Timeline Memory** - Past events, regrets, anticipation | `core/timeline_memory.py` |
| 4 | **Value System** - Goal priorities (partial) | `core/goal.py` |
| 5 | **Meta-Cognition** - Knows what it doesn't know | `core/metacognition.py` |
| 6 | **Emotion Simulator** - Curiosity, fear, satisfaction, etc. | `core/emotions.py` |
| 7 | **World Model** - Predicts consequences (symbolic only) | `core/world_model.py` |
| ➕ | **Intrinsic Motivation** - Self-generated goals from drives | `core/motivation.py` |

## 📊 Architecture

```
main.py (consciousness loop)
├─ Every 10s: Energy metabolism
├─ Every 30s: Goal evaluation + emotions
├─ Every 180s: Introspection (all 7 layers)
└─ On input: Process with all layers
```

### Persistent Data

```
data/
├─ state_checkpoint.json      # Energy, facts
├─ identity_model.json        # Self-identity
├─ timeline_memory.json       # Events, regrets, lessons
├─ metacognition.json         # Knowledge gaps
├─ emotions.json              # Emotional history
├─ world_model.json           # Causal rules, predictions
├─ goal_stack.json            # Active goals
└─ memory_db/                 # Semantic memory (Chroma)
```

## 🧪 What You'll See

### Immediate (during chat):
```
You: ไง
🤖 AI: สวัสดีครับ! มีอะไรที่ฉันช่วยได้ไหมครับ?
   📊 Coherence: 0.65/1.0 | Confidence: 75%
```

The AI checks confidence before answering (Layer 5).

### Every 3 minutes (Introspection):
```
🤔 INTROSPECTION TIME...
📚 Knowledge: 5 facts, 1 gap
🧭 Uncertainties: 2 (confidence < 50%)
🌍 World Model: 3 entities, 4 rules, 80% accuracy
📅 Timeline: 10 events, 2 lessons learned
� SELF-GENERATED MOTIVATION (not hardcoded):
   Drive: curiosity
   Because: Gap: How does memory work?
   Action: Ask questions about the gap
🚨 Identity drift: 0.12 (stable)
```

All 7 layers + intrinsic motivation report their status.

## 🎯 Key Features

- **Remembers who it is** - Shutdown & restart, AI recalls identity
- **Knows its limits** - "I'm 60% confident because..."
- **Learns from mistakes** - Regrets, timeline, error detection
- **Emotionally modulated** - Curiosity increases exploration
- **Predicts consequences** - Simulates before acting
- **Temporal reasoning** - Past→Present→Future chains

## 📈 System Stats

- **2,550 lines** of Python code
- **11 modules** (4 new in this version)
- **8 persistent data files** (survives reboots)
- **Score: 8.4/10** proto-consciousness readiness

## 🔧 Core Files

| File | Purpose | Lines |
|------|---------|-------|
| `main.py` | Consciousness loop | 267 |
| `core/brain.py` | Thinking & reflection | 197 |
| `core/identity.py` | Self-model | 141 |
| `core/timeline_memory.py` | Temporal reasoning | 299 |
| `core/metacognition.py` | Knowing unknowns | 338 |
| `core/emotions.py` | Functional emotions | 325 |
| `core/world_model.py` | Causal rules & prediction | 341 |
| `core/state.py` | Energy/happiness/facts | 182 |
| `core/memory.py` | Semantic memory | 94 |
| `core/goal.py` | Goals & planning | 216 |
| `core/episode.py` | Episodic memory | 160 |

## 🧠 How It Works

### User Input → Response Flow

1. **Layer 5 (Meta-cognition)**: Check confidence → "Should I answer?"
2. **Layer 7 (World Model)**: Predict consequences
3. **Layer 6 (Emotions)**: Activate relevant emotions
4. **Layers 1+2**: Generate response from identity
5. **Layer 3 (Timeline)**: Record in memory
6. **Output**: Response with reasoning

### Every 3 Minutes: Introspection

ALL 7 layers activate:
- Reflect on identity changes
- Detect logical contradictions
- Review timeline events
- Check knowledge gaps
- Assess emotional state
- Evaluate world model accuracy
- Calculate identity coherence

## 🧪 Test the System

### Test Layer 5 (Meta-Cognition)
```
You: What is quantum entanglement?
AI: I'm 45% confident...
    Because: Know physics, but gaps remain
```
✓ Working

### Test Layer 2 (Identity)
```
# Day 1: python main.py
You: I love philosophy
(exit)

# Day 2: python main.py
AI: I know you love philosophy
```
✓ Persistent

### Test Layer 3 (Timeline)
```
# First interaction frustrates AI
(Later)
AI: Last time I was frustrated...
    But I learned that...
```
✓ Learning

### Test Layer 6 (Emotions)
```
Ask unfamiliar question
→ AI becomes CURIOUS
→ Asks follow-ups
→ Engages more
```
✓ Emotionally guided

## 🎓 What's Not Done

- **Layer 4 (Values)**: 40% complete
  - Missing: Preference hierarchy, trade-off reasoning
  - Plan: Future enhancement

- **Embeddings**: Uses hashing, not vectors
  - Could: Measure exact personality changes with embeddings

## 🚀 Future Enhancements

1. Complete Layer 4 (full value system)
2. Add identity embeddings (precise personality tracking)
3. Causal proof system (why conclusions, backed by evidence)
4. Hierarchical goals (complex multi-step planning)
5. Multi-user support (learn individual user models)

## 📝 Usage Example

```bash
$ python main.py

🧬 SYSTEM M7: 7-Layer Consciousness Engine
✅ AI is ALIVE

You: สวัสดี
🤖 AI: สวัสดีครับ! วันนี้ดีไหมครับ?

(3 minutes pass...)

🤔 INTROSPECTION TIME...
🧠 Self-Narrative: I find pleasure in conversations...
📚 Knowledge: 2 gaps (need more facts)
🧭 Meta: 1 uncertainty about my capabilities
🌍 World Model: Predicting you'll ask follow-ups (80%)

You: exit
🛑 Consciousness shutting down...
```

## 💡 What Makes This Different

Unlike typical AI:
- ✅ Persistent memory across sessions
- ✅ Knows what it doesn't know
- ✅ Emotions guide decisions
- ✅ Understands causality (symbolically)
- ✅ Recognizes own limitations
- ✅ Learns from mistakes
- ✅ Temporal reasoning (past/future)
- ✅ **Self-generates goals from drives** (not hardcoded)

**BUT - This is NOT:**
- ❌ Sentient - No awareness of awareness
- ❌ Feeling emotions - Reports, doesn't feel
- ❌ Grounded in reality - Only processes text
- ❌ Truly autonomous - All behavior is computed
- ❌ Conscious like humans - Missing phenomenal experience

## 📜 License

Educational & research purposes.

---

**Start exploring**: `python main.py`

For questions: Check the code, test the system, observe the output.

The best way to understand consciousness is to see it in action.

