"""
Mock Adapter para slides - usado para desenvolvimento e testes

Este adapter gera conteúdo fictício sobre cibersegurança hospitalar,
permitindo testar o sistema sem dependências de APIs externas.
"""

from typing import Dict, List, Optional
from .slide_provider import SlideProvider


class MockSlideAdapter(SlideProvider):
    """
    Adapter simulado para testes e desenvolvimento.
    
    Gera slides fictícios sobre cibersegurança hospitalar sem
    necessidade de APIs externas. Útil para:
    - Desenvolvimento local
    - Testes unitários
    - Demonstrações
    - Ambiente de staging
    
    Exemplo:
        >>> adapter = MockSlideAdapter(num_slides=5)
        >>> total = adapter.get_total_slides()
        >>> print(total)
        5
        >>> slide = adapter.get_slide_content(1)
        >>> print(slide['title'])
        Introdução à Cibersegurança Hospitalar
    """
    
    # Conteúdo fictício para demonstração
    SLIDE_TEMPLATES = [
        {
            'title': 'Introdução à Cibersegurança Hospitalar',
            'content': 'Visão geral da importância da segurança de dados de saúde e principais ameaças no contexto hospitalar.',
            'notes': 'Enfatizar RGPD e regulamentações de saúde portuguesas.'
        },
        {
            'title': 'Phishing e Engenharia Social',
            'content': 'Como identificar emails maliciosos, técnicas comuns de phishing direcionado a profissionais de saúde.',
            'notes': 'Mostrar exemplos reais de tentativas de phishing em hospitais.'
        },
        {
            'title': 'Proteção de Dados de Pacientes',
            'content': 'Princípios de minimização de dados, consentimento informado e direitos dos titulares segundo RGPD.',
            'notes': 'Referir casos de violação de dados e consequências legais.'
        },
        {
            'title': 'Passwords e Autenticação',
            'content': 'Boas práticas para criação de passwords fortes, autenticação multi-fator, gestão de credenciais.',
            'notes': 'Demonstrar password manager e 2FA em ação.'
        },
        {
            'title': 'Ransomware em Ambiente Hospitalar',
            'content': 'Como ransomware pode paralisar operações hospitalares, medidas preventivas e planos de resposta.',
            'notes': 'Caso de estudo: ataque a hospital em Portugal.'
        },
        {
            'title': 'Dispositivos Médicos Conectados',
            'content': 'Riscos de segurança em IoT médico, bombas de infusão, monitores conectados e outros dispositivos.',
            'notes': 'Demonstrar vulnerabilidades conhecidas em equipamentos.'
        },
        {
            'title': 'Backup e Recuperação de Desastres',
            'content': 'Estratégias 3-2-1 para backup, testes regulares de recuperação, continuidade operacional.',
            'notes': 'Mostrar ferramentas de backup e procedimentos de teste.'
        },
        {
            'title': 'Resposta a Incidentes',
            'content': 'Procedimentos para identificar, conter e remediar incidentes de segurança, comunicação com autoridades.',
            'notes': 'Workflow de resposta a incidentes: deteção → contenção → erradicação → recuperação.'
        },
        {
            'title': 'Compliance e Auditorias',
            'content': 'Requisitos legais (RGPD, regulamentos saúde), preparação para auditorias, documentação necessária.',
            'notes': 'Checklist de compliance para DPOs.'
        },
        {
            'title': 'Cultura de Segurança',
            'content': 'Como promover awareness contínuo, reporting de incidentes sem penalizações, formação regular.',
            'notes': 'Programa de sensibilização: frequência, tópicos, gamificação.'
        }
    ]
    
    def __init__(self, num_slides: int = 10):
        """
        Inicializa MockAdapter.
        
        Args:
            num_slides: Número de slides a gerar (1-10)
        """
        if num_slides < 1:
            raise ValueError("num_slides deve ser >= 1")
        
        # Limita a 10 (temos 10 templates)
        self.num_slides = min(num_slides, len(self.SLIDE_TEMPLATES))
    
    def get_total_slides(self) -> int:
        """Retorna número total de slides."""
        return self.num_slides
    
    def get_slide_content(self, slide_num: int) -> Dict:
        """
        Retorna conteúdo de um slide fictício.
        
        Args:
            slide_num: Número do slide (1-indexed)
        
        Returns:
            dict: Conteúdo do slide
        """
        self.validate_slide_number(slide_num)
        
        # slide_num é 1-indexed, array é 0-indexed
        template = self.SLIDE_TEMPLATES[slide_num - 1]
        
        return {
            'slide_num': slide_num,
            'title': template['title'],
            'content': template['content'],
            'notes': template.get('notes', ''),
            'source': 'mock'
        }
    
    def get_slide_thumbnail(self, slide_num: int) -> Optional[str]:
        """
        Retorna URL de thumbnail placeholder.
        
        Args:
            slide_num: Número do slide (1-indexed)
        
        Returns:
            str: URL de placeholder image
        """
        self.validate_slide_number(slide_num)
        
        # Usa serviço placeholder público
        return f'https://via.placeholder.com/400x300/1976D2/FFFFFF?text=Slide+{slide_num}'
    
    def get_all_slides(self) -> List[Dict]:
        """
        Retorna todos os slides.
        
        Returns:
            list: Lista com conteúdo de todos os slides
        """
        return [
            self.get_slide_content(i) 
            for i in range(1, self.num_slides + 1)
        ]
    
    def get_metadata(self) -> Dict:
        """
        Retorna metadados da apresentação mock.
        
        Returns:
            dict: Metadados
        """
        return {
            'title': 'Formação em Cibersegurança Hospitalar',
            'author': 'Hospital da Lapa - Departamento IT',
            'total_slides': self.num_slides,
            'type': 'mock',
            'language': 'pt-PT'
        }
