"""
Keystroke Capture Module

Handles real-time keystroke timing capture for biometric authentication.
Captures key press/release events and calculates timing metrics.
"""

import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class KeyEvent:
    """Represents a single key event with timing information."""
    key: str
    press_time: float
    release_time: Optional[float] = None
    
    @property
    def dwell_time(self) -> Optional[float]:
        """Time the key was held down (release - press)."""
        if self.release_time is not None:
            return self.release_time - self.press_time
        return None


@dataclass
class KeystrokeSession:
    """
    Captures and stores keystroke timing data for a typing session.
    
    Tracks:
    - Dwell time: How long each key is held
    - Flight time: Time between releasing one key and pressing the next
    - Digraph timing: Time for two-key sequences
    - Trigraph timing: Time for three-key sequences
    """
    
    events: list[KeyEvent] = field(default_factory=list)
    _pending_events: dict[str, KeyEvent] = field(default_factory=dict)
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    
    def on_key_down(self, key: str, timestamp: Optional[float] = None) -> None:
        """Record a key press event."""
        ts = timestamp or time.time()
        
        if self.start_time is None:
            self.start_time = ts
            
        # Normalize key name
        key = self._normalize_key(key)
        
        # Only track if not already pressed (avoid key repeat)
        if key not in self._pending_events:
            self._pending_events[key] = KeyEvent(key=key, press_time=ts)
    
    def on_key_up(self, key: str, timestamp: Optional[float] = None) -> None:
        """Record a key release event."""
        ts = timestamp or time.time()
        self.end_time = ts
        
        key = self._normalize_key(key)
        
        if key in self._pending_events:
            event = self._pending_events.pop(key)
            event.release_time = ts
            self.events.append(event)
    
    def _normalize_key(self, key: str) -> str:
        """Normalize key names for consistency."""
        key = key.lower()
        
        # Handle special keys
        if key in (' ', 'space', ' '):
            return 'space'
        if len(key) == 1 and key.isalpha():
            return key
        
        return key
    
    def get_completed_events(self) -> list[KeyEvent]:
        """Get all events where key was pressed and released."""
        return [e for e in self.events if e.release_time is not None]
    
    def get_typing_duration(self) -> Optional[float]:
        """Total time from first keypress to last key release."""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return None
    
    def get_characters_typed(self) -> int:
        """Number of characters typed in this session."""
        return len(self.get_completed_events())
    
    def get_typing_speed(self) -> Optional[float]:
        """Average time per character (seconds/char)."""
        duration = self.get_typing_duration()
        chars = self.get_characters_typed()
        if duration and chars > 0:
            return duration / chars
        return None
    
    def clear(self) -> None:
        """Reset the session for new input."""
        self.events.clear()
        self._pending_events.clear()
        self.start_time = None
        self.end_time = None


def parse_js_keystroke_data(js_data: list[dict]) -> KeystrokeSession:
    """
    Parse keystroke data from JavaScript frontend.
    
    Expected format:
    [
        {"key": "h", "type": "keydown", "time": 1234567890.123},
        {"key": "h", "type": "keyup", "time": 1234567890.223},
        ...
    ]
    """
    session = KeystrokeSession()
    
    for event in js_data:
        key = event.get('key', '')
        event_type = event.get('type', '')
        timestamp = event.get('time', 0) / 1000  # Convert ms to seconds
        
        if event_type == 'keydown':
            session.on_key_down(key, timestamp)
        elif event_type == 'keyup':
            session.on_key_up(key, timestamp)
    
    return session


# Constants for tracked keys
TRACKED_LETTERS = ['e', 'a', 'r', 'i', 'o', 't', 'n', 's', 'h', 'l', 'd', 'g']
TRACKED_DIGRAPHS = ['in', 'th', 'ti', 'on', 'an', 'he', 'al', 'er', 'es']
TRACKED_TRIGRAPHS = ['the', 'and', 'are', 'ion', 'ing']

