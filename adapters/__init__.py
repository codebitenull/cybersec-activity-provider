"""
Package de Adapters para diferentes fontes de slides.
 
Implementa o padrão Adapter (GoF) para permitir integração
com múltiplas fontes mantendo interface comum.
"""

from .slide_provider import SlideProvider
from .mock_slide_adapter import MockSlideAdapter
from .google_slides_adapter import GoogleSlidesAdapter

__all__ = [
    'SlideProvider',
    'MockSlideAdapter',
    'GoogleSlidesAdapter'
]
