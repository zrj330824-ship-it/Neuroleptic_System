#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Neural Field System - Continuous Cognitive Architecture

🧠 Single Field with Timescale Separation
├─ Fast manifold ← spaCy perception (sensory cortex)
├─ Slow manifold ← cognitive attractors (cortex)
└─ Ultra-slow ← memory structure (hippocampus)

Key Principles:
- Perception = state perturbation (NOT translation)
- Understanding = attractor convergence (NOT decoding)
- Memory = energy landscape change (NOT storage)
"""

import numpy as np
import spacy
from typing import List, Optional, Tuple


class NeuralField:
    """
    Continuous neural field with reaction-diffusion dynamics.
    
    Dynamics: ∂ϕ/∂t = Δϕ + f(ϕ) + sensory_perturbation
    """
    
    def __init__(self, size: int = 64, dt: float = 0.1):
        self.size = size
        self.dt = dt
        self.state = np.random.randn(size, size) * 0.01
        
    def laplacian(self, x: np.ndarray) -> np.ndarray:
        """Discrete Laplacian operator (diffusion)."""
        return (
            np.roll(x, 1, 0) + np.roll(x, -1, 0) +
            np.roll(x, 1, 1) + np.roll(x, -1, 1) -
            4 * x
        )
    
    def evolve(self, steps: int = 20, perturbation: Optional[np.ndarray] = None,
               tau: float = 1.0) -> np.ndarray:
        """
        Evolve field with optional perturbation.
        
        Args:
            steps: Number of evolution steps
            perturbation: Sensory input (added each step, decays with tau)
            tau: Perturbation decay timescale (fast=0.1, slow=1.0)
        """
        for step in range(steps):
            # Diffusion term
            diffusion = self.laplacian(self.state)
            
            # Reaction term (simple cubic nonlinearity)
            reaction = self.state - self.state ** 3
            
            # Perturbation (decays over time)
            if perturbation is not None:
                decay = np.exp(-step / (tau * steps))
                self.state += self.dt * decay * perturbation
            
            # Update
            self.state += self.dt * (diffusion + reaction)
        
        return self.state


class AttractorMemory:
    """
    Hippocampus-like attractor memory.
    
    Memory is NOT stored as vectors.
    Memory CHANGES the energy landscape.
    
    Energy: E = ∫(||∇ϕ||² + Σᵢ λᵢ||ϕ - Aᵢ||²) dx dy
    """
    
    def __init__(self, capacity: int = 10):
        self.attractors: List[np.ndarray] = []
        self.strengths: List[float] = []
        self.capacity = capacity
    
    def store(self, state: np.ndarray, strength: float = 1.0):
        """
        Consolidate memory (change energy landscape).
        
        Args:
            state: Field state to remember
            strength: λᵢ (attractor strength)
        """
        if len(self.attractors) >= self.capacity:
            # Forget oldest
            self.attractors.pop(0)
            self.strengths.pop(0)
        
        self.attractors.append(state.copy())
        self.strengths.append(strength)
    
    def energy(self, field: np.ndarray) -> float:
        """
        Compute energy relative to stored attractors.
        
        Low energy = system is near a memory.
        """
        if not self.attractors:
            return float('inf')
        
        total_energy = 0.0
        for attractor, strength in zip(self.attractors, self.strengths):
            total_energy += strength * np.sum((field - attractor) ** 2)
        
        return total_energy
    
    def recall_force(self, field: np.ndarray) -> np.ndarray:
        """
        Compute attractor force (pulls field toward memories).
        
        Force: F = -Σᵢ λᵢ(ϕ - Aᵢ)
        """
        if not self.attractors:
            return np.zeros_like(field)
        
        force = np.zeros_like(field)
        for attractor, strength in zip(self.attractors, self.strengths):
            force -= strength * (field - attractor)
        
        return force


class NeuralFieldSystem:
    """
    Complete cognitive system with perception, cognition, and memory.
    
    Architecture:
    [ Neural Field System ]
    ├── field: Continuous dynamics (cortex)
    ├── perception: spaCy (sensory cortex)
    └── memory: AttractorMemory (hippocampus)
    
    ⚠️ FIVE THINGS THIS SYSTEM NEVER DOES:
    1. ❌ No token → symbol → logic pipeline
    2. ❌ No explicit "answer" module
    3. ❌ No attention / softmax
    4. ❌ No embedding lookup tables
    5. ❌ No pursuit of "general conversation"
    """
    
    def __init__(self, field_size: int = 64, spacy_model: str = "en_core_web_sm"):
        self.field = NeuralField(size=field_size)
        self.memory = AttractorMemory(capacity=10)
        self.perception = spacy.load(spacy_model)
        
        # Timescale parameters
        self.tau_perception = 0.1  # Fast: sensory decay
        self.tau_cognition = 1.0   # Slow: cognitive evolution
        self.tau_memory = 10.0     # Ultra-slow: memory consolidation
    
    def see(self, text: str) -> np.ndarray:
        """
        Perceive text as sensory perturbation.
        
        NOT: parse → understand → store
        BUT: perturb → self-organize → stabilize
        
        Language is a perturbation to the field, not an input to process.
        """
        doc = self.perception(text)
        
        # Create perturbation pattern from linguistic features
        perturbation = np.zeros_like(self.field.state)
        
        for token in doc:
            # Lemma → spatial position (hash-based)
            x = hash(token.lemma_) % self.field.size
            y = hash(token.pos_) % self.field.size
            
            # Dependency → perturbation strength
            strength = 1.0 / (1.0 + len(token.dep_))
            
            perturbation[x, y] += strength
        
        # Inject perturbation (fast timescale)
        self.field.evolve(steps=10, perturbation=perturbation, tau=self.tau_perception)
        
        return self.field.state
    
    def think(self, steps: int = 50) -> np.ndarray:
        """
        Let the field evolve freely (no external input).
        
        This is where "understanding" emerges:
        - System self-organizes
        - Falls into attractor basins
        - Stabilizes into coherent pattern
        """
        # Include memory attractor force during thinking
        for _ in range(steps):
            # Free evolution
            self.field.evolve(steps=1, tau=self.tau_cognition)
            
            # Memory pull (weak, ultra-slow timescale)
            if self.memory.attractors:
                memory_force = self.memory.recall_force(self.field.state) * 0.01
                self.field.state += memory_force
        
        return self.field.state
    
    def learn(self, label: str = ""):
        """
        Consolidate current state into memory.
        
        This CHANGES the energy landscape.
        Future states will be attracted to this pattern.
        """
        self.memory.store(self.field.state, strength=1.0)
        
        if label:
            # Associate label with this memory pattern
            # (In full version: label becomes part of attractor)
            pass
    
    def recognize(self, text: str) -> Tuple[float, str]:
        """
        Check if input matches existing memories.
        
        Returns: (energy, description)
        Low energy = familiar pattern.
        High energy = novel pattern.
        """
        # Store initial state
        initial = self.field.state.copy()
        
        # Perceive
        self.see(text)
        
        # Let system settle
        self.think(steps=30)
        
        # Measure energy relative to memories
        energy = self.memory.energy(self.field.state)
        
        # Restore state (don't permanently change for recognition)
        self.field.state = initial
        
        status = "familiar" if energy < 100 else "novel"
        return energy, status
    
    def complete(self, partial: str, steps: int = 100) -> dict:
        """
        Pattern completion via attractor dynamics.
        
        Input partial pattern → system evolves → completes to nearest attractor.
        """
        # Encode partial input
        self.see(partial)
        
        # Let system evolve to attractor
        final_state = self.think(steps)
        
        # Measure which memory it's closest to
        energy = self.memory.energy(final_state)
        
        return {
            'completed': True,
            'energy': float(energy),
            'final_activation': float(np.sum(final_state ** 2)),
            'stability': float(np.std(np.gradient(final_state)))
        }


def demo():
    """
    Demo: Neural Field System with embodied perception.
    
    Shows:
    1. Perception as perturbation
    2. Memory as energy landscape
    3. Recognition as attractor convergence
    """
    print("="*60)
    print("🧠 Neural Field System - Continuous Cognitive Architecture")
    print("="*60)
    
    # Create system
    brain = NeuralFieldSystem(field_size=64)
    
    # ===== Phase 1: Learning (Baby's first experiences) =====
    print("\n📚 Phase 1: Learning (Forming attractors)")
    
    experiences = [
        "The cat sits on the mat",
        "A dog runs in the park",
        "Birds fly in the sky"
    ]
    
    for i, text in enumerate(experiences):
        brain.see(text)
        brain.think(steps=50)
        brain.learn(label=f"memory_{i}")
        print(f"   Learned: '{text[:30]}...'")
    
    # ===== Phase 2: Recognition (Familiar vs Novel) =====
    print("\n👁️ Phase 2: Recognition")
    
    test_inputs = [
        "The cat sits on the mat",  # Familiar
        "A cat sits on a mat",      # Similar
        "Quantum physics is weird"  # Novel
    ]
    
    for text in test_inputs:
        energy, status = brain.recognize(text)
        print(f"   '{text[:30]}...' → {status} (energy={energy:.1f})")
    
    # ===== Phase 3: Pattern Completion =====
    print("\n🧩 Phase 3: Pattern Completion")
    
    partial = "The cat"
    result = brain.complete(partial, steps=100)
    print(f"   Input: '{partial}'")
    print(f"   Completed: energy={result['energy']:.1f}, activation={result['final_activation']:.1f}")
    
    # ===== Phase 4: Memory Association =====
    print("\n🔗 Phase 4: Memory Association")
    
    # Learn association: bell → food
    brain.see("bell rings")
    brain.think(30)
    brain.learn()
    
    brain.see("food arrives")
    brain.think(30)
    brain.learn()
    
    # Test: does "bell" activate "food" memory?
    energy_before = brain.memory.energy(brain.field.state)
    brain.see("bell")
    brain.think(50)
    energy_after = brain.memory.energy(brain.field.state)
    
    print(f"   'bell rings' → 'food arrives'")
    print(f"   Energy change: {energy_before:.1f} → {energy_after:.1f}")
    
    print("\n" + "="*60)
    print("✅ Demo completed!")
    print("="*60)
    print("\n⚠️ This system NEVER:")
    print("   1. ❌ Token → symbol → logic pipeline")
    print("   2. ❌ Explicit 'answer' module")
    print("   3. ❌ Attention / softmax")
    print("   4. ❌ Embedding lookup tables")
    print("   5. ❌ General conversation")
    print("\n✅ This system IS:")
    print("   - Continuous cognitive dynamics")
    print("   - Embodied perception (spaCy as sensory cortex)")
    print("   - Memory as energy landscape")
    print("   - Understanding as attractor convergence")


if __name__ == "__main__":
    demo()
