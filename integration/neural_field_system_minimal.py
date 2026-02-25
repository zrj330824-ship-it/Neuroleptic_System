#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Neural Field System - Minimal Viable Version

🧠 Single Field Architecture:
NeuralFieldSystem
├─ field_state      # 连续场（皮层）
├─ dynamics         # 场动力学（拉普拉斯扩散）
├─ perception       # spaCy（感觉皮层）
└─ memory           # 吸引子（海马体）

Key Principles:
- Perception = state perturbation (NOT translation)
- Understanding = attractor convergence (NOT decoding)
- Memory = energy landscape change (NOT storage)
"""

import numpy as np
from typing import List, Tuple

# Import dual-mode sensory cortex
from sensory_cortex import SensoryCortex


class NeuralField:
    """
    Continuous neural field with reaction-diffusion dynamics.
    
    ∂ϕ/∂t = Δϕ + f(ϕ)
    """
    
    def __init__(self, size: int = 64, dt: float = 0.1):
        self.size = size
        self.dt = dt
        self.state = np.random.randn(size, size) * 0.01
        
    def laplacian(self, x: np.ndarray) -> np.ndarray:
        """Discrete Laplacian (diffusion)."""
        return (
            np.roll(x, 1, 0) + np.roll(x, -1, 0) +
            np.roll(x, 1, 1) + np.roll(x, -1, 1) -
            4 * x
        )
    
    def evolve(self, steps: int = 20, perturbation: np.ndarray = None,
               tau: float = 1.0) -> np.ndarray:
        """
        Evolve field with optional perturbation.
        
        Args:
            steps: Evolution steps
            perturbation: Sensory input (decays with tau)
            tau: Timescale (fast=0.1, slow=1.0)
        """
        for step in range(steps):
            # Diffusion
            diffusion = self.laplacian(self.state)
            
            # Reaction (cubic nonlinearity for stability)
            reaction = self.state - self.state ** 3
            
            # Perturbation (decays)
            if perturbation is not None:
                decay = np.exp(-step / (tau * steps))
                self.state += self.dt * decay * perturbation
            
            # Update
            self.state += self.dt * (diffusion + reaction)
        
        return self.state


class AttractorMemory:
    """
    Hippocampus-like attractor memory.
    
    Memory CHANGES energy landscape, doesn't "store" vectors.
    
    Energy: E = Σᵢ λᵢ||ϕ - Aᵢ||²
    Force: F = -Σᵢ λᵢ(ϕ - Aᵢ)
    """
    
    def __init__(self, capacity: int = 10):
        self.attractors: List[np.ndarray] = []
        self.strengths: List[float] = []
        self.capacity = capacity
    
    def store(self, state: np.ndarray, strength: float = 1.0):
        """Consolidate memory (change energy landscape)."""
        if len(self.attractors) >= self.capacity:
            self.attractors.pop(0)
            self.strengths.pop(0)
        
        self.attractors.append(state.copy())
        self.strengths.append(strength)
    
    def energy(self, field: np.ndarray) -> float:
        """Energy relative to attractors (low = near memory)."""
        if not self.attractors:
            return float('inf')
        
        total = 0.0
        for attractor, strength in zip(self.attractors, self.strengths):
            total += strength * np.sum((field - attractor) ** 2)
        
        return total
    
    def recall_force(self, field: np.ndarray) -> np.ndarray:
        """Attractor force: F = -Σᵢ λᵢ(ϕ - Aᵢ)"""
        if not self.attractors:
            return np.zeros_like(field)
        
        force = np.zeros_like(field)
        for attractor, strength in zip(self.attractors, self.strengths):
            force -= strength * (field - attractor)
        
        return force


class NeuralFieldSystem:
    """
    Complete cognitive system.
    
    Architecture:
    [ NeuralFieldSystem ]
    ├── field: Continuous dynamics (cortex)
    ├── perception: spaCy (sensory cortex)
    └── memory: AttractorMemory (hippocampus)
    
    ⚠️ FIVE THINGS WE NEVER DO:
    1. ❌ Token → symbol → logic pipeline
    2. ❌ Explicit "answer" module
    3. ❌ Attention / softmax
    4. ❌ Embedding lookup tables
    5. ❌ General conversation
    """
    
    def __init__(self, size: int = 64, perception_mode: str = "spacy"):
        self.field = NeuralField(size=size)
        self.memory = AttractorMemory(capacity=10)
        self.perception = SensoryCortex(mode=perception_mode, field_size=size)
        
        # Timescale parameters
        self.tau_perception = 0.1   # Fast: sensory decay
        self.tau_cognition = 1.0    # Slow: field evolution
        self.tau_memory = 10.0      # Ultra-slow: consolidation
    
    def see(self, text: str) -> np.ndarray:
        """
        Perceive text as sensory perturbation.
        
        NOT: parse → understand → store
        BUT: perturb → self-organize → stabilize
        """
        # Use sensory cortex (dual-mode)
        perturbation = self.perception.perceive(text)
        
        # Inject perturbation (fast timescale)
        self.field.evolve(steps=10, perturbation=perturbation, tau=self.tau_perception)
        
        return self.field.state
    
    def think(self, steps: int = 50) -> np.ndarray:
        """
        Free evolution (no external input).
        
        Understanding emerges from self-organization.
        """
        for _ in range(steps):
            # Free evolution
            self.field.evolve(steps=1, tau=self.tau_cognition)
            
            # Memory pull (weak)
            if self.memory.attractors:
                force = self.memory.recall_force(self.field.state) * 0.01
                self.field.state += force
        
        return self.field.state
    
    def learn(self, label: str = ""):
        """Consolidate current state into memory."""
        self.memory.store(self.field.state, strength=1.0)
    
    def recognize(self, text: str) -> Tuple[float, str]:
        """Check if input matches memories."""
        initial = self.field.state.copy()
        
        self.see(text)
        self.think(steps=30)
        
        energy = self.memory.energy(self.field.state)
        
        # Restore
        self.field.state = initial
        
        status = "familiar" if energy < 100 else "novel"
        return energy, status
    
    def complete(self, partial: str, steps: int = 100) -> dict:
        """Pattern completion via attractor dynamics."""
        self.see(partial)
        final = self.think(steps)
        
        return {
            'energy': float(self.memory.energy(final)),
            'activation': float(np.sum(final ** 2)),
            'stability': float(np.std(np.gradient(final)))
        }


def demo():
    """
    Demo: Baby learning through experience.
    
    Shows:
    1. Learning (forming attractors)
    2. Recognition (familiar vs novel)
    3. Pattern completion
    4. Memory association
    """
    print("="*60)
    print("🧠 Neural Field System - Minimal Viable Version")
    print("="*60)
    
    # Create system with dual-mode perception
    print("\n👁️ Perception Mode: spaCy (development)")
    brain = NeuralFieldSystem(size=64, perception_mode="spacy")
    
    # ===== Phase 1: Learning =====
    print("\n📚 Phase 1: Learning (Forming attractors)")
    
    experiences = [
        "The cat sits on the mat",
        "A dog runs in the park",
        "Birds fly in the sky"
    ]
    
    for i, text in enumerate(experiences):
        brain.see(text)
        brain.think(steps=50)
        brain.learn()
        print(f"   ✓ '{text[:30]}...'")
    
    # ===== Phase 2: Recognition =====
    print("\n👁️ Phase 2: Recognition")
    
    tests = [
        ("The cat sits on the mat", "Exact repeat"),
        ("A cat sits on a mat", "Similar pattern"),
        ("Quantum physics is weird", "Novel input")
    ]
    
    for text, desc in tests:
        energy, status = brain.recognize(text)
        print(f"   {desc}: {status} (E={energy:.1f})")
    
    # ===== Phase 3: Pattern Completion =====
    print("\n🧩 Phase 3: Pattern Completion")
    
    result = brain.complete("The cat", steps=100)
    print(f"   Input: 'The cat'")
    print(f"   → E={result['energy']:.1f}, Act={result['activation']:.1f}")
    
    # ===== Phase 4: Classical Conditioning =====
    print("\n🔗 Phase 4: Classical Conditioning (Pavlov)")
    
    # Learn: bell → food
    brain.see("bell rings")
    brain.think(30)
    brain.learn()
    
    brain.see("food arrives")
    brain.think(30)
    brain.learn()
    
    # Test association
    E_before = brain.memory.energy(brain.field.state)
    brain.see("bell")
    brain.think(50)
    E_after = brain.memory.energy(brain.field.state)
    
    print(f"   'bell rings' → 'food arrives'")
    print(f"   Energy: {E_before:.1f} → {E_after:.1f}")
    print(f"   ΔE = {E_before - E_after:+.1f} (negative = attraction)")
    
    # ===== Summary =====
    print("\n" + "="*60)
    print("✅ System characteristics:")
    print("   • spaCy = sensory cortex (NOT external tool)")
    print("   • Language = perturbation (NOT input format)")
    print("   • Memory = energy landscape (NOT vector storage)")
    print("   • Understanding = attractor convergence (NOT decoding)")
    # Demo lightweight mode
    print("\n\n🟢 Testing Lightweight Mode:")
    brain_light = NeuralFieldSystem(size=64, perception_mode="lightweight")
    brain_light.see("The cat sits")
    brain_light.think(30)
    print(f"   ✓ Lightweight perception working")
    
    print("\n⚠️ This system NEVER:")
    print("   1. ❌ Token → symbol → logic")
    print("   2. ❌ Explicit 'answer' module")
    print("   3. ❌ Attention / softmax")
    print("   4. ❌ Embedding lookup")
    print("   5. ❌ General conversation")
    print("="*60)


if __name__ == "__main__":
    demo()
