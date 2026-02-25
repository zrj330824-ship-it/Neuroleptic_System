#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Neural Field ↔ spaCy Interface
Baby Brain (Neural Field) ↔ Symbol System (spaCy)

Architecture:
[ Text ] → spaCy → [ Symbols ] → Neural Field → [ Patterns ] → spaCy → [ Text ]
"""

import spacy
import numpy as np
from typing import Dict, List, Optional, Tuple


class NeuralFieldSpacyInterface:
    """
    Connects Neural Field dynamics with spaCy symbolic processing.
    
    Analogy:
    - Neural Field (15M params) = Baby Brain (sensorimotor, patterns)
    - spaCy = Language System (symbols, grammar)
    """
    
    def __init__(self, neural_field, spacy_model: str = "en_core_web_sm"):
        """
        Args:
            neural_field: NeuralField2D instance (the "baby brain")
            spacy_model: spaCy model name
        """
        self.nlp = spacy.load(spacy_model)
        self.field = neural_field
        
        # Symbol grounding: map linguistic features to field states
        self.pos_encoding = {
            'NOUN': 0.8, 'VERB': 0.6, 'ADJ': 0.7, 'ADV': 0.5,
            'PRON': 0.4, 'DET': 0.3, 'ADP': 0.4, 'CONJ': 0.3,
            'NUM': 0.9, 'PART': 0.2, 'INTJ': 0.1
        }
        
    def text_to_field_state(self, text: str) -> np.ndarray:
        """
        Convert text to Neural Field initial state.
        
        Process:
        1. Parse text with spaCy
        2. Extract linguistic features (POS, dependencies)
        3. Encode as field activation pattern
        """
        doc = self.nlp(text)
        
        # Create activation pattern from tokens
        activations = []
        for token in doc:
            # Encode POS as activation level
            pos_val = self.pos_encoding.get(token.pos_, 0.5)
            
            # Encode dependency as spatial position
            dep_hash = hash(token.dep_) % 100
            
            activations.append((dep_hash, pos_val))
        
        # Convert to field state (2D grid)
        field_state = np.zeros(self.field.shape)
        
        for i, (pos, val) in enumerate(activations):
            x = pos % self.field.shape[0]
            y = i % self.field.shape[1]
            field_state[x, y] = val
        
        return field_state
    
    def field_state_to_text(self, field_state: Optional[np.ndarray] = None,
                           template: str = "Pattern: {pattern}") -> str:
        """
        Convert Neural Field state to text description.
        
        Process:
        1. Extract pattern from field (attractors, energy)
        2. Generate symbolic description
        """
        if field_state is None:
            field_state = self.field.state
        
        # Extract features
        energy = np.sum(field_state ** 2)
        stability = self._measure_stability(field_state)
        dominant_region = self._find_dominant_region(field_state)
        
        # Generate description
        description = template.format(
            pattern=f"energy={energy:.2f}, stability={stability:.2f}",
            region=dominant_region
        )
        
        return description
    
    def complete_pattern(self, partial_text: str, steps: int = 50) -> str:
        """
        Use Neural Field to complete a pattern from partial text.
        
        Analogy: Baby sees half a pattern → completes it
        
        Process:
        1. Encode partial text → field state
        2. Let field evolve (attractor dynamics)
        3. Decode evolved state → completed description
        """
        # Initialize field from partial input
        initial_state = self.text_to_field_state(partial_text)
        self.field.state = initial_state.copy()
        
        # Let field evolve to attractor
        final_state = self.field.evolve(steps=steps)
        
        # Decode to text
        completion = self.field_state_to_text(
            final_state,
            template="Completed: {pattern} in region {region}"
        )
        
        return completion
    
    def associate(self, text1: str, text2: str, steps: int = 100) -> Dict:
        """
        Form associative memory between two texts.
        
        Analogy: Baby learns "bell → food" association
        
        Process:
        1. Encode both texts
        2. Let field learn association (Hebbian)
        3. Measure association strength
        """
        state1 = self.text_to_field_state(text1)
        state2 = self.text_to_field_state(text2)
        
        # Measure overlap (association strength)
        overlap = np.sum(state1 * state2) / (np.linalg.norm(state1) * np.linalg.norm(state2))
        
        return {
            'association_strength': float(overlap),
            'text1_energy': float(np.sum(state1 ** 2)),
            'text2_energy': float(np.sum(state2 ** 2))
        }
    
    def _measure_stability(self, state: np.ndarray) -> float:
        """Measure how stable the field state is (low energy gradient)."""
        gradient = np.gradient(state)
        gradient_magnitude = np.sqrt(np.sum(np.array([g ** 2 for g in gradient])))
        return float(1.0 / (1.0 + gradient_magnitude))
    
    def _find_dominant_region(self, state: np.ndarray) -> str:
        """Find the most active region in the field."""
        h, w = state.shape
        quadrants = [
            ('top-left', state[:h//2, :w//2]),
            ('top-right', state[:h//2, w//2:]),
            ('bottom-left', state[h//2:, :w//2]),
            ('bottom-right', state[h//2:, w//2:])
        ]
        
        energies = [(name, np.sum(region ** 2)) for name, region in quadrants]
        return max(energies, key=lambda x: x[1])[0]


def demo():
    """Demo: Neural Field + spaCy interface"""
    print("="*60)
    print("🧠 Neural Field ↔ spaCy Interface Demo")
    print("="*60)
    
    # Import neural field
    import sys
    sys.path.insert(0, '/home/jerry/.openclaw/workspace/neuro_symbolic_reasoner/core')
    from neural_field_2d import NeuralField2D
    
    # Create interface
    field = NeuralField2D(shape=(50, 50))
    interface = NeuralFieldSpacyInterface(field)
    
    # Test 1: Text → Field
    print("\n1️⃣ Text to Field State:")
    text = "The cat sits on the mat"
    state = interface.text_to_field_state(text)
    print(f"   Input: '{text}'")
    print(f"   Field shape: {state.shape}")
    print(f"   Activation sum: {np.sum(state):.2f}")
    
    # Test 2: Pattern Completion
    print("\n2️⃣ Pattern Completion:")
    partial = "The dog"
    completion = interface.complete_pattern(partial, steps=50)
    print(f"   Partial: '{partial}'")
    print(f"   Completion: {completion}")
    
    # Test 3: Association
    print("\n3️⃣ Associative Memory:")
    assoc = interface.associate("bell rings", "food arrives")
    print(f"   'bell rings' ↔ 'food arrives'")
    print(f"   Association strength: {assoc['association_strength']:.3f}")
    
    print("\n" + "="*60)
    print("✅ Demo completed!")
    print("="*60)


if __name__ == "__main__":
    demo()
