#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Selective Memory Mechanism for Neural Fields
选择性记忆机制

Features:
- Importance gating (selective storage)
- Active forgetting (reverse Hebbian learning)
- Temporal decay
- Usage reinforcement
"""

import jax.numpy as jnp
import time
from typing import Dict, Tuple
from neural_field_2d import NeuralField2D


class SelectiveMemoryField(NeuralField2D):
    """
    Neural Field with selective memory capabilities
    
    Key innovations:
    1. Importance Gating - filter unimportant information
    2. Active Forgetting - suppress unwanted memories
    3. Temporal Decay - memories fade over time
    4. Usage Reinforcement - frequently used memories strengthen
    """
    
    def __init__(self, shape=(100, 100), **kwargs):
        super().__init__(shape, **kwargs)
        
        # Memory metadata
        self.memory_metadata = {}
        
        # Forgetting parameters
        self.decay_rate = 0.001
        self.importance_threshold = 0.5
        self.interference_factor = 0.1
    
    def store_memory(self, name: str, pattern: jnp.ndarray, 
                     importance: float = 1.0,
                     emotional_weight: float = 1.0) -> bool:
        """
        Store memory with importance gating
        
        Args:
            name: Memory name
            pattern: Memory pattern (field activation)
            importance: Importance score (0-1)
            emotional_weight: Emotional weight (>1 enhance, <1 reduce)
        
        Returns:
            True if successfully stored
        """
        # Step 1: Importance gating (SELECTIVE MEMORY)
        if importance < self.importance_threshold:
            print(f"⚠️  Memory '{name}' filtered (importance={importance:.2f})")
            return False
        
        print(f"✅ Storing memory: '{name}' (importance={importance:.2f})")
        
        # Step 2: Emotional modulation
        effective_importance = importance * emotional_weight
        
        # Step 3: Hebbian learning (shape kernel)
        learning_rate = 0.01 * effective_importance
        pattern_flat = pattern.flatten()
        self.kernel = self.kernel + learning_rate * jnp.outer(pattern_flat, pattern_flat)
        
        # Step 4: Record metadata
        self.memory_metadata[name] = {
            'importance': importance,
            'emotional_weight': emotional_weight,
            'timestamp': time.time(),
            'usage_count': 0,
            'last_accessed': time.time()
        }
        
        return True
    
    def recall_memory(self, name: str, cue: jnp.ndarray) -> Tuple[jnp.ndarray, float]:
        """
        Recall memory using pattern completion
        
        Args:
            name: Memory name
            cue: Partial cue
        
        Returns:
            (recalled pattern, similarity)
        """
        if name not in self.memory_metadata:
            return jnp.zeros(self.shape), 0.0
        
        # Field evolution recall
        self.set_state(cue)
        final_state = self.evolve(steps=50)
        
        # Calculate similarity
        target = self._get_memory_pattern(name)
        similarity = jnp.sum(final_state * target) / (
            jnp.sqrt(jnp.sum(final_state**2)) * jnp.sqrt(jnp.sum(target**2))
        )
        
        # Update metadata
        self.memory_metadata[name]['usage_count'] += 1
        self.memory_metadata[name]['last_accessed'] = time.time()
        
        return final_state, similarity
    
    def forget_memory(self, name: str, method: str = 'active'):
        """
        Actively forget a memory
        
        Args:
            name: Memory name
            method: 'active', 'passive', or 'interference'
        """
        if name not in self.memory_metadata:
            return
        
        pattern = self._get_memory_pattern(name)
        pattern_flat = pattern.flatten()
        
        if method == 'active':
            # Active suppression (reverse Hebbian)
            print(f"🗑️  Actively forgetting: '{name}'")
            unlearn_rate = 0.02
            self.kernel = self.kernel - unlearn_rate * jnp.outer(pattern_flat, pattern_flat)
        
        elif method == 'passive':
            # Passive decay
            print(f"⏳  Passive forgetting: '{name}'")
            decay = 0.1
            self.kernel = self.kernel * (1 - decay)
        
        del self.memory_metadata[name]
    
    def apply_temporal_decay(self):
        """Apply temporal decay to all memories"""
        current_time = time.time()
        memories_to_forget = []
        
        for name, meta in self.memory_metadata.items():
            hours_since_access = (current_time - meta['last_accessed']) / 3600
            decay_factor = jnp.exp(-self.decay_rate * hours_since_access * (1 / meta['importance']))
            
            meta['importance'] *= decay_factor
            
            if meta['importance'] < self.importance_threshold * 0.5:
                memories_to_forget.append(name)
        
        for name in memories_to_forget:
            self.forget_memory(name, method='passive')
    
    def _get_memory_pattern(self, name: str) -> jnp.ndarray:
        """Generate memory pattern from name (deterministic)"""
        hash_val = hash(name) % 1000
        x = jnp.arange(self.shape[0])[:, None]
        y = jnp.arange(self.shape[1])[None, :]
        
        center_x = hash_val % self.shape[0]
        center_y = (hash_val // 10) % self.shape[1]
        
        pattern = jnp.exp(-((x - center_x)**2 + **(y - center_y)2) / 100)
        return pattern
    
    def get_memory_stats(self) -> Dict:
        """Get memory statistics"""
        if not self.memory_metadata:
            return {'total': 0}
        
        importances = [m['importance'] for m in self.memory_metadata.values()]
        usage_counts = [m['usage_count'] for m in self.memory_metadata.values()]
        
        return {
            'total': len(self.memory_metadata),
            'avg_importance': float(jnp.mean(jnp.array(importances))),
            'max_importance': float(jnp.max(jnp.array(importances))),
            'min_importance': float(jnp.min(jnp.array(importances))),
            'avg_usage': float(jnp.mean(jnp.array(usage_counts))),
        }


def demo():
    """Demonstrate selective memory"""
    print("="*60)
    print("🧠 Selective Memory Demo")
    print("="*60)
    
    field = SelectiveMemoryField(shape=(100, 100))
    
    # Store memories with different importance
    print("\nStoring memories...")
    field.store_memory("important", jnp.zeros((100, 100)), 0.9, 1.5)
    field.store_memory("trivial", jnp.zeros((100, 100)), 0.3, 0.5)
    field.store_memory("emotional", jnp.zeros((100, 100)), 0.7, 2.0)
    
    # Show statistics
    stats = field.get_memory_stats()
    print(f"\n📊 Memory statistics:")
    print(f"  Total stored: {stats['total']}")
    print(f"  Avg importance: {stats['avg_importance']:.3f}")
    
    print("\n" + "="*60)
    print("✅ Demo completed!")
    print("="*60)


if __name__ == "__main__":
    demo()
