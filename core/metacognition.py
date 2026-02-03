"""
Layer 5: Meta-cognition (ปัญญา) - Knowing what you don't know

This is THE CORE of wisdom:
1. Know you don't know (epistemic humility)
2. Know you're wrong (error detection)
3. Know your limits (confidence scoring)
4. Adjust your thinking method
5. Decompose hard problems

WITHOUT THIS: AI is confidently wrong
WITH THIS: AI is humbly uncertain
"""

import json
import time
import os
from typing import List, Dict, Any, Tuple, Optional
import ollama

class KnowledgeGap:
    """Represents something the AI doesn't know."""
    def __init__(self, topic: str, reason: str, priority: float = 0.5):
        self.topic = topic  # "How does climate change affect coral?"
        self.reason = reason  # "Not in training data" / "Contradicts known facts" / "Too complex"
        self.priority = priority  # 0.0-1.0, how important to learn
        self.timestamp = time.time()
        self.attempts = 0  # How many times tried to fill this gap

    def to_dict(self) -> Dict[str, Any]:
        return {
            "topic": self.topic,
            "reason": self.reason,
            "priority": self.priority,
            "timestamp": self.timestamp,
            "attempts": self.attempts
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'KnowledgeGap':
        gap = KnowledgeGap(data["topic"], data["reason"], data.get("priority", 0.5))
        gap.timestamp = data.get("timestamp", time.time())
        gap.attempts = data.get("attempts", 0)
        return gap


class Uncertainty:
    """Confidence scoring for specific beliefs/answers."""
    def __init__(self, statement: str):
        self.statement = statement
        self.confidence = 0.5  # 0.0-1.0
        self.evidence_count = 0
        self.contradictions = []  # Evidence against this statement
        self.timestamp = time.time()
        self.reasoning = ""  # Why this confidence level

    def update_confidence(self, evidence_pieces: int, contra_count: int = 0):
        """Update confidence based on evidence and contradictions."""
        # More evidence = higher confidence, but contradictions lower it
        evidence_weight = min(1.0, evidence_pieces / 5.0)  # Saturates at 5 pieces
        contradiction_weight = max(0.0, 1.0 - contra_count * 0.2)
        self.confidence = 0.5 * evidence_weight + 0.5 * contradiction_weight
        self.evidence_count = evidence_pieces

    def to_dict(self) -> Dict[str, Any]:
        return {
            "statement": self.statement,
            "confidence": round(self.confidence, 2),
            "evidence_count": self.evidence_count,
            "contradictions": self.contradictions,
            "reasoning": self.reasoning
        }


class ErrorDetector:
    """Detects when the AI is wrong or contradicting itself."""
    
    def __init__(self):
        self.detected_errors = []
        self.error_log = []  # For learning
    
    def find_contradictions_in_facts(self, facts: List[str], model: str = "llama3.1") -> List[Dict[str, Any]]:
        """Use LLM to detect contradictions with causal reasoning."""
        if len(facts) < 2:
            return []
        
        facts_str = "\n".join([f"{i+1}. {f}" for i, f in enumerate(facts)])
        
        prompt = (
            f"FIND CONTRADICTIONS in these statements:\n"
            f"{facts_str}\n\n"
            f"For each contradiction found, explain:\n"
            f"1. Which facts contradict?\n"
            f"2. Why are they contradictory?\n"
            f"3. Which is more likely to be wrong and why?\n"
            f"4. What should we investigate?\n\n"
            f"Output JSON format:\n"
            f"[{{"
            f"  \"fact_1\": \"statement\",\n"
            f"  \"fact_2\": \"statement\",\n"
            f"  \"reason\": \"why contradictory\",\n"
            f"  \"likely_error\": \"which is probably wrong\",\n"
            f"  \"investigate\": \"what to verify\"\n"
            f"}}]\n"
            f"If no contradictions, return: []"
        )
        
        try:
            response = ollama.chat(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a logical analyzer finding contradictions. Be precise."},
                    {"role": "user", "content": prompt}
                ],
                options={"temperature": 0.1}
            )
            
            content = response['message']['content'].strip()
            
            # Try to parse JSON
            try:
                import json as json_module
                contradictions = json_module.loads(content)
                if contradictions:
                    self.error_log.extend(contradictions)
                return contradictions if isinstance(contradictions, list) else []
            except:
                return []
                
        except Exception as e:
            print(f"⚠️ Error detection failed: {e}")
            return []
    
    def compare_with_previous(self, previous_statement: str, current_statement: str, 
                             model: str = "llama3.1") -> Dict[str, Any]:
        """Detect if AI changed its mind or was wrong before."""
        prompt = (
            f"Compare these two statements from the same AI:\n"
            f"PREVIOUS: {previous_statement}\n"
            f"CURRENT: {current_statement}\n\n"
            f"Analyze:\n"
            f"1. Are these contradictory? (yes/no)\n"
            f"2. If yes, which was likely the error?\n"
            f"3. What changed? (learning? new info? mistake corrected?)\n"
            f"4. Should the AI learn from this?\n\n"
            f"Output JSON:\n"
            f"{{"
            f"  \"contradictory\": bool,\n"
            f"  \"error_was_in\": \"previous/current/neither\",\n"
            f"  \"what_changed\": \"explanation\",\n"
            f"  \"should_learn\": bool,\n"
            f"  \"lesson\": \"what to remember\"\n"
            f"}}"
        )
        
        try:
            response = ollama.chat(
                model=model,
                messages=[
                    {"role": "system", "content": "You are analyzing AI self-corrections."},
                    {"role": "user", "content": prompt}
                ],
                options={"temperature": 0.1}
            )
            
            content = response['message']['content'].strip()
            try:
                import json as json_module
                result = json_module.loads(content)
                return result
            except:
                return {"error": "parse_failed"}
                
        except Exception as e:
            return {"error": str(e)}


class ProblemDecomposer:
    """Breaks complex problems into smaller parts (metacognitive planning)."""
    
    @staticmethod
    def decompose(problem: str, model: str = "llama3.1") -> Dict[str, Any]:
        """Break down complex problem into steps."""
        prompt = (
            f"Break down this problem into steps:\n"
            f"PROBLEM: {problem}\n\n"
            f"Think about:\n"
            f"1. What do I need to know?\n"
            f"2. What am I uncertain about?\n"
            f"3. What's the simplest approach?\n"
            f"4. What could go wrong?\n"
            f"5. Should I ask for help?\n\n"
            f"Output JSON:\n"
            f"{{"
            f"  \"problem_type\": \"simple/moderate/complex\",\n"
            f"  \"steps\": [\"step1\", \"step2\", ...],\n"
            f"  \"unknowns\": [\"unknown1\", ...],\n"
            f"  \"risks\": [\"risk1\", ...],\n"
            f"  \"confidence\": 0.0-1.0,\n"
            f"  \"need_help\": bool,\n"
            f"  \"approach\": \"what method to use\"\n"
            f"}}"
        )
        
        try:
            response = ollama.chat(
                model=model,
                messages=[
                    {"role": "system", "content": "You decompose complex problems. Think step by step."},
                    {"role": "user", "content": prompt}
                ],
                options={"temperature": 0.3}
            )
            
            content = response['message']['content'].strip()
            try:
                import json as json_module
                result = json_module.loads(content)
                return result
            except:
                return {"error": "parse_failed"}
                
        except Exception as e:
            return {"error": str(e)}


class MetaCognition:
    """
    Main meta-cognition system.
    Tracks: unknowns, uncertainties, errors, problem-solving approach
    """
    
    def __init__(self, checkpoint_path: str = "./data/metacognition.json"):
        self.checkpoint_path = checkpoint_path
        self.knowledge_gaps: List[KnowledgeGap] = []
        self.uncertainties: List[Uncertainty] = []
        self.error_detector = ErrorDetector()
        self.problem_decomposer = ProblemDecomposer()
        self.learning_events = []  # "I was wrong about X, now know Y"
        self.load()
    
    def register_unknown(self, topic: str, reason: str, priority: float = 0.5) -> None:
        """Register something we don't know."""
        gap = KnowledgeGap(topic, reason, priority)
        self.knowledge_gaps.append(gap)
        self.save()
    
    def register_uncertainty(self, statement: str, confidence: float = 0.5, 
                            reasoning: str = "") -> Uncertainty:
        """Register uncertainty about a belief."""
        uncertainty = Uncertainty(statement)
        uncertainty.confidence = confidence
        uncertainty.reasoning = reasoning
        self.uncertainties.append(uncertainty)
        self.save()
        return uncertainty
    
    def learn_from_error(self, error_description: str, correction: str) -> None:
        """Record learning from mistakes."""
        event = {
            "timestamp": time.time(),
            "error": error_description,
            "correction": correction,
            "learned": True
        }
        self.learning_events.append(event)
        self.save()
    
    def assess_confidence(self, topic: str, facts_count: int, 
                         contradiction_count: int = 0) -> float:
        """Assess confidence about a topic (0.0 = very uncertain, 1.0 = certain)."""
        base_confidence = min(1.0, facts_count / 5.0)  # Saturates at 5 facts
        contradiction_penalty = contradiction_count * 0.1
        final_confidence = max(0.0, base_confidence - contradiction_penalty)
        return round(final_confidence, 2)
    
    def get_epistemic_status(self) -> Dict[str, Any]:
        """Return current knowledge/uncertainty status."""
        return {
            "knowledge_gaps": len(self.knowledge_gaps),
            "high_priority_gaps": sum(1 for g in self.knowledge_gaps if g.priority > 0.7),
            "uncertainties": len(self.uncertainties),
            "low_confidence_beliefs": sum(1 for u in self.uncertainties if u.confidence < 0.5),
            "learning_events": len(self.learning_events),
            "last_error_fixed": self.learning_events[-1]["timestamp"] if self.learning_events else None
        }
    
    def get_confidence_explanation(self, topic: str, confidence: float) -> str:
        """Generate human-readable confidence explanation."""
        if confidence > 0.8:
            return f"I'm quite confident about {topic} (80%+) - strong evidence"
        elif confidence > 0.6:
            return f"I'm moderately confident about {topic} (60-80%) - some evidence"
        elif confidence > 0.4:
            return f"I'm uncertain about {topic} (40-60%) - contradicting signals"
        elif confidence > 0.2:
            return f"I'm very uncertain about {topic} (20-40%) - weak evidence"
        else:
            return f"I'm essentially guessing about {topic} - little/no evidence"
    
    def should_verify(self, topic: str) -> bool:
        """Decide if we should verify/double-check about this topic."""
        # Look for uncertainty about this topic
        for uncertainty in self.uncertainties:
            if topic.lower() in uncertainty.statement.lower():
                return uncertainty.confidence < 0.6
        return True  # Default: verify unfamiliar topics
    
    def save(self) -> None:
        """Persist meta-cognition state."""
        try:
            os.makedirs(os.path.dirname(self.checkpoint_path), exist_ok=True)
            data = {
                "knowledge_gaps": [g.to_dict() for g in self.knowledge_gaps],
                "uncertainties": [u.to_dict() for u in self.uncertainties],
                "learning_events": self.learning_events,
                "saved_at": time.time()
            }
            with open(self.checkpoint_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ Failed to save meta-cognition: {e}")
    
    def load(self) -> None:
        """Load meta-cognition state."""
        if os.path.exists(self.checkpoint_path):
            try:
                with open(self.checkpoint_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.knowledge_gaps = [KnowledgeGap.from_dict(g) for g in data.get("knowledge_gaps", [])]
                    self.uncertainties = [Uncertainty(u["statement"]) for u in data.get("uncertainties", [])]
                    for u, u_data in zip(self.uncertainties, data.get("uncertainties", [])):
                        u.confidence = u_data.get("confidence", 0.5)
                        u.reasoning = u_data.get("reasoning", "")
                    self.learning_events = data.get("learning_events", [])
            except Exception as e:
                print(f"⚠️ Failed to load meta-cognition: {e}")

