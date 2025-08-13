from typing import List, Dict, Tuple, Optional
from src.extractor.pdf_extractor import PDFExtractor

class GameLevel:
    """Representa um nível no jogo de aprendizado."""
    
    def __init__(self, article_id: str, article_text: str, keywords: List[str]):
        self.article_id = article_id
        self.article_text = article_text
        self.keywords = keywords
        
    def _create_masked_text(self) -> str:
        """Cria uma versão do texto com palavras-chave mascaradas."""
        masked_text = self.article_text
        for keyword in self.keywords:
            masked_text = masked_text.replace(keyword, "_____")
        return masked_text

class GameEngine:
    """Motor do jogo para gerenciar níveis e interação."""
    
    def __init__(self, pdf_extractor: PDFExtractor):
        self.pdf_extractor = pdf_extractor
        self.current_level_index = 0
        self.levels = self._initialize_levels()
        
    def _initialize_levels(self) -> List[GameLevel]:
        """Inicializa os níveis do jogo a partir do PDF."""
        # Para simplificar, usamos um texto de exemplo com algumas palavras-chave
        article_text = """A Assembleia Legislativa do Estado de Goiás, com sede na Capital do Estado, funciona normalmente no Palácio Maguito Vilela.
        
§ 1º Havendo motivo relevante ou de força maior, a Assembleia Legislativa poderá, por deliberação da Mesa e ad referendum da maioria absoluta dos seus Membros, reunir-se em outro edifício ou em ponto diverso no território estadual, observado o que dispõe este Regimento.

§ 2º No Plenário do Palácio Maguito Vilela não se realizarão atos estranhos à função da Assembleia Legislativa.

CAPÍTULO II
DA HABILITAÇÃO PARA POSSE"""
        
        keywords = ["deliberação", "Membros", "edifício", "atos", "poder"]
        
        # Criar um nível de jogo básico
        level = GameLevel("1", article_text, keywords)
        
        return [level]
        
    def get_current_level(self) -> Optional[GameLevel]:
        """Retorna o nível atual."""
        if 0 <= self.current_level_index < len(self.levels):
            return self.levels[self.current_level_index]
        return None
        
    def advance_level(self) -> bool:
        """Avança para o próximo nível se houver."""
        if self.current_level_index < len(self.levels) - 1:
            self.current_level_index += 1
            return True
        return False
        
    def reset_level(self) -> None:
        """Reinicia o nível atual."""
        # Por enquanto não faz nada, mas pode ser expandido depois
        pass