"""
ML Model Module

Machine learning classifier for user identification based on keystroke dynamics.
Uses Random Forest with confidence scoring for authentication decisions.
"""

import json
import os
from pathlib import Path
from typing import Optional
from dataclasses import dataclass

import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score

from .features import KeystrokeFeatures, get_feature_names


@dataclass
class PredictionResult:
    """Result of user identification prediction."""
    predicted_user: str
    confidence: float
    all_probabilities: dict[str, float]
    
    def is_confident(self, threshold: float = 0.5) -> bool:
        """Check if prediction meets confidence threshold."""
        return self.confidence >= threshold


class KeystrokeAuthenticator:
    """
    ML-based keystroke dynamics authenticator.
    
    Uses Random Forest classifier to identify users based on their
    typing patterns. Supports training, prediction, and persistence.
    """
    
    def __init__(self, model_path: Optional[Path] = None):
        self.classifier: Optional[RandomForestClassifier] = None
        self.scaler: Optional[StandardScaler] = None
        self.users: list[str] = []
        self.model_path = model_path or Path('models/keystroke_model.joblib')
        self._is_trained = False
    
    @property
    def is_trained(self) -> bool:
        """Check if model has been trained."""
        return self._is_trained and self.classifier is not None
    
    def train(
        self, 
        user_features: dict[str, list[KeystrokeFeatures]],
        n_estimators: int = 100
    ) -> dict:
        """
        Train the classifier on user keystroke data.
        
        Args:
            user_features: Dict mapping username to list of feature samples
            n_estimators: Number of trees in Random Forest
            
        Returns:
            Training metrics dict
        """
        if len(user_features) < 2:
            raise ValueError("Need at least 2 users to train classifier")
        
        # Prepare training data
        X, y = [], []
        self.users = sorted(user_features.keys())
        
        for user in self.users:
            samples = user_features[user]
            for features in samples:
                X.append(features.to_vector())
                y.append(user)
        
        X = np.array(X)
        y = np.array(y)
        
        # Scale features
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)
        
        # Train Random Forest
        self.classifier = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=10,
            min_samples_split=2,
            min_samples_leaf=1,
            random_state=42,
            class_weight='balanced'
        )
        self.classifier.fit(X_scaled, y)
        self._is_trained = True
        
        # Calculate metrics
        cv_scores = cross_val_score(
            self.classifier, X_scaled, y, cv=min(3, len(y))
        )
        
        return {
            'n_users': len(self.users),
            'n_samples': len(X),
            'cv_accuracy': float(np.mean(cv_scores)),
            'cv_std': float(np.std(cv_scores)),
            'feature_importance': self._get_feature_importance()
        }
    
    def predict(self, features: KeystrokeFeatures) -> PredictionResult:
        """
        Predict user identity from keystroke features.
        
        Args:
            features: Extracted keystroke features
            
        Returns:
            PredictionResult with user, confidence, and probabilities
        """
        if not self.is_trained:
            raise RuntimeError("Model not trained. Call train() first.")
        
        # Prepare features
        X = features.to_vector().reshape(1, -1)
        X_scaled = self.scaler.transform(X)
        
        # Predict
        predicted_user = self.classifier.predict(X_scaled)[0]
        probabilities = self.classifier.predict_proba(X_scaled)[0]
        
        # Build probability dict
        prob_dict = {
            user: float(prob) 
            for user, prob in zip(self.classifier.classes_, probabilities)
        }
        
        confidence = max(probabilities)
        
        return PredictionResult(
            predicted_user=predicted_user,
            confidence=confidence,
            all_probabilities=prob_dict
        )
    
    def _get_feature_importance(self) -> dict[str, float]:
        """Get feature importance scores from trained model."""
        if not self.is_trained:
            return {}
        
        importances = self.classifier.feature_importances_
        names = get_feature_names()
        
        return {
            name: float(imp) 
            for name, imp in zip(names, importances)
        }
    
    def save(self, path: Optional[Path] = None) -> None:
        """Save trained model to disk."""
        if not self.is_trained:
            raise RuntimeError("Cannot save untrained model")
        
        save_path = path or self.model_path
        save_path.parent.mkdir(parents=True, exist_ok=True)
        
        model_data = {
            'classifier': self.classifier,
            'scaler': self.scaler,
            'users': self.users
        }
        
        joblib.dump(model_data, save_path)
    
    def load(self, path: Optional[Path] = None) -> bool:
        """
        Load trained model from disk.
        
        Returns:
            True if loaded successfully, False otherwise
        """
        load_path = path or self.model_path
        
        if not load_path.exists():
            return False
        
        try:
            model_data = joblib.load(load_path)
            self.classifier = model_data['classifier']
            self.scaler = model_data['scaler']
            self.users = model_data['users']
            self._is_trained = True
            return True
        except Exception:
            return False


def load_users_from_json(json_path: Path) -> dict[str, list[KeystrokeFeatures]]:
    """
    Load user keystroke data from JSON file.
    
    Args:
        json_path: Path to users.json
        
    Returns:
        Dict mapping username to list of KeystrokeFeatures
    """
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    user_features = {}
    
    for username, user_data in data.get('users', {}).items():
        samples = []
        for sample in user_data.get('samples', []):
            features = KeystrokeFeatures.from_dict(sample.get('features', {}))
            samples.append(features)
        
        if samples:
            user_features[username] = samples
    
    return user_features


def save_user_to_json(
    json_path: Path, 
    username: str, 
    display_name: str,
    features_list: list[KeystrokeFeatures]
) -> None:
    """
    Save or update user keystroke data in JSON file.
    
    Args:
        json_path: Path to users.json
        username: User identifier
        display_name: User display name
        features_list: List of keystroke feature samples
    """
    # Load existing data
    if json_path.exists():
        with open(json_path, 'r') as f:
            data = json.load(f)
    else:
        data = {'users': {}, 'metadata': {'version': '2.0.0'}}
    
    # Add/update user
    data['users'][username] = {
        'display_name': display_name,
        'samples': [{'features': f.to_dict()} for f in features_list]
    }
    
    # Save
    json_path.parent.mkdir(parents=True, exist_ok=True)
    with open(json_path, 'w') as f:
        json.dump(data, f, indent=2)

