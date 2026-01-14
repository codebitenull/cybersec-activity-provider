"""
Basic Training Processor - Formação básica obrigatória.

Implementação concreta do Template Method para formações básicas
em cibersegurança hospitalar (profissionais administrativos).
"""

from typing import Dict, Any
from .training_processor import TrainingProcessor


class BasicTrainingProcessor(TrainingProcessor):
    """
    Processor para formações básicas.
    
    Características:
    - Sem pré-requisitos (qualquer profissional pode fazer)
    - Avaliação simples: >= 70% para passar
    - Sem certificação formal
    - Duração: ~30 minutos
    
    Público-alvo: Profissionais administrativos e suporte
    Conteúdo: Conceitos essenciais (phishing, passwords básicas)
    """
    
    def validate_prerequisites(self) -> bool:
        """
        Formações básicas não têm pré-requisitos.
        
        Qualquer profissional do hospital pode fazer.
        
        Returns:
            bool: Sempre True (sem pré-requisitos)
        """
        print(f"[BasicProcessor] Validating prerequisites - No requirements")
        return True  # Sempre permite
    
    def get_prerequisite_message(self) -> str:
        """
        Mensagem de pré-requisitos (nunca usada pois sempre passa).
        
        Returns:
            str: Mensagem vazia
        """
        return ""
    
    def evaluate(self) -> Dict[str, Any]:
        """
        Avalia estudante com critérios básicos.
        
        Critério: Score >= 70% para passar
        Sem ponderação, sem certificação.
        
        NOTA: Por agora retorna mock data. Em implementação real,
        receberia respostas do quiz e calcularia score real.
        
        Returns:
            dict: Resultado da avaliação
        """
        print(f"[BasicProcessor] Evaluating student {self.student_id}")
        
        # TODO: Em implementação real, receber respostas do quiz
        # Por agora, simula avaliação
        
        # Mock: simula que estudante acertou 8 de 10 questões
        total_questions = 10
        correct_answers = 8
        score = (correct_answers / total_questions) * 100
        
        passed = score >= 70  # Critério: 70%
        
        evaluation_result = {
            'total_questions': total_questions,
            'correct_answers': correct_answers,
            'score': score,
            'passing_score': 70,
            'passed': passed,
            'certification_issued': False,  # Básica não emite certificado
            'evaluation_type': 'basic'
        }
        
        if passed:
            print(f"[BasicProcessor] Student PASSED with {score}%")
        else:
            print(f"[BasicProcessor] Student FAILED with {score}%")
        
        return evaluation_result
    
    # Não precisa sobrescrever post_finalize() porque básica não emite certificado
