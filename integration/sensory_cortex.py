#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sensory Cortex - Dual-Mode Perception

🎯 Dual-Mode Architecture:
- Mode A: spaCy backend (mature NLP, rapid prototyping)
- Mode B: Lightweight backend (efficient, deployable)

✅ Unified interface - backends are swappable
✅ Performance comparison enabled
✅ Biological plausibility: perception as continuous encoding

Usage:
    # Development (spaCy)
    cortex = SensoryCortex(mode="spacy")
    
    # Deployment (lightweight)
    cortex = SensoryCortex(mode="lightweight")
    
    # Same interface
    perturbation = cortex.perceive("The cat sits")
"""

import numpy as np
import re
from typing import List, Dict, Optional, Tuple
import hashlib


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Mode A: spaCy Backend (Mature NLP)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class SpacyBackend:
    """
    spaCy-based perception backend.
    
    Advantages:
    - Mature tokenization
    - POS tagging
    - Dependency parsing
    - Lemma normalization
    
    Disadvantages:
    - ~50MB model size
    - ~0.5s load time
    - ~100MB runtime memory
    """
    
    def __init__(self, model: str = "en_core_web_sm"):
        try:
            import spacy
            self.nlp = spacy.load(model)
            self.available = True
        except Exception as e:
            print(f"⚠️ spaCy not available: {e}")
            self.nlp = None
            self.available = False
    
    def tokenize(self, text: str) -> List[Dict]:
        """
        Tokenize with linguistic features.
        
        Returns:
            List of token dicts with lemma, pos, dep
        """
        if not self.available:
            return []
        
        doc = self.nlp(text)
        
        tokens = []
        for token in doc:
            tokens.append({
                'text': token.text,
                'lemma': token.lemma_.lower(),
                'pos': token.pos_,
                'dep': token.dep_,
                'is_stop': token.is_stop
            })
        
        return tokens


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Mode B: Lightweight Backend (Efficient)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class LightweightBackend:
    """
    Lightweight perception backend.
    
    Advantages:
    - ~1KB code size
    - ~0.01s load time
    - ~5MB runtime memory
    - No external dependencies
    
    Disadvantages:
    - Basic tokenization only
    - Rule-based POS (approximate)
    - No dependency parsing
    
    Biological rationale:
    - Early sensory cortex does simple feature detection
    - Complex processing happens in association cortex
    - This is V1, not IT cortex
    """
    
    # Simple POS patterns (approximate)
    POS_PATTERNS = {
        # Function words
        'the': 'DET', 'a': 'DET', 'an': 'DET', 'this': 'DET', 'that': 'DET',
        'these': 'DET', 'those': 'DET', 'my': 'PRON', 'your': 'PRON',
        'he': 'PRON', 'she': 'PRON', 'it': 'PRON', 'they': 'PRON',
        'is': 'VERB', 'are': 'VERB', 'was': 'VERB', 'were': 'VERB',
        'has': 'VERB', 'have': 'VERB', 'had': 'VERB', 'do': 'VERB',
        'does': 'VERB', 'did': 'VERB', 'will': 'VERB', 'would': 'VERB',
        'can': 'VERB', 'could': 'VERB', 'may': 'VERB', 'might': 'VERB',
        # Prepositions
        'on': 'ADP', 'in': 'ADP', 'at': 'ADP', 'to': 'ADP', 'for': 'ADP',
        'with': 'ADP', 'by': 'ADP', 'from': 'ADP', 'of': 'ADP',
        # Conjunctions
        'and': 'CONJ', 'or': 'CONJ', 'but': 'CONJ', 'if': 'CONJ',
        # Common nouns (very basic)
        'cat': 'NOUN', 'dog': 'NOUN', 'bird': 'NOUN', 'mat': 'NOUN',
        'park': 'NOUN', 'sky': 'NOUN', 'bell': 'NOUN', 'food': 'NOUN',
        # Common verbs
        'sit': 'VERB', 'run': 'VERB', 'fly': 'VERB', 'ring': 'VERB',
        'arrive': 'VERB', 'see': 'VERB', 'move': 'VERB',
        # Common adjectives
        'big': 'ADJ', 'small': 'ADJ', 'fast': 'ADJ', 'slow': 'ADJ',
        'good': 'ADJ', 'bad': 'ADJ', 'new': 'ADJ', 'old': 'ADJ',
    }
    
    def __init__(self):
        self.pos_patterns = self.POS_PATTERNS
        self.available = True
    
    def tokenize(self, text: str) -> List[Dict]:
        """
        Simple tokenization with rule-based POS.
        
        Process:
        1. Lowercase + split on whitespace/punctuation
        2. Rule-based POS tagging
        3. Return simplified token features
        """
        # Simple tokenization (split on whitespace + punctuation)
        tokens_raw = re.findall(r'\b\w+\b', text.lower())
        
        tokens = []
        for word in tokens_raw:
            # Rule-based POS
            pos = self._guess_pos(word)
            
            tokens.append({
                'text': word,
                'lemma': word,  # No lemmatization (use word as-is)
                'pos': pos,
                'dep': 'unknown',  # No dependency parsing
                'is_stop': word in ['the', 'a', 'an', 'is', 'are', 'was', 'were']
            })
        
        return tokens
    
    def _guess_pos(self, word: str) -> str:
        """Guess POS from word patterns."""
        # Check dictionary first
        if word in self.pos_patterns:
            return self.pos_patterns[word]
        
        # Suffix-based rules
        if word.endswith('ing'):
            return 'VERB'  # Running, sitting
        elif word.endswith('ly'):
            return 'ADV'   # Quickly, slowly
        elif word.endswith('tion') or word.endswith('ness'):
            return 'NOUN'  # Action, happiness
        elif word.endswith('ed'):
            return 'VERB'  # Walked, talked
        elif word.endswith('s') and len(word) > 3:
            return 'NOUN'  # Cats, dogs (plural)
        elif word.endswith('y'):
            return 'ADJ'   # Happy, sunny
        else:
            return 'NOUN'  # Default


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Unified Sensory Cortex Interface
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class SensoryCortex:
    """
    Unified sensory perception interface.
    
    Architecture:
    [ SensoryCortex ]
    ├── backend: spaCy OR lightweight (swappable)
    ├── encoder: Token → perturbation pattern
    └── output: Continuous field perturbation
    
    Biological rationale:
    - Perception is NOT symbolic translation
    - Perception IS continuous pattern injection
    - Different backends = different "sensory acuity"
    """
    
    def __init__(self, mode: str = "spacy", field_size: int = 64):
        """
        Args:
            mode: "spacy" or "lightweight"
            field_size: Target perturbation size
        """
        self.mode = mode
        self.field_size = field_size
        
        # Initialize backend
        if mode == "spacy":
            self.backend = SpacyBackend()
            if not self.backend.available:
                print("⚠️ spaCy not available, falling back to lightweight")
                self.mode = "lightweight"
                self.backend = LightweightBackend()
        else:
            self.backend = LightweightBackend()
        
        # Encoding parameters
        self.encoding_dim = 3  # lemma, pos, dep
    
    def perceive(self, text: str) -> np.ndarray:
        """
        Convert text to field perturbation.
        
        Process:
        1. Tokenize (backend-specific)
        2. Encode tokens → continuous pattern
        3. Return perturbation array
        
        This is NOT symbolic processing.
        This IS sensory transduction (like retina → V1).
        """
        # Step 1: Tokenize
        tokens = self.backend.tokenize(text)
        
        # Step 2: Encode to perturbation
        perturbation = self._encode_tokens(tokens)
        
        return perturbation
    
    def _encode_tokens(self, tokens: List[Dict]) -> np.ndarray:
        """
        Encode tokens as continuous perturbation pattern.
        
        Encoding strategy:
        - lemma → spatial position (hash-based)
        - pos → activation strength
        - dep → spatial distribution
        
        This creates a 2D activation pattern, not a symbol list.
        """
        perturbation = np.zeros((self.field_size, self.field_size))
        
        for token in tokens:
            # Skip stop words (low salience)
            if token.get('is_stop', False):
                continue
            
            # Spatial position from lemma hash
            lemma_hash = hashlib.md5(token['lemma'].encode()).hexdigest()
            x = int(lemma_hash[:4], 16) % self.field_size
            y = int(lemma_hash[4:8], 16) % self.field_size
            
            # Activation strength from POS
            pos_strength = self._pos_to_strength(token['pos'])
            
            # Dependency affects spread
            dep_spread = self._dep_to_spread(token.get('dep', 'unknown'))
            
            # Add Gaussian blob (not point activation)
            perturbation += self._gaussian_blob(x, y, pos_strength, dep_spread)
        
        # Normalize
        max_val = np.max(perturbation)
        if max_val > 0:
            perturbation /= max_val
        
        return perturbation
    
    def _pos_to_strength(self, pos: str) -> float:
        """Map POS to activation strength."""
        strength_map = {
            'NOUN': 1.0,    # High salience
            'VERB': 0.9,    # High salience
            'ADJ': 0.7,     # Medium
            'ADV': 0.6,     # Medium
            'PRON': 0.4,    # Low
            'DET': 0.2,     # Very low
            'ADP': 0.3,     # Low
            'CONJ': 0.3,    # Low
            'NUM': 0.8,     # High
            'INTJ': 0.5,    # Medium
        }
        return strength_map.get(pos, 0.5)
    
    def _dep_to_spread(self, dep: str) -> float:
        """Map dependency to spatial spread (sigma)."""
        # Core arguments = focused, modifiers = spread
        spread_map = {
            'nsubj': 1.0,    # Focused
            'dobj': 1.0,     # Focused
            'prep': 2.0,     # Spread (relational)
            'amod': 1.5,     # Medium
            'advmod': 1.5,   # Medium
            'det': 0.5,      # Very focused
            'unknown': 1.5,  # Default
        }
        return spread_map.get(dep, 1.5)
    
    def _gaussian_blob(self, x: int, y: int, 
                       amplitude: float, sigma: float) -> np.ndarray:
        """Create 2D Gaussian activation blob."""
        x_coords = np.arange(self.field_size)
        y_coords = np.arange(self.field_size)
        xx, yy = np.meshgrid(x_coords, y_coords)
        
        gaussian = amplitude * np.exp(
            -((xx - x) ** 2 + (yy - y) ** 2) / (2 * sigma ** 2)
        )
        
        return gaussian
    
    def get_backend_info(self) -> Dict:
        """Get backend information for logging."""
        if isinstance(self.backend, SpacyBackend):
            return {
                'mode': 'spacy',
                'available': self.backend.available,
                'model': 'en_core_web_sm',
                'size_mb': '~50',
                'load_time_s': '~0.5'
            }
        else:
            return {
                'mode': 'lightweight',
                'available': True,
                'size_kb': '~1',
                'load_time_s': '~0.01'
            }


def demo_comparison():
    """
    Compare spaCy vs lightweight backends.
    """
    print("="*60)
    print("👁️ Sensory Cortex - Dual-Mode Perception Comparison")
    print("="*60)
    
    test_text = "The cat sits on the mat and watches the bird"
    
    # Mode A: spaCy
    print("\n🔵 Mode A: spaCy Backend")
    print("-" * 60)
    cortex_spacy = SensoryCortex(mode="spacy", field_size=64)
    info_spacy = cortex_spacy.get_backend_info()
    print(f"   Backend: {info_spacy}")
    
    import time
    start = time.time()
    perturb_spacy = cortex_spacy.perceive(test_text)
    time_spacy = time.time() - start
    
    print(f"   Perturbation shape: {perturb_spacy.shape}")
    print(f"   Activation sum: {np.sum(perturb_spacy):.3f}")
    print(f"   Processing time: {time_spacy*1000:.2f}ms")
    
    # Mode B: Lightweight
    print("\n🟢 Mode B: Lightweight Backend")
    print("-" * 60)
    cortex_light = SensoryCortex(mode="lightweight", field_size=64)
    info_light = cortex_light.get_backend_info()
    print(f"   Backend: {info_light}")
    
    start = time.time()
    perturb_light = cortex_light.perceive(test_text)
    time_light = time.time() - start
    
    print(f"   Perturbation shape: {perturb_light.shape}")
    print(f"   Activation sum: {np.sum(perturb_light):.3f}")
    print(f"   Processing time: {time_light*1000:.2f}ms")
    
    # Comparison
    print("\n📊 Comparison")
    print("-" * 60)
    speedup = time_spacy / time_light if time_light > 0 else float('inf')
    correlation = np.corrcoef(perturb_spacy.flatten(), perturb_light.flatten())[0, 1]
    
    print(f"   Speed improvement: {speedup:.1f}x faster")
    print(f"   Pattern correlation: r = {correlation:.3f}")
    print(f"   Memory saving: ~50MB → ~1KB")
    
    # Visualize difference
    print("\n🔬 Pattern Analysis")
    print("-" * 60)
    print(f"   spaCy peaks: {np.sum(perturb_spacy > 0.5)}")
    print(f"   Lightweight peaks: {np.sum(perturb_light > 0.5)}")
    print(f"   Overlap: {np.sum((perturb_spacy > 0.5) & (perturb_light > 0.5))}")
    
    print("\n" + "="*60)
    print("✅ Dual-mode perception ready!")
    print("="*60)
    print("\nUsage:")
    print("   # Development (rich features)")
    print("   cortex = SensoryCortex(mode='spacy')")
    print("   ")
    print("   # Deployment (efficient)")
    print("   cortex = SensoryCortex(mode='lightweight')")
    print("   ")
    print("   # Same interface, swappable backend!")


if __name__ == "__main__":
    demo_comparison()
