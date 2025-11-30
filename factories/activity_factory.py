"""
Factory Method Pattern para criação de instâncias de atividades.

Este módulo implementa o padrão Factory Method conforme descrito no 
"Design Patterns: Elements of Reusable Object-Oriented Software" 
(Gamma et al., 1994), páginas 107-116.

O Factory Method permite que subclasses decidam qual classe concreta
instanciar, promovendo baixo acoplamento e extensibilidade.
"""

from models.activity_instance import (
    ActivityInstance,
    BasicTrainingInstance,
    AdvancedTrainingInstance,
    CertificationInstance
)


class ActivityInstanceFactory:
    """
    Factory para criação de instâncias de atividade.
    
    Implementa o padrão Factory Method para desacoplar a criação
    de objetos do código cliente. O endpoint /deploy não precisa
    saber quais classes concretas existem - apenas chama a factory.
    
    Benefícios:
    - Open/Closed Principle: Adicionar novos tipos não requer modificar o cliente
    - Single Responsibility: Lógica de criação centralizada
    - Facilita testes: Factory pode ser mockada
    """
    
    # Mapeamento de tipos para classes (pode ser configurável)
    _type_mapping = {
        'basic': BasicTrainingInstance,
        'advanced': AdvancedTrainingInstance,
        'certification': CertificationInstance
    }
    
    @classmethod
    def create_instance(cls, activity_id, student_id, config):
        """
        Factory Method: cria instância apropriada baseada na configuração.
        
        Este é o "Factory Method" propriamente dito. Decide qual classe
        concreta instanciar baseado no campo 'type' da configuração.
        
        Args:
            activity_id (str): Identificador da atividade
            student_id (str): Identificador do estudante (Inven!RAstdID)  
            config (dict): Configuração da atividade (json_params)
        
        Returns:
            ActivityInstance: Instância concreta (Basic, Advanced ou Certification)
        
        Raises:
            ValueError: Se o tipo especificado não for reconhecido
        
        Example:
            >>> factory = ActivityInstanceFactory()
            >>> config = {'type': 'advanced', 'title': '...'}
            >>> instance = factory.create_instance('act123', 'std456', config)
            >>> instance.get_training_type()
            'advanced'
        """
        # Extrair tipo da configuração (default: basic)
        training_type = config.get('type', 'basic').lower()
        
        # Validar tipo
        if training_type not in cls._type_mapping:
            # Tipo desconhecido - usar basic como fallback seguro
            # (Princípio: Fail gracefully)
            print(f"Warning: Unknown training type '{training_type}', defaulting to 'basic'")
            training_type = 'basic'
        
        # Obter classe concreta do mapeamento
        instance_class = cls._type_mapping[training_type]
        
        # Criar e retornar instância
        return instance_class(activity_id, student_id, config)
    
    @classmethod
    def get_supported_types(cls):
        """
        Retorna lista de tipos suportados.
        
        Útil para validação e documentação da API.
        
        Returns:
            list: Lista de strings com tipos suportados
        """
        return list(cls._type_mapping.keys())
    
    @classmethod
    def register_type(cls, type_name, instance_class):
        """
        Regista novo tipo de instância (extensibilidade).
        
        Permite adicionar novos tipos dinamicamente sem modificar
        o código da factory. Útil para plugins ou configuração externa.
        
        Args:
            type_name (str): Nome do tipo (ex: 'simulation')
            instance_class (class): Classe concreta (deve herdar de ActivityInstance)
        
        Raises:
            TypeError: Se instance_class não herdar de ActivityInstance
        
        Example:
            >>> class SimulationInstance(ActivityInstance):
            ...     pass
            >>> ActivityInstanceFactory.register_type('simulation', SimulationInstance)
        """
        # Validar que a classe herda de ActivityInstance
        if not issubclass(instance_class, ActivityInstance):
            raise TypeError(
                f"{instance_class.__name__} must inherit from ActivityInstance"
            )
        
        cls._type_mapping[type_name] = instance_class
        print(f"Registered new activity type: '{type_name}'")
