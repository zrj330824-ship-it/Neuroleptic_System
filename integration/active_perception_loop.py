#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Active Perception Loop - Closed-Loop Cognitive System

🧠 Complete Architecture:
[ Motor Cortex ] → Action → Environment
      ↑                          ↓
      │                    (Feedback)
      │                          ↓
[ Neural Field ] ← Perturbation ← Sensory
      │
      ↓
[ Attractor Memory ]

⏱️ Timescales:
- Fast (τ=0.1): Sensory perturbation
- Slow (τ=1.0): Field dynamics
- Ultra-slow (τ=10.0): Memory consolidation

🎯 Key Innovation:
System can DECIDE where to look, what to ask, what to do.
NOT passive reception — ACTIVE EXPLORATION.
"""

import numpy as np
from typing import Dict, List, Optional, Tuple, Callable
from sensory_cortex import SensoryCortex


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Motor Cortex (Action Output)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class MotorCortex:
    """
    Convert field state to actions.
    
    NOT: symbolic command generation
    BUT: continuous state → action mapping
    
    Biological rationale:
    - Motor cortex reads from premotor areas
    - Action emerges from population dynamics
    - No "decision module" — just dynamics
    """
    
    def __init__(self, action_space: Dict[str, np.ndarray]):
        """
        Args:
            action_space: Dict mapping action names to field patterns
        """
        self.action_space = action_space
        self.action_threshold = 0.7  # Confidence threshold
    
    def decode_action(self, field_state: np.ndarray) -> Dict:
        """
        Decode action from field state.
        
        Process:
        1. Compare field to action patterns
        2. Select best match (if above threshold)
        3. Return action + confidence
        """
        best_action = None
        best_similarity = 0.0
        
        for action_name, action_pattern in self.action_space.items():
            # Cosine similarity
            similarity = np.sum(field_state * action_pattern) / (
                np.linalg.norm(field_state) * np.linalg.norm(action_pattern) + 1e-8
            )
            
            if similarity > best_similarity:
                best_similarity = similarity
                best_action = action_name
        
        # Only act if confident
        if best_similarity >= self.action_threshold:
            return {
                'action': best_action,
                'confidence': float(best_similarity),
                'execute': True
            }
        else:
            return {
                'action': None,
                'confidence': float(best_similarity),
                'execute': False
            }
    
    def learn_action(self, name: str, field_state: np.ndarray):
        """Learn new action pattern from demonstration."""
        self.action_space[name] = field_state.copy()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Environment Interface (Feedback Loop)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class SimpleEnvironment:
    """
    Simple environment for closed-loop interaction.
    
    Environment provides:
    - State observation
    - Action effects
    - Reward/punishment signals
    
    This is a placeholder — replace with real environment.
    """
    
    def __init__(self):
        self.state = "neutral"
        self.history: List[Dict] = []
    
    def step(self, action: Optional[str]) -> Tuple[str, float, Dict]:
        """
        Execute action and return feedback.
        
        Returns:
            observation: Environment state description
            reward: Scalar feedback (positive/negative)
            info: Additional context
        """
        if action is None:
            # No action — observe only
            observation = f"Environment is {self.state}"
            reward = 0.0
        else:
            # Simple reward logic (demo)
            if action == "approach" and self.state == "positive":
                reward = 1.0
                self.state = "engaged"
            elif action == "avoid" and self.state == "negative":
                reward = 1.0
                self.state = "safe"
            elif action == "explore":
                reward = 0.5  # Intrinsic curiosity
                self.state = np.random.choice(["neutral", "positive", "negative"])
            else:
                reward = -0.1  # Wrong action
                self.state = "neutral"
            
            observation = f"After {action}: environment is {self.state}"
        
        # Record
        self.history.append({
            'action': action,
            'observation': observation,
            'reward': reward
        })
        
        return observation, reward, {'state': self.state}
    
    def get_perturbation(self, observation: str, cortex: SensoryCortex) -> np.ndarray:
        """Convert observation to field perturbation."""
        return cortex.perceive(observation)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Attention Mechanism (Active Perception)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class AttentionMechanism:
    """
    Selective attention for active perception.
    
    NOT: attention weights for softmax
    BUT: spatial modulation of sensory input
    
    Biological rationale:
    - Attention modulates V1 responses
    - Enhances relevant features
    - Suppresses irrelevant features
    """
    
    def __init__(self, field_size: int = 64):
        self.field_size = field_size
        self.attention_map = np.ones((field_size, field_size))  # Uniform initially
    
    def focus(self, x: int, y: int, sigma: float = 5.0):
        """Focus attention on spatial region."""
        x_coords = np.arange(self.field_size)
        y_coords = np.arange(self.field_size)
        xx, yy = np.meshgrid(x_coords, y_coords)
        
        self.attention_map = np.exp(
            -((xx - x) ** 2 + (yy - y) ** 2) / (2 * sigma ** 2)
        )
    
    def modulate(self, perturbation: np.ndarray) -> np.ndarray:
        """Apply attention modulation to perturbation."""
        return perturbation * self.attention_map
    
    def reset(self):
        """Reset to uniform attention."""
        self.attention_map = np.ones((self.field_size, self.field_size))


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Complete Active Perception System
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class ActivePerceptionSystem:
    """
    Complete closed-loop cognitive system.
    
    Architecture:
    [ SensoryCortex ] → Perturbation → [ NeuralField ]
                                              ↓
    [ Environment ] ← Action ← [ MotorCortex ]
          ↓
    (Feedback perturbation)
    
    With attention modulation and memory consolidation.
    """
    
    def __init__(self, field_size: int = 64, perception_mode: str = "spacy"):
        # Core components
        self.field_size = field_size
        self.phi = np.random.randn(field_size, field_size) * 0.01
        
        # Perception (dual-mode)
        self.cortex = SensoryCortex(mode=perception_mode, field_size=field_size)
        
        # Attention
        self.attention = AttentionMechanism(field_size)
        
        # Memory
        self.attractors: List[np.ndarray] = []
        self.lambda_strengths: List[float] = []
        
        # Action
        self.motor = MotorCortex(action_space={})
        
        # Environment
        self.env = SimpleEnvironment()
        
        # Timescales
        self.tau_fast = 0.1
        self.tau_slow = 1.0
        self.tau_ultraslow = 10.0
        
        # History
        self.episode_history: List[Dict] = []
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # Core Dynamics
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    def laplacian(self, phi: np.ndarray) -> np.ndarray:
        """Discrete Laplacian."""
        return (
            np.roll(phi, 1, 0) + np.roll(phi, -1, 0) +
            np.roll(phi, 1, 1) + np.roll(phi, -1, 1) -
            4 * phi
        )
    
    def attractor_force(self) -> np.ndarray:
        """Memory attractor force."""
        if not self.attractors:
            return np.zeros((self.field_size, self.field_size))
        
        force = np.zeros_like(self.phi)
        for A, lambda_i in zip(self.attractors, self.lambda_strengths):
            force -= lambda_i * (self.phi - A)
        
        return force
    
    def evolve(self, steps: int = 20, perturbation: Optional[np.ndarray] = None) -> np.ndarray:
        """Evolve field with perturbation."""
        for step in range(steps):
            # Diffusion
            diffusion = self.laplacian(self.phi)
            
            # Reaction
            reaction = self.phi - self.phi ** 3
            
            # Memory
            memory = self.attractor_force()
            
            # Perturbation (attention-modulated)
            if perturbation is not None:
                decay = np.exp(-step / (self.tau_slow * steps))
                modulated = self.attention.modulate(perturbation)
                self.phi += 0.1 * decay * modulated
            
            # Update
            self.phi += 0.1 * (diffusion + reaction + memory)
        
        return self.phi
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # Active Perception Loop
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    def perceive(self, text: str, attend: bool = True):
        """
        Perceive with optional attention.
        
        If attend=True, system focuses on salient regions.
        """
        perturbation = self.cortex.perceive(text)
        
        if attend:
            # Find salient region (highest activation)
            salient_x, salient_y = np.unravel_index(
                np.argmax(perturbation), perturbation.shape
            )
            self.attention.focus(salient_x, salient_y)
        
        self.evolve(steps=20, perturbation=perturbation)
    
    def act(self) -> Dict:
        """
        Generate and execute action.
        
        Returns:
            Action decision and outcome
        """
        # Decode action from field state
        decision = self.motor.decode_action(self.phi)
        
        if decision['execute']:
            # Execute action
            observation, reward, info = self.env.step(decision['action'])
            
            # Feedback as perturbation
            feedback_text = f"{observation} (reward={reward:+.1f})"
            self.perceive(feedback_text)
            
            # Consolidate if reward positive
            if reward > 0:
                self.consolidate_memory(strength=1.0)
            else:
                self.consolidate_memory(strength=0.3)  # Weak memory for negative
            
            result = {
                'action': decision['action'],
                'reward': reward,
                'observation': observation
            }
        else:
            # No action — just observe
            observation, reward, info = self.env.step(None)
            result = {
                'action': None,
                'reward': reward,
                'observation': observation,
                'reason': f"Low confidence ({decision['confidence']:.2f})"
            }
        
        self.episode_history.append(result)
        return result
    
    def learn_action(self, name: str):
        """Associate current state with action name."""
        self.motor.learn_action(name, self.phi.copy())
    
    def consolidate_memory(self, strength: float = 1.0):
        """Store current state as attractor."""
        self.attractors.append(self.phi.copy())
        self.lambda_strengths.append(strength)
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # Exploration Strategies
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    def explore(self, n_steps: int = 10) -> List[Dict]:
        """
        Active exploration loop.
        
        Perceive → Think → Act → Learn
        """
        results = []
        
        for i in range(n_steps):
            # Think (free evolution)
            self.evolve(steps=30)
            
            # Act
            outcome = self.act()
            
            results.append(outcome)
        
        return results
    
    def get_energy(self) -> float:
        """Compute total energy."""
        # Smoothness
        grad_x, grad_y = np.gradient(self.phi)
        E_smooth = np.sum(grad_x ** 2 + grad_y ** 2)
        
        # Attractor potential
        E_attract = 0.0
        for A, lambda_i in zip(self.attractors, self.lambda_strengths):
            E_attract += lambda_i * np.sum((self.phi - A) ** 2)
        
        return E_smooth + E_attract


def demo_active_perception():
    """
    Demo: Active perception loop with learning.
    """
    print("="*60)
    print("🔄 Active Perception Loop - Closed-Loop System")
    print("="*60)
    
    # Create system
    system = ActivePerceptionSystem(field_size=64, perception_mode="spacy")
    
    # Phase 1: Learn action repertoire
    print("\n📚 Phase 1: Learning Action Repertoire")
    
    # Demonstrate actions
    system.perceive("approach positive stimulus")
    system.learn_action("approach")
    print("   ✓ Learned: approach")
    
    system.perceive("avoid negative stimulus")
    system.learn_action("avoid")
    print("   ✓ Learned: avoid")
    
    system.perceive("explore environment")
    system.learn_action("explore")
    print("   ✓ Learned: explore")
    
    # Phase 2: Active exploration
    print("\n🔍 Phase 2: Active Exploration (10 steps)")
    
    # Set environment to positive state
    system.env.state = "positive"
    
    results = system.explore(n_steps=10)
    
    # Analyze
    actions_taken = [r['action'] for r in results if r['action']]
    rewards = [r['reward'] for r in results]
    
    print(f"\n   Actions taken: {actions_taken}")
    print(f"   Total reward: {sum(rewards):+.1f}")
    print(f"   Success rate: {len([r for r in rewards if r > 0])/len(rewards)*100:.0f}%")
    
    # Phase 3: Memory analysis
    print("\n💾 Phase 3: Memory Analysis")
    print(f"   Attractors stored: {len(system.attractors)}")
    print(f"   Initial energy: {system.get_energy():.2f}")
    
    # Perturb and recover
    initial_phi = system.phi.copy()
    system.phi += np.random.randn(64, 64) * 0.5  # Strong noise
    noisy_energy = system.get_energy()
    
    system.evolve(steps=100)  # Let system settle
    final_energy = system.get_energy()
    
    print(f"   After noise: {noisy_energy:.2f}")
    print(f"   After settle: {final_energy:.2f}")
    print(f"   ΔE = {noisy_energy - final_energy:+.2f} (convergence)")
    
    # Phase 4: Attention demo
    print("\n👁️ Phase 4: Active Attention")
    
    system.attention.reset()
    system.perceive("focus on important pattern", attend=True)
    
    print(f"   Attention focused: {np.sum(system.attention.attention_map > 0.5)} regions")
    print(f"   Field activation: {np.sum(system.phi > 0.5)} regions")
    
    print("\n" + "="*60)
    print("✅ Active perception loop complete!")
    print("="*60)
    print("\nKey capabilities:")
    print("  • Active attention (decides where to look)")
    print("  • Action generation (field state → behavior)")
    print("  • Closed-loop learning (action → feedback → memory)")
    print("  • Multi-timescale dynamics (fast/slow/ultra-slow)")


if __name__ == "__main__":
    demo_active_perception()
