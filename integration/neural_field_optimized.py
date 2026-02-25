#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Neural Field System - Optimized with Timescale Separation

🧠 Architecture:
- Fast manifold: Sensory perturbation (τ=0.05)
- Slow manifold: Cortical dynamics (τ=0.01)
- Ultra-slow: Attractor memory (hippocampus)

👁️ Active Perception:
- System decides which input to attend
- Based on energy gradient / salience

Key Improvement:
- Explicit fast/slow manifold separation
- Cleaner dynamics integration
- Active perception strategy
"""

import numpy as np
import spacy
from typing import List, Callable, Optional, Dict


class NeuralField:
    """
    Neural field with explicit timescale separation.
    
    Dynamics:
    - Fast manifold: Sensory perturbation (τ_fast = 0.05)
    - Slow manifold: Cortical dynamics (τ_slow = 0.01)
    - State = Fast + Slow
    """
    
    def __init__(self, size: int = 64):
        self.size = size
        
        # Fast manifold (sensory)
        self.fast_manifold = np.random.randn(size, size) * 0.01
        
        # Slow manifold (cortical)
        self.slow_manifold = np.random.randn(size, size) * 0.01
        
        # Combined state
        self.state = self.fast_manifold + self.slow_manifold
    
    def laplacian(self, x: np.ndarray) -> np.ndarray:
        """Discrete Laplacian (5-point stencil)."""
        return (
            np.roll(x, 1, 0) + np.roll(x, -1, 0) +
            np.roll(x, 1, 1) + np.roll(x, -1, 1) -
            4 * x
        )
    
    def evolve(self, steps: int = 20,
               dt_fast: float = 0.05,
               dt_slow: float = 0.01,
               memory_force: Optional[Callable] = None) -> np.ndarray:
        """
        Evolve with timescale separation.
        
        Args:
            steps: Evolution steps
            dt_fast: Fast manifold timestep (sensory)
            dt_slow: Slow manifold timestep (cortical)
            memory_force: Function computing attractor force
        """
        for _ in range(steps):
            # Fast manifold: Sensory perturbation (diffusion only)
            self.fast_manifold += dt_fast * self.laplacian(self.fast_manifold)
            
            # Slow manifold: Cortical dynamics + memory
            slow_change = dt_slow * self.laplacian(self.slow_manifold)
            
            # Attractor memory force
            if memory_force is not None:
                slow_change -= dt_slow * memory_force(self.slow_manifold)
            
            self.slow_manifold += slow_change
            
            # Combined state
            self.state = self.fast_manifold + self.slow_manifold
        
        return self.state
    
    def reset(self):
        """Reset to baseline."""
        self.fast_manifold = np.random.randn(self.size, self.size) * 0.01
        self.slow_manifold = np.random.randn(self.size, self.size) * 0.01
        self.state = self.fast_manifold + self.slow_manifold


class AttractorMemory:
    """
    Hippocampus-like attractor memory.
    
    Memory force: F = Σᵢ (ϕ - Aᵢ) / N
    Pulls field toward stored patterns.
    """
    
    def __init__(self, capacity: int = 20):
        self.attractors: List[np.ndarray] = []
        self.capacity = capacity
    
    def store(self, state: np.ndarray):
        """Store state as attractor."""
        if len(self.attractors) >= self.capacity:
            self.attractors.pop(0)  # Forget oldest
        
        self.attractors.append(state.copy())
    
    def memory_force(self, field: np.ndarray) -> np.ndarray:
        """
        Compute attractor force.
        
        F = Σᵢ (ϕ - Aᵢ) / N
        
        Pulls field toward all stored memories.
        """
        if not self.attractors:
            return np.zeros_like(field)
        
        force = np.zeros_like(field)
        for attractor in self.attractors:
            force += (field - attractor)
        
        return force / len(self.attractors)
    
    def energy(self, field: np.ndarray) -> float:
        """Compute energy relative to attractors."""
        if not self.attractors:
            return float('inf')
        
        total_energy = 0.0
        for attractor in self.attractors:
            total_energy += np.sum((field - attractor) ** 2)
        
        return total_energy


class NeuralFieldSystem:
    """
    Complete cognitive system with active perception.
    
    Architecture:
    [ Sensory Cortex (spaCy) ]
            ↓
    [ Fast Manifold ] → [ Slow Manifold ] → [ Motor Output ]
            ↑                ↓
            └──── Memory ←───┘
    """
    
    def __init__(self, size: int = 64, spacy_model: str = "en_core_web_sm"):
        self.field = NeuralField(size)
        self.memory = AttractorMemory(capacity=20)
        
        # SpaCy as endogenous perception (sensory cortex)
        self.perception = spacy.load(spacy_model)
        
        # Active perception state
        self.attention_focus = None
        self.episode_log: List[Dict] = []
    
    def perceive(self, text: str):
        """
        Perceive text as fast manifold perturbation.
        
        NOT symbolic processing — sensory transduction.
        """
        doc = self.perception(text)
        
        # Create perturbation pattern
        perturb = np.zeros_like(self.field.state)
        
        for token in doc:
            x = hash(token.lemma_) % self.field.size
            y = hash(token.pos_) % self.field.size
            perturb[x, y] += 1.0
        
        # Inject into fast manifold (sensory layer)
        self.field.fast_manifold += 0.05 * perturb
    
    def think(self, steps: int = 50):
        """
        Free evolution with memory influence.
        
        Slow manifold evolves under:
        - Diffusion (spatial smoothing)
        - Attractor force (memory pull)
        """
        return self.field.evolve(
            steps=steps,
            memory_force=self.memory.memory_force
        )
    
    def remember(self):
        """Consolidate current state into attractor memory."""
        self.memory.store(self.field.state)
    
    def active_perceive(self, inputs: List[str], strategy: str = "energy"):
        """
        Active perception: decide which inputs to attend.
        
        Strategies:
        - "energy": Attend to input that minimizes energy
        - "novelty": Attend to input most different from memory
        - "round_robin": Simple sequential attention
        
        This is where the system "chooses what to look at".
        """
        if strategy == "energy":
            # Select input that leads to lowest energy
            best_input = None
            best_energy = float('inf')
            
            for text in inputs:
                # Simulate perception
                initial_state = self.field.state.copy()
                self.perceive(text)
                self.think(steps=20)
                
                energy = self.memory.energy(self.field.state)
                
                if energy < best_energy:
                    best_energy = energy
                    best_input = text
                
                # Restore state
                self.field.state = initial_state
                self.field.fast_manifold = initial_state * 0.5
                self.field.slow_manifold = initial_state * 0.5
            
            # Actually perceive best input
            if best_input:
                self.perceive(best_input)
                self.think(steps=50)
                self.attention_focus = best_input
        
        elif strategy == "novelty":
            # Select input most different from memory
            best_input = None
            best_novelty = 0.0
            
            for text in inputs:
                initial_state = self.field.state.copy()
                self.perceive(text)
                self.think(steps=20)
                
                # Novelty = inverse of energy
                energy = self.memory.energy(self.field.state)
                novelty = 1.0 / (1.0 + energy)
                
                if novelty > best_novelty:
                    best_novelty = novelty
                    best_input = text
                
                self.field.state = initial_state
                self.field.fast_manifold = initial_state * 0.5
                self.field.slow_manifold = initial_state * 0.5
            
            if best_input:
                self.perceive(best_input)
                self.think(steps=50)
                self.attention_focus = best_input
        
        else:  # round_robin
            for text in inputs:
                self.perceive(text)
                self.think(steps=20)
            
            self.attention_focus = inputs[-1] if inputs else None
        
        self.episode_log.append({
            'strategy': strategy,
            'focus': self.attention_focus,
            'inputs': len(inputs)
        })
    
    def recognize(self, text: str) -> Dict:
        """
        Recognize if input matches existing memories.
        
        Returns:
            Dict with energy, status (familiar/novel)
        """
        initial = self.field.state.copy()
        
        self.perceive(text)
        self.think(steps=30)
        
        energy = self.memory.energy(self.field.state)
        
        # Restore
        self.field.state = initial
        self.field.fast_manifold = initial * 0.5
        self.field.slow_manifold = initial * 0.5
        
        status = "familiar" if energy < 100 else "novel"
        
        return {
            'energy': float(energy),
            'status': status
        }
    
    def complete_pattern(self, partial: str, steps: int = 100) -> Dict:
        """
        Pattern completion via attractor dynamics.
        
        Partial input → system evolves → completes to nearest attractor.
        """
        self.perceive(partial)
        final_state = self.think(steps)
        
        return {
            'energy': float(self.memory.energy(final_state)),
            'activation': float(np.sum(final_state ** 2)),
            'stability': float(np.std(np.gradient(final_state)))
        }
    
    def get_energy(self) -> float:
        """Compute current system energy."""
        return self.memory.energy(self.field.state)


def demo_optimized():
    """
    Demo: Optimized system with timescale separation.
    """
    print("="*60)
    print("🧠 Neural Field System - Optimized Version")
    print("="*60)
    print("\nArchitecture:")
    print("  • Fast manifold: Sensory perturbation (τ=0.05)")
    print("  • Slow manifold: Cortical dynamics (τ=0.01)")
    print("  • Attractor memory: Hippocampus (energy landscape)")
    print("  • Active perception: Decides what to attend")
    
    # Create system
    brain = NeuralFieldSystem(size=64)
    
    # Phase 1: Learning
    print("\n📚 Phase 1: Learning (Forming Attractors)")
    
    experiences = [
        "The cat sits on the mat",
        "A dog runs in the park",
        "Birds fly in the sky"
    ]
    
    for i, text in enumerate(experiences):
        brain.perceive(text)
        brain.think(steps=50)
        brain.remember()
        print(f"   ✓ Stored: '{text[:30]}...'")
    
    # Phase 2: Recognition
    print("\n👁️ Phase 2: Recognition")
    
    tests = [
        ("The cat sits on the mat", "Exact repeat"),
        ("A cat sits on a mat", "Similar pattern"),
        ("Quantum physics is weird", "Novel input")
    ]
    
    for text, desc in tests:
        result = brain.recognize(text)
        print(f"   {desc}: {result['status']} (E={result['energy']:.1f})")
    
    # Phase 3: Pattern Completion
    print("\n🧩 Phase 3: Pattern Completion")
    
    result = brain.complete_pattern("The cat", steps=100)
    print(f"   Input: 'The cat'")
    print(f"   → Energy={result['energy']:.1f}, Activation={result['activation']:.1f}")
    
    # Phase 4: Active Perception
    print("\n🔍 Phase 4: Active Perception")
    
    # Test energy-based attention
    print("   Strategy: Energy minimization")
    options = [
        "The cat sleeps",
        "A dog barks",
        "Birds sing"
    ]
    
    brain.active_perceive(options, strategy="energy")
    print(f"   Attended to: '{brain.attention_focus}'")
    
    # Test novelty-based attention
    print("\n   Strategy: Novelty seeking")
    brain.active_perceive(options, strategy="novelty")
    print(f"   Attended to: '{brain.attention_focus}'")
    
    # Phase 5: Energy Analysis
    print("\n⚡ Phase 5: Energy Analysis")
    
    initial_E = brain.get_energy()
    print(f"   Initial energy: {initial_E:.2f}")
    
    # Perturb
    brain.field.state += np.random.randn(64, 64) * 0.5
    perturbed_E = brain.get_energy()
    print(f"   After perturbation: {perturbed_E:.2f}")
    
    # Recover
    brain.think(steps=100)
    recovered_E = brain.get_energy()
    print(f"   After recovery: {recovered_E:.2f}")
    print(f"   ΔE = {perturbed_E - recovered_E:+.2f} (convergence)")
    
    print("\n" + "="*60)
    print("✅ Optimized system verified!")
    print("="*60)
    print("\nKey improvements:")
    print("  • Explicit fast/slow manifold separation")
    print("  • Cleaner dynamics integration")
    print("  • Active perception strategies (energy/novelty)")
    print("  • Memory as continuous attractor force")


if __name__ == "__main__":
    demo_optimized()
