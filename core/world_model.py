"""
Layer 7: World Model (ภาพโลกในหัว)

The AI builds an internal representation of how the world works:
- Entities (user, self, concepts)
- Relations (knows, affects, causes)
- Rules (if X then Y)
- Predictions (what happens next)

This enables:
- Proactive behavior (not just reactive)
- Multi-step planning
- Consequence anticipation
- Causal reasoning

WITHOUT world model: AI is purely reactive
WITH world model: AI can plan and anticipate
"""

import json
import time
import os
from typing import List, Dict, Any, Optional, Tuple, Set
import ollama

class Entity:
    """A thing in the world (user, self, concept, goal)."""
    def __init__(self, name: str, entity_type: str, properties: Dict[str, Any] = None):
        self.name = name  # "User" / "Myself" / "Learning goal"
        self.entity_type = entity_type  # "person" / "ai" / "concept" / "goal"
        self.properties = properties or {}  # state, attributes
        self.relationships = {}  # name -> list of relations
        self.last_updated = time.time()
    
    def update_property(self, key: str, value: Any) -> None:
        self.properties[key] = value
        self.last_updated = time.time()
    
    def add_relation(self, relation_type: str, target: str) -> None:
        """Track relation: self ---relation_type---> target"""
        if relation_type not in self.relationships:
            self.relationships[relation_type] = []
        if target not in self.relationships[relation_type]:
            self.relationships[relation_type].append(target)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "type": self.entity_type,
            "properties": self.properties,
            "relationships": self.relationships,
            "updated": self.last_updated
        }


class CausalRule:
    """A rule: if X happens, then Y will likely follow."""
    def __init__(self, condition: str, consequence: str, probability: float = 0.7):
        self.condition = condition  # "User gets frustrated"
        self.consequence = consequence  # "User will disengage or become hostile"
        self.probability = probability  # 0.0-1.0
        self.times_observed = 1
        self.times_violated = 0
        self.learned_from = []  # List of episodes that reinforced this rule
    
    def update_probability(self, was_true: bool) -> None:
        """Update probability based on whether consequence occurred."""
        if was_true:
            self.times_observed += 1
        else:
            self.times_violated += 1
        
        # Bayesian update
        if self.times_observed + self.times_violated > 0:
            self.probability = self.times_observed / (self.times_observed + self.times_violated)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "condition": self.condition,
            "consequence": self.consequence,
            "probability": round(self.probability, 2),
            "observed": self.times_observed,
            "violated": self.times_violated
        }


class Prediction:
    """A prediction about what will happen next."""
    def __init__(self, prediction_text: str, confidence: float = 0.5):
        self.prediction = prediction_text  # "User will ask a follow-up question"
        self.confidence = confidence  # 0.0-1.0
        self.made_at = time.time()
        self.outcome = None  # "true" / "false" / None
        self.reasoning = ""
    
    def verify(self, was_true: bool) -> None:
        """Record whether prediction was correct."""
        self.outcome = "true" if was_true else "false"
        if was_true and self.confidence < 1.0:
            self.confidence = min(1.0, self.confidence + 0.1)
        elif not was_true and self.confidence > 0.0:
            self.confidence = max(0.0, self.confidence - 0.1)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "prediction": self.prediction,
            "confidence": round(self.confidence, 2),
            "made_at": self.made_at,
            "outcome": self.outcome,
            "reasoning": self.reasoning
        }


class WorldModel:
    """
    Internal representation of how the world works.
    Enables proactive behavior and consequence reasoning.
    """
    
    def __init__(self, model_path: str = "./data/world_model.json"):
        self.model_path = model_path
        self.entities: Dict[str, Entity] = {}
        self.causal_rules: List[CausalRule] = []
        self.active_predictions: List[Prediction] = []
        self.proven_consequences: List[Dict[str, Any]] = []  # cause-effect logs
        self.load()
    
    def get_or_create_entity(self, name: str, entity_type: str) -> Entity:
        """Get entity or create if doesn't exist."""
        if name not in self.entities:
            self.entities[name] = Entity(name, entity_type)
        return self.entities[name]
    
    def observe_state(self, entity_name: str, property_key: str, value: Any) -> None:
        """Update how entity state changes."""
        entity = self.get_or_create_entity(entity_name, "object")
        entity.update_property(property_key, value)
    
    def establish_relation(self, entity1: str, relation: str, entity2: str) -> None:
        """Track: entity1 ---relation---> entity2"""
        e1 = self.get_or_create_entity(entity1, "entity")
        e2 = self.get_or_create_entity(entity2, "entity")
        e1.add_relation(relation, entity2)
    
    def learn_causal_rule(self, condition: str, consequence: str, probability: float = 0.7) -> None:
        """Learn: if X happens, Y will follow."""
        # Check if rule already exists
        for rule in self.causal_rules:
            if rule.condition == condition and rule.consequence == consequence:
                rule.update_probability(True)
                return
        
        # New rule
        new_rule = CausalRule(condition, consequence, probability)
        self.causal_rules.append(new_rule)
    
    def predict_next_state(self, current_situation: str, model: str = "llama3.1") -> List[Prediction]:
        """Given current situation, predict what happens next."""
        # Get relevant causal rules
        relevant_rules = []
        for rule in self.causal_rules:
            if any(word in current_situation.lower() for word in rule.condition.lower().split()[:2]):
                relevant_rules.append(rule)
        
        rules_str = "\n".join([
            f"- If {r.condition}, then {r.consequence} ({r.probability:.0%} probability)"
            for r in relevant_rules[:5]
        ])
        
        prompt = (
            f"Given this situation: {current_situation}\n"
            f"\nBased on these patterns I've learned:\n"
            f"{rules_str if rules_str else 'No specific patterns learned'}\n\n"
            f"Predict:\n"
            f"1. What will happen next? (be specific)\n"
            f"2. Why? (causal reasoning)\n"
            f"3. How confident? (0-100%)\n"
            f"4. What should I do? (proactive action)\n\n"
            f"Output JSON:\n"
            f"[{{\n"
            f"  \"prediction\": \"what happens next\",\n"
            f"  \"reasoning\": \"why\",\n"
            f"  \"confidence\": 0.0-1.0,\n"
            f"  \"recommended_action\": \"what to do about it\"\n"
            f"}}]"
        )
        
        predictions = []
        try:
            response = ollama.chat(
                model=model,
                messages=[
                    {"role": "system", "content": "You predict consequences and help plan proactively."},
                    {"role": "user", "content": prompt}
                ],
                options={"temperature": 0.4}
            )
            
            content = response['message']['content'].strip()
            try:
                results = json.loads(content)
                if isinstance(results, list):
                    for pred_data in results:
                        pred = Prediction(
                            pred_data.get("prediction", ""),
                            pred_data.get("confidence", 0.5)
                        )
                        pred.reasoning = pred_data.get("reasoning", "")
                        predictions.append(pred)
                        self.active_predictions.append(pred)
            except:
                pass
        except Exception as e:
            print(f"⚠️ Prediction failed: {e}")
        
        return predictions
    
    def record_consequence(self, action: str, outcome: str, was_predicted: bool = False) -> None:
        """Record: action led to outcome."""
        consequence = {
            "timestamp": time.time(),
            "action": action,
            "outcome": outcome,
            "was_predicted": was_predicted
        }
        self.proven_consequences.append(consequence)
        
        # Update relevant causal rules
        for rule in self.causal_rules:
            if action.lower() in rule.condition.lower():
                rule.update_probability(outcome.lower() in rule.consequence.lower())
    
    def simulate_action(self, action: str, model: str = "llama3.1") -> Dict[str, Any]:
        """Simulate: "What happens if I do X?" - Consequence anticipation."""
        prompt = (
            f"I'm considering this action: {action}\n\n"
            f"Simulate consequences:\n"
            f"1. What happens immediately? (short-term)\n"
            f"2. What cascades from that? (medium-term: 1 day)\n"
            f"3. What's the ultimate impact? (long-term: 1 week)\n"
            f"4. What could go wrong?\n"
            f"5. Are there any good outcomes?\n"
            f"6. Net recommendation: do it or not?\n\n"
            f"Output JSON:\n"
            f"{{\n"
            f"  \"immediate\": \"what happens right away\",\n"
            f"  \"cascade\": \"what follows from that\",\n"
            f"  \"long_term\": \"ultimate impact\",\n"
            f"  \"risks\": [\"risk1\", \"risk2\"],\n"
            f"  \"benefits\": [\"benefit1\", \"benefit2\"],\n"
            f"  \"recommendation\": \"do_it/avoid_it/uncertain\",\n"
            f"  \"confidence\": 0.0-1.0\n"
            f"}}"
        )
        
        try:
            response = ollama.chat(
                model=model,
                messages=[
                    {"role": "system", "content": "Simulate consequences with reasoning."},
                    {"role": "user", "content": prompt}
                ],
                options={"temperature": 0.3}
            )
            
            content = response['message']['content'].strip()
            try:
                result = json.loads(content)
                return result
            except:
                return {"error": "parse_failed"}
                
        except Exception as e:
            return {"error": str(e)}
    
    def get_world_summary(self) -> Dict[str, Any]:
        """Get current understanding of the world."""
        return {
            "entities_known": len(self.entities),
            "causal_rules": len(self.causal_rules),
            "active_predictions": len(self.active_predictions),
            "proven_consequences": len(self.proven_consequences),
            "high_confidence_rules": sum(1 for r in self.causal_rules if r.probability > 0.7),
            "recent_prediction_accuracy": self._calc_prediction_accuracy()
        }
    
    def _calc_prediction_accuracy(self) -> float:
        """Calculate accuracy of recent predictions."""
        verified = [p for p in self.active_predictions if p.outcome is not None]
        if not verified:
            return 0.0
        correct = sum(1 for p in verified if p.outcome == "true")
        return correct / len(verified) if verified else 0.0
    
    def save(self) -> None:
        """Persist world model."""
        try:
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            data = {
                "entities": {name: e.to_dict() for name, e in self.entities.items()},
                "causal_rules": [r.to_dict() for r in self.causal_rules],
                "recent_predictions": [p.to_dict() for p in self.active_predictions[-20:]],
                "consequences_log": self.proven_consequences[-50:],
                "saved_at": time.time()
            }
            with open(self.model_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ Failed to save world model: {e}")
    
    def load(self) -> None:
        """Load world model from disk."""
        if os.path.exists(self.model_path):
            try:
                with open(self.model_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    # Restore entities
                    for name, entity_data in data.get("entities", {}).items():
                        entity = Entity(entity_data["name"], entity_data["type"], entity_data.get("properties", {}))
                        entity.relationships = entity_data.get("relationships", {})
                        self.entities[name] = entity
                    
                    # Restore rules
                    for rule_data in data.get("causal_rules", []):
                        rule = CausalRule(rule_data["condition"], rule_data["consequence"], rule_data.get("probability", 0.7))
                        rule.times_observed = rule_data.get("observed", 1)
                        rule.times_violated = rule_data.get("violated", 0)
                        self.causal_rules.append(rule)
                    
                    # Restore recent predictions
                    for pred_data in data.get("recent_predictions", []):
                        pred = Prediction(pred_data["prediction"], pred_data.get("confidence", 0.5))
                        pred.outcome = pred_data.get("outcome")
                        self.active_predictions.append(pred)
                    
                    self.proven_consequences = data.get("consequences_log", [])
                    
            except Exception as e:
                print(f"⚠️ Failed to load world model: {e}")

