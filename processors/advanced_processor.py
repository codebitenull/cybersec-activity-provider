"""
Advanced Training Processor - Formação avançada com certificação RGPD.

Implementação concreta do Template Method para formações avançadas
em cibersegurança para profissionais clínicos.
"""

from typing import Dict, Any
from .training_processor import TrainingProcessor


class AdvancedTrainingProcessor(TrainingProcessor):
    """
    Processor para formações avançadas.
    
    Características:
    - Pré-requisito: Formação básica completa
    - Avaliação rigorosa: >= 80% para passar
    - Certificação RGPD emitida
    - Duração: ~60 minutos
    
    Público-alvo: Profissionais clínicos (médicos, enfermeiros)
    Conteúdo: Proteção de dados de saúde, minimização, consentimentos
    """
    
    def validate_prerequisites(self) -> bool:
        """
        Valida que estudante completou formação básica.
        
        NOTA: Por agora retorna True (mock). Em implementação real,
        consultaria base de dados para verificar se estudante tem
        BasicTraining completa.
        
        Returns:
            bool: True se formação básica completa, False caso contrário
        """
        print(f"[AdvancedProcessor] Validating prerequisites for {self.student_id}")
        
        # TODO: Em implementação real, consultar BD
        # has_basic = check_training_completed(student_id, 'basic')
        
        # Mock: assume que estudante tem básica completa
        has_basic_training = True
        
        if not has_basic_training:
            print(f"[AdvancedProcessor] Prerequisites NOT met - Basic training required")
        else:
            print(f"[AdvancedProcessor] Prerequisites met")
        
        return has_basic_training
    
    def get_prerequisite_message(self) -> str:
        """
        Mensagem quando pré-requisitos não cumpridos.
        
        Returns:
            str: Mensagem explicativa
        """
        return (
            "Formação avançada requer conclusão da formação básica. "
            "Por favor complete a formação básica primeiro."
        )
    
    def evaluate(self) -> Dict[str, Any]:
        """
        Avalia estudante com critérios avançados.
        
        Critérios:
        - Score >= 80% (mais exigente que básica)
        - Emite certificação RGPD se passar
        
        Returns:
            dict: Resultado da avaliação com certificação
        """
        print(f"[AdvancedProcessor] Evaluating student {self.student_id}")
        
        # TODO: Em implementação real, receber respostas do quiz
        
        # Mock: simula que estudante acertou 13 de 15 questões
        total_questions = 15
        correct_answers = 13
        score = (correct_answers / total_questions) * 100
        
        passed = score >= 80  # Critério: 80% (mais exigente)
        
        evaluation_result = {
            'total_questions': total_questions,
            'correct_answers': correct_answers,
            'score': score,
            'passing_score': 80,
            'passed': passed,
            'certification_issued': passed,  # Emite se passar
            'certification_type': 'RGPD',
            'evaluation_type': 'advanced'
        }
        
        if passed:
            print(f"[AdvancedProcessor] Student PASSED with {score}% - Certificate issued")
        else:
            print(f"[AdvancedProcessor] Student FAILED with {score}%")
        
        return evaluation_result
    
    def post_finalize(self, result: Dict) -> None:
        """
        Emite certificado RGPD se estudante passou.
        
        Hook que executa após finalização principal.
        Sobrescreve método da classe base.
        
        Args:
            result: Resultado final do processamento
        """
        if result['passed']:
            self._issue_rgpd_certificate(result)
    
    def _issue_rgpd_certificate(self, result: Dict) -> None:
        """
        Emite certificado RGPD para estudante.
        
        TODO: Em implementação real:
        - Gerar PDF do certificado
        - Guardar na BD
        - Enviar email ao estudante
        - Notificar DPO
        
        Args:
            result: Resultado da avaliação
        """
        print(f"[AdvancedProcessor] Issuing RGPD certificate for {self.student_id}")
        
        certificate_data = {
            'student_id': self.student_id,
            'certificate_type': 'RGPD Data Protection',
            'score': result['evaluation']['score'],
            'issued_at': result['completed_at'],
            'valid_for': '2 years'
        }
        
        # TODO: Gerar PDF, guardar, notificar
        print(f"[AdvancedProcessor] Certificate issued: {certificate_data}")
