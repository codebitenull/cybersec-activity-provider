"""
Certification Training Processor - Certificação profissional para DPOs.

Implementação concreta do Template Method para formações de certificação
profissional em cibersegurança para DPOs e responsáveis de segurança.
"""

from typing import Dict, Any
from .training_processor import TrainingProcessor


class CertificationTrainingProcessor(TrainingProcessor):
    """
    Processor para formações de certificação profissional.
    
    Características:
    - Pré-requisitos: Formação avançada + experiência
    - Avaliação rigorosa: >= 85% com ponderação
    - Certificação profissional reconhecida
    - Duração: ~120 minutos
    
    Público-alvo: DPOs, Responsáveis de Segurança, Gestão
    Conteúdo: Análise de risco (FAIR), auditorias, compliance ISO 27001
    """
    
    def validate_prerequisites(self) -> bool:
        """
        Valida pré-requisitos rigorosos para certificação.
        
        Requisitos:
        - Formação avançada completa
        - Pelo menos 6 meses de experiência em funções relacionadas
        
        NOTA: Por agora mock. Em implementação real, consultar BD.
        
        Returns:
            bool: True se pré-requisitos cumpridos
        """
        print(f"[CertificationProcessor] Validating prerequisites for {self.student_id}")
        
        # TODO: Em implementação real, consultar BD
        # has_advanced = check_training_completed(student_id, 'advanced')
        # has_experience = check_professional_experience(student_id, months=6)
        
        # Mock: simula validação
        has_advanced_training = True
        has_required_experience = True
        
        prerequisites_met = has_advanced_training and has_required_experience
        
        if not prerequisites_met:
            print(f"[CertificationProcessor] Prerequisites NOT met")
        else:
            print(f"[CertificationProcessor] Prerequisites met")
        
        return prerequisites_met
    
    def get_prerequisite_message(self) -> str:
        """
        Mensagem quando pré-requisitos não cumpridos.
        
        Returns:
            str: Mensagem explicativa detalhada
        """
        return (
            "Certificação profissional requer: "
            "(1) Conclusão da formação avançada, "
            "(2) Mínimo 6 meses de experiência em funções de DPO ou segurança. "
            "Por favor verifique os requisitos."
        )
    
    def evaluate(self) -> Dict[str, Any]:
        """
        Avalia estudante com critérios de certificação profissional.
        
        Critérios:
        - Score ponderado >= 85%
        - Questões têm pesos diferentes (difíceis valem mais)
        - Emite certificação profissional reconhecida
        
        REFACTORING T7: Uso de Extract Method da classe base
        
        Returns:
            dict: Resultado da avaliação com certificação profissional
        """
        # REFATORAÇÃO: Usa método comum
        self._log_evaluation_start()
        
        # TODO: Em implementação real, receber respostas e calcular score ponderado
        
        # Mock: simula avaliação ponderada
        # 20 questões com pesos diferentes
        questions = [
            {'weight': 1, 'correct': True},   # Fácil
            {'weight': 1, 'correct': True},   # Fácil
            {'weight': 2, 'correct': True},   # Média
            {'weight': 2, 'correct': True},   # Média
            {'weight': 3, 'correct': True},   # Difícil
            {'weight': 3, 'correct': False},  # Difícil - ERROU
            # ... mais questões
        ]
        
        # Simula score ponderado
        total_weight = 50
        obtained_weight = 44
        weighted_score = (obtained_weight / total_weight) * 100
        
        passed = weighted_score >= 85  # Critério: 85%
        
        evaluation_result = {
            'total_questions': 20,
            'weighted_score': weighted_score,
            'passing_score': 85,
            'passed': passed,
            'certification_issued': passed,
            'certification_type': 'Professional Cybersecurity',
            'evaluation_type': 'certification',
            'scoring_method': 'weighted'
        }
        
        # REFATORAÇÃO: Usa método comum com informação adicional
        extra_info = "(weighted)" if passed else ""
        self._log_evaluation_result(weighted_score, passed, extra_info)
        
        return evaluation_result
    
    def post_finalize(self, result: Dict) -> None:
        """
        Emite certificação profissional e notifica entidades.
        
        Sobrescreve método da classe base.
        
        Args:
            result: Resultado final do processamento
        """
        if result['passed']:
            self._issue_professional_certificate(result)
            self._notify_authorities(result)
    
    def _issue_professional_certificate(self, result: Dict) -> None:
        """
        Emite certificado profissional reconhecido.
        
        TODO: Em implementação real:
        - Gerar PDF com QR code
        - Registar em plataforma nacional de certificações
        - Enviar email com credenciais digitais
        - Atualizar CV do profissional
        
        Args:
            result: Resultado da avaliação
        """
        print(f"[CertificationProcessor] Issuing professional certificate for {self.student_id}")
        
        certificate_data = {
            'student_id': self.student_id,
            'certificate_type': 'Professional Cybersecurity Certification',
            'level': 'Advanced DPO',
            'weighted_score': result['evaluation']['weighted_score'],
            'issued_at': result['completed_at'],
            'valid_for': '3 years',
            'certificate_number': f'CERT-{self.student_id}-2026',
            'recognized_by': ['CNPD', 'ISO 27001']
        }
        
        # TODO: Gerar PDF, registar, notificar
        print(f"[CertificationProcessor] Professional certificate issued: {certificate_data}")
    
    def _notify_authorities(self, result: Dict) -> None:
        """
        Notifica DPO e entidades relevantes sobre nova certificação.
        
        Args:
            result: Resultado da avaliação
        """
        print(f"[CertificationProcessor] Notifying DPO about new certified professional")
        
        # TODO: Enviar notificações
        # - Email ao DPO do hospital
        # - Atualizar lista de profissionais certificados
        # - Notificar CNPD (se aplicável)
