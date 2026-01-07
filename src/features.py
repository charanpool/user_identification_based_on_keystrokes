"""
Feature Extraction Module

Extracts keystroke dynamics features from typing sessions for ML classification.
Features include dwell times, flight times, digraph/trigraph latencies.
"""

import numpy as np
from dataclasses import dataclass
from typing import Optional

from .capture import (
    KeystrokeSession, 
    KeyEvent,
    TRACKED_LETTERS, 
    TRACKED_DIGRAPHS, 
    TRACKED_TRIGRAPHS
)


@dataclass
class KeystrokeFeatures:
    """
    Extracted features from a typing session.
    
    Feature types:
    - Dwell times: How long each key is held (key-specific)
    - Digraph latencies: Time for common two-letter sequences
    - Trigraph latencies: Time for common three-letter sequences  
    - Typing speed: Overall characters per second
    """
    
    dwell_times: dict[str, float]
    digraph_latencies: dict[str, float]
    trigraph_latencies: dict[str, float]
    typing_speed: float
    
    def to_vector(self) -> np.ndarray:
        """
        Convert features to a fixed-length numpy array for ML models.
        
        Order: dwell_times (13) + digraph_latencies (9) + trigraph_latencies (5) + typing_speed (1) = 28
        """
        vector = []
        
        # Dwell times for tracked letters + space
        for letter in TRACKED_LETTERS + ['space']:
            vector.append(self.dwell_times.get(letter, 0.0))
        
        # Digraph latencies
        for digraph in TRACKED_DIGRAPHS:
            vector.append(self.digraph_latencies.get(digraph, 0.0))
        
        # Trigraph latencies
        for trigraph in TRACKED_TRIGRAPHS:
            vector.append(self.trigraph_latencies.get(trigraph, 0.0))
        
        # Typing speed
        vector.append(self.typing_speed)
        
        return np.array(vector, dtype=np.float32)
    
    @classmethod
    def from_vector(cls, vector: np.ndarray) -> 'KeystrokeFeatures':
        """Reconstruct features from a vector."""
        idx = 0
        
        dwell_times = {}
        for letter in TRACKED_LETTERS + ['space']:
            dwell_times[letter] = float(vector[idx])
            idx += 1
        
        digraph_latencies = {}
        for digraph in TRACKED_DIGRAPHS:
            digraph_latencies[digraph] = float(vector[idx])
            idx += 1
        
        trigraph_latencies = {}
        for trigraph in TRACKED_TRIGRAPHS:
            trigraph_latencies[trigraph] = float(vector[idx])
            idx += 1
        
        typing_speed = float(vector[idx])
        
        return cls(
            dwell_times=dwell_times,
            digraph_latencies=digraph_latencies,
            trigraph_latencies=trigraph_latencies,
            typing_speed=typing_speed
        )
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'dwell_times': self.dwell_times,
            'digraph_latencies': self.digraph_latencies,
            'trigraph_latencies': self.trigraph_latencies,
            'typing_speed': self.typing_speed
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'KeystrokeFeatures':
        """Create from dictionary."""
        return cls(
            dwell_times=data.get('dwell_times', {}),
            digraph_latencies=data.get('digraph_latencies', {}),
            trigraph_latencies=data.get('trigraph_latencies', {}),
            typing_speed=data.get('typing_speed', 0.0)
        )


def get_feature_names() -> list[str]:
    """Get ordered list of feature names matching vector order."""
    names = []
    
    for letter in TRACKED_LETTERS + ['space']:
        names.append(f'dwell_{letter}')
    
    for digraph in TRACKED_DIGRAPHS:
        names.append(f'digraph_{digraph}')
    
    for trigraph in TRACKED_TRIGRAPHS:
        names.append(f'trigraph_{trigraph}')
    
    names.append('typing_speed')
    
    return names


def extract_features(session: KeystrokeSession) -> Optional[KeystrokeFeatures]:
    """
    Extract keystroke dynamics features from a typing session.
    
    Args:
        session: Completed keystroke capture session
        
    Returns:
        KeystrokeFeatures object or None if insufficient data
    """
    events = session.get_completed_events()
    
    if len(events) < 10:  # Need minimum data
        return None
    
    # Calculate dwell times (average per key)
    dwell_times = _calculate_dwell_times(events)
    
    # Calculate digraph latencies
    digraph_latencies = _calculate_digraph_latencies(events)
    
    # Calculate trigraph latencies
    trigraph_latencies = _calculate_trigraph_latencies(events)
    
    # Typing speed
    typing_speed = session.get_typing_speed() or 0.0
    
    return KeystrokeFeatures(
        dwell_times=dwell_times,
        digraph_latencies=digraph_latencies,
        trigraph_latencies=trigraph_latencies,
        typing_speed=typing_speed
    )


def _calculate_dwell_times(events: list[KeyEvent]) -> dict[str, float]:
    """Calculate average dwell time for each key."""
    key_dwells: dict[str, list[float]] = {}
    
    for event in events:
        if event.dwell_time is not None:
            key = event.key
            if key not in key_dwells:
                key_dwells[key] = []
            key_dwells[key].append(event.dwell_time)
    
    # Calculate averages
    return {
        key: np.mean(dwells) 
        for key, dwells in key_dwells.items()
        if len(dwells) > 0
    }


def _calculate_digraph_latencies(events: list[KeyEvent]) -> dict[str, float]:
    """
    Calculate digraph (two-key sequence) latencies.
    
    Latency = time from pressing first key to releasing second key.
    """
    digraph_times: dict[str, list[float]] = {}
    
    for i in range(len(events) - 1):
        first, second = events[i], events[i + 1]
        
        if first.key and second.key and second.release_time:
            digraph = first.key + second.key
            
            if digraph in TRACKED_DIGRAPHS:
                latency = second.release_time - first.press_time
                
                if digraph not in digraph_times:
                    digraph_times[digraph] = []
                digraph_times[digraph].append(latency)
    
    return {
        digraph: np.mean(times)
        for digraph, times in digraph_times.items()
        if len(times) > 0
    }


def _calculate_trigraph_latencies(events: list[KeyEvent]) -> dict[str, float]:
    """
    Calculate trigraph (three-key sequence) latencies.
    
    Latency = time from pressing first key to releasing third key.
    """
    trigraph_times: dict[str, list[float]] = {}
    
    for i in range(len(events) - 2):
        first, second, third = events[i], events[i + 1], events[i + 2]
        
        if first.key and second.key and third.key and third.release_time:
            trigraph = first.key + second.key + third.key
            
            if trigraph in TRACKED_TRIGRAPHS:
                latency = third.release_time - first.press_time
                
                if trigraph not in trigraph_times:
                    trigraph_times[trigraph] = []
                trigraph_times[trigraph].append(latency)
    
    return {
        trigraph: np.mean(times)
        for trigraph, times in trigraph_times.items()
        if len(times) > 0
    }


def aggregate_features(feature_list: list[KeystrokeFeatures]) -> KeystrokeFeatures:
    """
    Aggregate multiple feature samples into a single averaged profile.
    
    Args:
        feature_list: List of feature samples from multiple typing sessions
        
    Returns:
        Averaged KeystrokeFeatures
    """
    if not feature_list:
        raise ValueError("Cannot aggregate empty feature list")
    
    if len(feature_list) == 1:
        return feature_list[0]
    
    # Stack all vectors
    vectors = np.stack([f.to_vector() for f in feature_list])
    
    # Calculate mean (ignoring zeros as missing values)
    masked = np.ma.masked_equal(vectors, 0)
    mean_vector = np.ma.filled(masked.mean(axis=0), 0)
    
    return KeystrokeFeatures.from_vector(mean_vector)

