"""
Template Method Pattern para processar formações.

Este módulo implementa o padrão Template Method conforme descrito no
"Design Patterns: Elements of Reusable Object-Oriented Software"
(Gamma et al., 1995), páginas 325-330.

O Template Method define o esqueleto de um algoritmo, permitindo que
subclasses redefinam certos passos sem alterar a estrutura geral.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Any


class TrainingProcessor(ABC):
    """
    Classe abstrata que define o Template Method para processar formações.
    
    O método process() define a sequência fixa de passos para processar
    qualquer formação. Subclasses implementam os passos que variam
    (validate_prerequisites, evaluate).
    
    Padrão: Template Method (GoF pp. 325-330) 
    
    Workflow fixo:
    1. validate_prerequisites() - Verifica se estudante pode fazer formação
    2. load_training_content() - Carrega slides via Adapter (Tópico 5)
    3. initialize_session() - Prepara sessão de formação
    4. evaluate() - Avalia estudante (VARIA por tipo)
    5. finalize() - Guarda progresso e finaliza
    """
    
    def __init__(self, instance_data: Dict, student_id: str, slide_adapter):
        """
        Inicializa processor.
        
        Args:
            instance_data: Dados da instância de formação
            student_id: ID do estudante
            slide_adapter: Adapter de slides (Tópico 5 - Adapter Pattern)
        """
        self.instance_data = instance_data
        self.student_id = student_id
        self.slide_adapter = slide_adapter
        self.session_data = {}
        self.start_time = None
        self.end_time = None
    
    # =========================================================================
    # TEMPLATE METHOD - Define workflow fixo
    # =========================================================================
    
    def process(self) -> Dict[str, Any]:
        """
        Template Method - Define o algoritmo de processamento.
        
        Este método NÃO deve ser sobrescrito pelas subclasses.
        Define a sequência fixa de passos. Cada passo pode ser
        concreto (implementado aqui) ou abstrato (implementado
        nas subclasses).
        
        Returns:
            dict: Resultado do processamento com status e dados
        
        Example:
            >>> processor = BasicTrainingProcessor(instance, student, adapter)
            >>> result = processor.process()
            >>> print(result['status'])
            'completed'
        """
        try:
            # Passo 1: Validar pré-requisitos (abstrato - varia)
            if not self.validate_prerequisites():
                return {
                    'status': 'failed',
                    'reason': 'prerequisites_not_met',
                    'message': self.get_prerequisite_message()
                }
            
            # Passo 2: Carregar conteúdo (concreto - comum)
            self.load_training_content()
            
            # Passo 3: Inicializar sessão (concreto - comum)
            self.initialize_session()
            
            # Passo 4: Avaliar estudante (abstrato - varia)
            evaluation_result = self.evaluate()
            
            # Passo 5: Finalizar (concreto - comum)
            final_result = self.finalize(evaluation_result)
            
            return final_result
        
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Processing failed: {str(e)}'
            }
    
    # =========================================================================
    # MÉTODOS ABSTRATOS - Subclasses DEVEM implementar
    # =========================================================================
    
    @abstractmethod
    def validate_prerequisites(self) -> bool:
        """
        Valida se estudante cumpre pré-requisitos para esta formação.
        
        Este método VARIA conforme o tipo:
        - Basic: Sem pré-requisitos (sempre True)
        - Advanced: Requer formação básica completa
        - Certification: Requer formação avançada + experiência
        
        Returns:
            bool: True se pré-requisitos cumpridos, False caso contrário
        """
        pass
    
    @abstractmethod
    def get_prerequisite_message(self) -> str:
        """
        Retorna mensagem sobre pré-requisitos não cumpridos.
        
        Returns:
            str: Mensagem explicativa
        """
        pass
    
    @abstractmethod
    def evaluate(self) -> Dict[str, Any]:
        """
        Avalia o desempenho do estudante na formação.
        
        Este é o método que MAIS VARIA entre tipos:
        - Basic: Avaliação simples (>= 70%)
        - Advanced: Avaliação detalhada + certificação RGPD
        - Certification: Avaliação ponderada + certificação profissional
        
        Returns:
            dict: Resultado da avaliação com score, passed, etc.
        """
        pass
    
    # =========================================================================
    # MÉTODOS CONCRETOS - Comuns a todos (podem ser sobrescritos se necessário)
    # =========================================================================
    
    def load_training_content(self) -> None:
        """
        Carrega conteúdo da formação via Adapter Pattern (Tópico 5).
        
        Este método é COMUM a todos os tipos - usa o slide_adapter
        para carregar slides independentemente da fonte (Mock, Google, etc.)
        """
        self.session_data['slides'] = self.slide_adapter.get_all_slides()
        self.session_data['total_slides'] = self.slide_adapter.get_total_slides()
        
        print(f"[TrainingProcessor] Loaded {self.session_data['total_slides']} slides")
    
    def initialize_session(self) -> None:
        """
        Inicializa sessão de formação.
        
        Método COMUM - prepara dados da sessão, regista início.
        """
        self.start_time = datetime.now()
        self.session_data['started_at'] = self.start_time.isoformat()
        self.session_data['student_id'] = self.student_id
        self.session_data['training_type'] = self.instance_data.get('type', 'unknown')
        
        print(f"[TrainingProcessor] Session initialized for student {self.student_id}")
    
    def finalize(self, evaluation_result: Dict) -> Dict[str, Any]:
        """
        Finaliza processamento e guarda resultado.
        
        Método COMUM - guarda progresso, calcula duração, prepara resposta.
        
        Args:
            evaluation_result: Resultado da avaliação
        
        Returns:
            dict: Resultado final completo
        """
        self.end_time = datetime.now()
        duration = (self.end_time - self.start_time).total_seconds()
        
        final_result = {
            'status': 'completed',
            'student_id': self.student_id,
            'training_type': self.session_data['training_type'],
            'started_at': self.session_data['started_at'],
            'completed_at': self.end_time.isoformat(),
            'duration_seconds': duration,
            'evaluation': evaluation_result,
            'passed': evaluation_result.get('passed', False)
        }
        
        # Hook para subclasses adicionarem lógica final (ex: emitir certificado)
        self.post_finalize(final_result)
        
        print(f"[TrainingProcessor] Finalized - Passed: {final_result['passed']}")
        
        return final_result
    
    def post_finalize(self, result: Dict) -> None:
        """
        Hook para subclasses adicionarem lógica após finalização.
        
        Por defeito não faz nada. Subclasses podem sobrescrever para:
        - Emitir certificados
        - Enviar notificações
        - Atualizar estatísticas
        
        Args:
            result: Resultado final do processamento
        """
        pass  # Hook opcional
    
    # =========================================================================
    # MÉTODOS AUXILIARES
    # =========================================================================
    
    def get_training_type(self) -> str:
        """Retorna tipo de formação (basic, advanced, certification)."""
        return self.instance_data.get('type', 'unknown')
    
    def get_duration_minutes(self) -> int:
        """Retorna duração esperada da formação."""
        return self.instance_data.get('durationMinutes', 30)
