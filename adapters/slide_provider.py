"""
Interface abstrata para fornecedores de slides (Adapter Pattern)
 
Este módulo implementa o padrão Adapter para permitir integração
com diferentes fontes de slides mantendo interface comum.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional


class SlideProvider(ABC):
    """
    Interface abstrata para fornecedores de slides.
    
    Diferentes fontes (Google Slides, PowerPoint, PDF) implementam
    esta interface, permitindo ao Activity Manager trabalhar com
    qualquer fonte sem conhecer detalhes de implementação.
    
    Padrão: Adapter (GoF pp. 139-150)
    """
    
    @abstractmethod
    def get_total_slides(self) -> int:
        """
        Retorna o número total de slides disponíveis.
        
        Returns:
            int: Número total de slides
        """
        pass
    
    @abstractmethod
    def get_slide_content(self, slide_num: int) -> Dict:
        """
        Retorna o conteúdo de um slide específico.
        
        Args:
            slide_num: Número do slide (1-indexed)
        
        Returns:
            dict: Conteúdo do slide com estrutura:
                {
                    'slide_num': int,
                    'title': str,
                    'content': str,
                    'notes': str (opcional)
                }
        
        Raises:
            ValueError: Se slide_num inválido
        """
        pass
    
    @abstractmethod
    def get_slide_thumbnail(self, slide_num: int) -> Optional[str]:
        """
        Retorna URL da thumbnail de um slide.
        
        Args:
            slide_num: Número do slide (1-indexed)
        
        Returns:
            str: URL da thumbnail ou None se não disponível
        """
        pass
    
    @abstractmethod
    def get_all_slides(self) -> List[Dict]:
        """
        Retorna conteúdo de todos os slides.
        
        Útil para carregamento inicial ou cache.
        
        Returns:
            list: Lista de dicionários com conteúdo dos slides
        """
        pass
    
    def validate_slide_number(self, slide_num: int) -> None:
        """
        Valida se número do slide é válido.
        
        Método auxiliar comum a todos os adapters.
        
        Args:
            slide_num: Número do slide a validar
        
        Raises:
            ValueError: Se slide_num < 1 ou > total_slides
        """
        total = self.get_total_slides()
        if slide_num < 1 or slide_num > total:
            raise ValueError(
                f"Slide number {slide_num} inválido. "
                f"Deve estar entre 1 e {total}"
            )
