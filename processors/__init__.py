"""
Package de Processors usando Template Method Pattern.

Implementa o padrão Template Method (GoF) para processar diferentes
tipos de formação com workflow comum mas avaliação específica.
"""

from .training_processor import TrainingProcessor
from .basic_processor import BasicTrainingProcessor
from .advanced_processor import AdvancedTrainingProcessor
from .certification_processor import CertificationTrainingProcessor

__all__ = [
    'TrainingProcessor',
    'BasicTrainingProcessor',
    'AdvancedTrainingProcessor',
    'CertificationTrainingProcessor'
]
