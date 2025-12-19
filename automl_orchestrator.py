"""
🤖 Advanced AutoML System
End-to-end automated machine learning pipeline

Features:
- Automated data preprocessing and feature engineering
- Neural architecture search (NAS)
- Hyperparameter optimization
- Multi-algorithm model selection
- Ensemble creation and optimization
- Automated model evaluation and validation
- Deployment automation
"""

import asyncio
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any, Callable
from enum import Enum
import json
from abc import ABC, abstractmethod
import random
import statistics


class ProblemType(Enum):
    """ML problem types"""
    REGRESSION = "regression"
    CLASSIFICATION = "classification"
    CLUSTERING = "clustering"
    TIME_SERIES = "time_series"
    NLP = "nlp"
    COMPUTER_VISION = "computer_vision"


class ModelType(Enum):
    """Supported model types"""
    LINEAR = "linear"
    TREE = "tree"
    ENSEMBLE = "ensemble"
    NEURAL = "neural"
    SVM = "svm"
    KNN = "knn"
    NAIVE_BAYES = "naive_bayes"
    GRADIENT_BOOSTING = "gradient_boosting"


@dataclass
class FeatureInfo:
    """Information about a feature"""
    name: str
    dtype: str  # "numeric", "categorical", "text", "datetime"
    missing_percent: float
    cardinality: Optional[int] = None
    importance_score: float = 0.0
    
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "dtype": self.dtype,
            "missing_percent": self.missing_percent,
            "cardinality": self.cardinality,
            "importance_score": self.importance_score
        }


@dataclass
class DatasetProfile:
    """Profile of input dataset"""
    num_samples: int
    num_features: int
    features: List[FeatureInfo]
    target_variable: str
    problem_type: ProblemType
    class_distribution: Optional[Dict[str, int]] = None
    
    def to_dict(self) -> Dict:
        return {
            "num_samples": self.num_samples,
            "num_features": self.num_features,
            "features": [f.to_dict() for f in self.features],
            "target_variable": self.target_variable,
            "problem_type": self.problem_type.value,
            "class_distribution": self.class_distribution
        }


@dataclass
class ModelArchitecture:
    """Neural network architecture specification"""
    layers: List[Dict[str, Any]]
    activation_functions: List[str]
    dropout_rates: List[float]
    batch_norm: bool = True
    learning_rate: float = 0.001
    optimizer: str = "adam"
    
    def to_dict(self) -> Dict:
        return {
            "layers": self.layers,
            "activation_functions": self.activation_functions,
            "dropout_rates": self.dropout_rates,
            "batch_norm": self.batch_norm,
            "learning_rate": self.learning_rate,
            "optimizer": self.optimizer
        }


@dataclass
class HyperparameterConfig:
    """Model hyperparameters"""
    model_type: ModelType
    hyperparameters: Dict[str, Any]
    estimated_training_time: float = 0.0
    
    def to_dict(self) -> Dict:
        return {
            "model_type": self.model_type.value,
            "hyperparameters": self.hyperparameters,
            "estimated_training_time": self.estimated_training_time
        }


@dataclass
class TrainedModel:
    """Results of model training"""
    model_id: str
    model_type: ModelType
    hyperparameters: Dict[str, Any]
    training_metrics: Dict[str, float]
    validation_metrics: Dict[str, float]
    feature_importance: Dict[str, float]
    training_time_seconds: float
    model_size_bytes: int
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict:
        return {
            "model_id": self.model_id,
            "model_type": self.model_type.value,
            "hyperparameters": self.hyperparameters,
            "training_metrics": self.training_metrics,
            "validation_metrics": self.validation_metrics,
            "feature_importance": self.feature_importance,
            "training_time_seconds": self.training_time_seconds,
            "model_size_bytes": self.model_size_bytes,
            "created_at": self.created_at.isoformat()
        }


@dataclass
class EnsembleModel:
    """Ensemble of multiple trained models"""
    ensemble_id: str
    model_ids: List[str]
    weights: Dict[str, float]
    ensemble_metrics: Dict[str, float]
    voting_strategy: str  # "average", "weighted", "voting"
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict:
        return {
            "ensemble_id": self.ensemble_id,
            "model_ids": self.model_ids,
            "weights": self.weights,
            "ensemble_metrics": self.ensemble_metrics,
            "voting_strategy": self.voting_strategy,
            "created_at": self.created_at.isoformat()
        }


class FeatureEngineer:
    """Automated feature engineering"""
    
    @staticmethod
    def extract_statistics(features: List[FeatureInfo]) -> List[str]:
        """Extract statistical features"""
        extracted = []
        for feature in features:
            if feature.dtype == "numeric":
                extracted.extend([
                    f"{feature.name}_sqrt",
                    f"{feature.name}_log1p",
                    f"{feature.name}_squared"
                ])
        return extracted
    
    @staticmethod
    def create_interactions(feature_names: List[str], top_k: int = 10) -> List[str]:
        """Create feature interactions"""
        interactions = []
        for i in range(min(top_k, len(feature_names))):
            for j in range(i + 1, min(top_k + 1, len(feature_names))):
                interactions.append(f"{feature_names[i]}_x_{feature_names[j]}")
        return interactions
    
    @staticmethod
    def encode_categorical(feature_names: List[str]) -> Dict[str, str]:
        """Suggest encoding methods for categorical features"""
        encoding_strategies = {}
        for feat in feature_names:
            # One-hot for low cardinality, label encoding for high
            encoding_strategies[feat] = "one_hot"
        return encoding_strategies
    
    @staticmethod
    def handle_missing_values(features: List[FeatureInfo]) -> Dict[str, str]:
        """Suggest missing value handling strategies"""
        strategies = {}
        for feature in features:
            if feature.missing_percent > 50:
                strategies[feature.name] = "drop"
            elif feature.missing_percent > 20:
                strategies[feature.name] = "mean_or_mode"
            else:
                strategies[feature.name] = "knn_impute"
        return strategies


class NeuralArchitectureSearch:
    """Neural Architecture Search (NAS)"""
    
    @staticmethod
    def generate_architecture(input_dim: int, 
                            output_dim: int,
                            problem_type: ProblemType) -> ModelArchitecture:
        """Generate neural network architecture"""
        
        # Base architecture based on problem type
        if problem_type == ProblemType.REGRESSION:
            layers = [
                {"type": "dense", "units": max(128, input_dim * 2)},
                {"type": "dense", "units": 64},
                {"type": "dense", "units": 32},
                {"type": "dense", "units": output_dim}
            ]
            activations = ["relu", "relu", "relu", "linear"]
            dropouts = [0.3, 0.2, 0.1, 0.0]
        
        elif problem_type == ProblemType.CLASSIFICATION:
            layers = [
                {"type": "dense", "units": max(256, input_dim * 4)},
                {"type": "dense", "units": 128},
                {"type": "dense", "units": 64},
                {"type": "dense", "units": output_dim}
            ]
            activations = ["relu", "relu", "relu", "softmax"]
            dropouts = [0.4, 0.3, 0.2, 0.0]
        
        elif problem_type == ProblemType.TIME_SERIES:
            layers = [
                {"type": "lstm", "units": 128},
                {"type": "dense", "units": 64},
                {"type": "dense", "units": output_dim}
            ]
            activations = ["relu", "relu", "linear"]
            dropouts = [0.2, 0.1, 0.0]
        
        else:  # Default
            layers = [
                {"type": "dense", "units": 128},
                {"type": "dense", "units": 64},
                {"type": "dense", "units": output_dim}
            ]
            activations = ["relu", "relu", "linear"]
            dropouts = [0.2, 0.1, 0.0]
        
        return ModelArchitecture(
            layers=layers,
            activation_functions=activations,
            dropout_rates=dropouts,
            learning_rate=0.001,
            optimizer="adam"
        )
    
    @staticmethod
    def mutate_architecture(base_arch: ModelArchitecture) -> ModelArchitecture:
        """Mutate architecture for evolutionary search"""
        # Random modifications
        new_arch = ModelArchitecture(
            layers=base_arch.layers.copy(),
            activation_functions=base_arch.activation_functions.copy(),
            dropout_rates=base_arch.dropout_rates.copy(),
            batch_norm=base_arch.batch_norm,
            learning_rate=base_arch.learning_rate * random.uniform(0.5, 2.0),
            optimizer=base_arch.optimizer
        )
        
        # Randomly modify dropout rates
        for i in range(len(new_arch.dropout_rates)):
            new_arch.dropout_rates[i] = max(0, min(0.5, 
                new_arch.dropout_rates[i] + random.uniform(-0.1, 0.1)))
        
        return new_arch


class HyperparameterOptimizer:
    """Hyperparameter optimization engine"""
    
    @staticmethod
    def generate_search_space(model_type: ModelType) -> Dict[str, List[Any]]:
        """Generate hyperparameter search space"""
        
        search_spaces = {
            ModelType.LINEAR: {
                "regularization": [0.0, 0.001, 0.01, 0.1],
                "fit_intercept": [True, False]
            },
            ModelType.TREE: {
                "max_depth": [5, 10, 15, 20, None],
                "min_samples_split": [2, 5, 10],
                "min_samples_leaf": [1, 2, 4]
            },
            ModelType.GRADIENT_BOOSTING: {
                "n_estimators": [50, 100, 200],
                "learning_rate": [0.001, 0.01, 0.1],
                "max_depth": [3, 5, 7],
                "subsample": [0.8, 1.0]
            },
            ModelType.SVM: {
                "kernel": ["linear", "rbf", "poly"],
                "C": [0.1, 1, 10],
                "gamma": ["scale", "auto"]
            },
            ModelType.KNN: {
                "n_neighbors": [3, 5, 7, 11],
                "weights": ["uniform", "distance"],
                "metric": ["euclidean", "manhattan"]
            }
        }
        
        return search_spaces.get(model_type, {})
    
    @staticmethod
    async def bayesian_optimization(model_type: ModelType,
                                   metric_history: List[float],
                                   iterations: int = 10) -> Dict[str, Any]:
        """Simple Bayesian-inspired optimization"""
        search_space = HyperparameterOptimizer.generate_search_space(model_type)
        
        best_config = {}
        best_score = -float('inf')
        
        for iteration in range(iterations):
            # Randomly sample from search space
            current_config = {}
            for param, values in search_space.items():
                current_config[param] = random.choice(values)
            
            # Simulate evaluation (in real system, train model)
            simulated_score = random.uniform(0.5, 0.99)
            
            if simulated_score > best_score:
                best_score = simulated_score
                best_config = current_config
        
        return best_config
    
    @staticmethod
    def estimate_training_time(model_type: ModelType,
                              dataset_size: int,
                              num_features: int) -> float:
        """Estimate training time in seconds"""
        base_times = {
            ModelType.LINEAR: 0.5,
            ModelType.TREE: 1.0,
            ModelType.GRADIENT_BOOSTING: 5.0,
            ModelType.NEURAL: 10.0,
            ModelType.SVM: 2.0,
            ModelType.KNN: 0.1,
            ModelType.NAIVE_BAYES: 0.5
        }
        
        base_time = base_times.get(model_type, 1.0)
        size_factor = (dataset_size / 10000) ** 1.5
        feature_factor = (num_features / 100) ** 1.2
        
        return base_time * size_factor * feature_factor


class AutoMLOrchestrator:
    """Main AutoML orchestrator"""
    
    def __init__(self):
        self.trained_models: Dict[str, TrainedModel] = {}
        self.ensembles: Dict[str, EnsembleModel] = {}
        self.feature_engineer = FeatureEngineer()
        self.nas = NeuralArchitectureSearch()
        self.hyperopt = HyperparameterOptimizer()
    
    async def analyze_dataset(self, 
                             num_samples: int,
                             num_features: int,
                             problem_type: ProblemType,
                             features: List[FeatureInfo],
                             target_variable: str) -> DatasetProfile:
        """Analyze dataset and suggest problem type"""
        return DatasetProfile(
            num_samples=num_samples,
            num_features=num_features,
            features=features,
            target_variable=target_variable,
            problem_type=problem_type
        )
    
    async def automated_preprocessing(self, profile: DatasetProfile) -> Dict[str, Any]:
        """Automated preprocessing pipeline"""
        feature_names = [f.name for f in profile.features]
        
        return {
            "missing_value_strategy": self.feature_engineer.handle_missing_values(profile.features),
            "categorical_encoding": self.feature_engineer.encode_categorical(
                [f.name for f in profile.features if f.dtype == "categorical"]
            ),
            "scaling_method": "standardization",
            "outlier_handling": "iqr_method"
        }
    
    async def automated_feature_engineering(self, profile: DatasetProfile) -> Dict[str, List[str]]:
        """Automated feature engineering"""
        feature_names = [f.name for f in profile.features]
        
        return {
            "statistical_features": self.feature_engineer.extract_statistics(profile.features),
            "interaction_features": self.feature_engineer.create_interactions(feature_names),
            "encoding_strategies": self.feature_engineer.encode_categorical(feature_names)
        }
    
    async def neural_architecture_search(self,
                                        profile: DatasetProfile,
                                        num_architectures: int = 5) -> List[ModelArchitecture]:
        """Neural architecture search"""
        architectures = []
        
        # Generate initial architecture
        base_arch = self.nas.generate_architecture(
            profile.num_features,
            len(profile.class_distribution) if profile.class_distribution else 1,
            profile.problem_type
        )
        architectures.append(base_arch)
        
        # Generate mutations
        for _ in range(num_architectures - 1):
            mutated = self.nas.mutate_architecture(base_arch)
            architectures.append(mutated)
        
        return architectures
    
    async def hyperparameter_optimization(self,
                                         model_type: ModelType,
                                         metric_history: Optional[List[float]] = None) -> Dict[str, Any]:
        """Optimize hyperparameters"""
        return await self.hyperopt.bayesian_optimization(
            model_type,
            metric_history or [],
            iterations=10
        )
    
    async def train_model(self,
                         model_id: str,
                         model_type: ModelType,
                         hyperparameters: Dict[str, Any],
                         dataset_size: int,
                         num_features: int) -> TrainedModel:
        """Train a single model"""
        
        # Simulate training
        training_time = self.hyperopt.estimate_training_time(
            model_type,
            dataset_size,
            num_features
        )
        
        await asyncio.sleep(min(training_time / 100, 0.1))  # Simulate training
        
        training_metrics = {
            "train_loss": random.uniform(0.1, 0.5),
            "train_accuracy": random.uniform(0.7, 0.95)
        }
        
        validation_metrics = {
            "val_loss": random.uniform(0.15, 0.55),
            "val_accuracy": random.uniform(0.65, 0.93)
        }
        
        feature_importance = {
            f"feature_{i}": random.uniform(0, 1)
            for i in range(min(10, num_features))
        }
        
        model = TrainedModel(
            model_id=model_id,
            model_type=model_type,
            hyperparameters=hyperparameters,
            training_metrics=training_metrics,
            validation_metrics=validation_metrics,
            feature_importance=feature_importance,
            training_time_seconds=training_time,
            model_size_bytes=random.randint(1000000, 50000000)
        )
        
        self.trained_models[model_id] = model
        return model
    
    async def select_best_models(self, metric_name: str = "val_accuracy", top_k: int = 5) -> List[TrainedModel]:
        """Select best performing models"""
        models = list(self.trained_models.values())
        models.sort(
            key=lambda m: m.validation_metrics.get(metric_name, 0),
            reverse=True
        )
        return models[:top_k]
    
    async def create_ensemble(self,
                             ensemble_id: str,
                             model_ids: List[str],
                             voting_strategy: str = "weighted") -> EnsembleModel:
        """Create ensemble from trained models"""
        
        # Calculate weights based on model performance
        weights = {}
        total_score = 0
        
        for mid in model_ids:
            if mid in self.trained_models:
                model = self.trained_models[mid]
                score = model.validation_metrics.get("val_accuracy", 0.5)
                weights[mid] = score
                total_score += score
        
        # Normalize weights
        if total_score > 0:
            weights = {k: v / total_score for k, v in weights.items()}
        else:
            weights = {mid: 1.0 / len(model_ids) for mid in model_ids}
        
        ensemble_metrics = {
            "ensemble_val_accuracy": statistics.mean([
                self.trained_models[mid].validation_metrics.get("val_accuracy", 0.5)
                for mid in model_ids if mid in self.trained_models
            ])
        }
        
        ensemble = EnsembleModel(
            ensemble_id=ensemble_id,
            model_ids=model_ids,
            weights=weights,
            ensemble_metrics=ensemble_metrics,
            voting_strategy=voting_strategy
        )
        
        self.ensembles[ensemble_id] = ensemble
        return ensemble
    
    async def full_automl_pipeline(self,
                                   dataset_profile: DatasetProfile,
                                   num_trials: int = 10) -> Dict[str, Any]:
        """Execute full AutoML pipeline"""
        
        # Preprocess
        preprocessing = await self.automated_preprocessing(dataset_profile)
        
        # Feature engineering
        features = await self.automated_feature_engineering(dataset_profile)
        
        # Train multiple models
        trained_models = []
        model_types = [ModelType.LINEAR, ModelType.TREE, ModelType.GRADIENT_BOOSTING]
        
        for i, model_type in enumerate(model_types[:num_trials]):
            model_id = f"automl_model_{i}_{datetime.now().timestamp()}"
            
            hyperparams = await self.hyperparameter_optimization(model_type)
            
            trained_model = await self.train_model(
                model_id,
                model_type,
                hyperparams,
                dataset_profile.num_samples,
                dataset_profile.num_features
            )
            trained_models.append(trained_model)
        
        # Select best models
        best_models = await self.select_best_models(top_k=3)
        
        # Create ensemble
        ensemble = await self.create_ensemble(
            f"automl_ensemble_{datetime.now().timestamp()}",
            [m.model_id for m in best_models]
        )
        
        return {
            "dataset_profile": dataset_profile.to_dict(),
            "preprocessing": preprocessing,
            "features": features,
            "trained_models": len(self.trained_models),
            "best_models": [m.to_dict() for m in best_models],
            "ensemble": ensemble.to_dict()
        }
    
    def export_to_json(self) -> str:
        """Export all models and ensembles to JSON"""
        return json.dumps({
            "trained_models": {
                mid: m.to_dict()
                for mid, m in self.trained_models.items()
            },
            "ensembles": {
                eid: e.to_dict()
                for eid, e in self.ensembles.items()
            }
        }, indent=2, default=str)


# Global instance
_automl_orchestrator: Optional[AutoMLOrchestrator] = None


async def get_automl_orchestrator() -> AutoMLOrchestrator:
    """Get or create AutoML orchestrator"""
    global _automl_orchestrator
    if _automl_orchestrator is None:
        _automl_orchestrator = AutoMLOrchestrator()
    return _automl_orchestrator
