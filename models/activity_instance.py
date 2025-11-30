"""
Módulo de instâncias de atividades usando Factory Method Pattern

Este módulo implementa o padrão Factory Method para criar diferentes
tipos de instâncias de formação em cibersegurança hospitalar.
"""

from abc import ABC, abstractmethod
from datetime import datetime
import uuid


class ActivityInstance(ABC):
    """
    Classe abstrata base para todas as instâncias de atividade.
    
    Define a interface comum que todas as instâncias concretas devem implementar.
    Segue o padrão Factory Method do Gang of Four.
    """
    
    def __init__(self, activity_id, student_id, config):
        """
        Inicializa uma instância de atividade.
        
        Args:
            activity_id: Identificador da atividade
            student_id: Identificador do estudante (Inven!RAstdID)
            config: Dicionário de configuração (json_params)
        """
        self.instance_id = str(uuid.uuid4())
        self.activity_id = activity_id
        self.student_id = student_id
        self.config = config
        self.created_at = datetime.now().isoformat()
        self.status = 'active'
    
    @abstractmethod
    def get_training_type(self):
        """Retorna o tipo de formação (basic, advanced, certification)"""
        pass
    
    @abstractmethod
    def get_duration_minutes(self):
        """Retorna a duração esperada em minutos"""
        pass
    
    @abstractmethod
    def requires_certification(self):
        """Indica se esta formação emite certificado formal"""
        pass
    
    @abstractmethod
    def get_target_audience(self):
        """Retorna o público-alvo desta formação"""
        pass
    
    def to_dict(self):
        """
        Converte a instância para dicionário (serialização).
        
        Returns:
            dict: Representação da instância
        """
        return {
            'instanceID': self.instance_id,
            'activityID': self.activity_id,
            'studentID': self.student_id,
            'config': self.config,
            'createdAt': self.created_at,
            'status': self.status,
            'type': self.get_training_type(),
            'durationMinutes': self.get_duration_minutes(),
            'requiresCertification': self.requires_certification(),
            'targetAudience': self.get_target_audience()
        }


class BasicTrainingInstance(ActivityInstance):
    """
    Formação básica em cibersegurança para profissionais administrativos.
    
    Características:
    - Duração: 30 minutos
    - Sem certificação formal
    - Focada em conceitos essenciais (phishing, passwords)
    """
    
    def get_training_type(self):
        return "basic"
    
    def get_duration_minutes(self):
        return 30
    
    def requires_certification(self):
        return False
    
    def get_target_audience(self):
        return "Profissionais administrativos e suporte"


class AdvancedTrainingInstance(ActivityInstance):
    """
    Formação avançada em cibersegurança para profissionais clínicos.
    
    Características:
    - Duração: 60 minutos
    - Com certificação RGPD
    - Focada em proteção de dados de saúde e minimização
    """
    
    def get_training_type(self):
        return "advanced"
    
    def get_duration_minutes(self):
        return 60
    
    def requires_certification(self):
        return True
    
    def get_target_audience(self):
        return "Profissionais clínicos (médicos, enfermeiros)"


class CertificationInstance(ActivityInstance):
    """
    Formação de certificação profissional para DPOs e responsáveis de segurança.
    
    Características:
    - Duração: 120 minutos
    - Certificação profissional reconhecida
    - Focada em análise de risco, auditorias e compliance
    """
    
    def get_training_type(self):
        return "certification"
    
    def get_duration_minutes(self):
        return 120
    
    def requires_certification(self):
        return True
    
    def get_target_audience(self):
        return "DPOs, Responsáveis de Segurança, Gestão"
