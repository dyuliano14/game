import PyPDF2
import re
import os
from typing import Dict, List, Tuple

class PDFExtractor:
    """Classe para extrair conteúdo de arquivos PDF."""
    
    def __init__(self, pdf_path: str):
        """
        Inicializa o extrator com o caminho para o PDF.
        
        Args:
            pdf_path: Caminho para o arquivo PDF da legislação
        """
        self.pdf_path = pdf_path
        self.text_by_article = {}
        self.articles = []
        self.keywords = set()
        
    def extract_text(self) -> str:
        """Extrai texto de um arquivo PDF."""
        # Normalmente usaria PyPDF2 ou pdfminer aqui
        # Para simplificar, apenas lemos o arquivo como texto
        try:
            with open(self.pdf_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Erro ao extrair texto do PDF: {e}")
            return "Texto de exemplo para o jogo."
    
    def extract_articles(self) -> Dict[str, str]:
        """
        Extrai artigos individuais da legislação.
        
        Returns:
            Um dicionário mapeando identificadores de artigos para seus textos
        """
        full_text = self.extract_text()
        
        # Regex para encontrar artigos (pode precisar de ajustes com base no formato exato)
        article_pattern = r'Art\.\s+(\d+)[º°]?\s*[-–.]?\s*(.*?)(?=Art\.\s+\d+[º°]?|$)'
        matches = re.finditer(article_pattern, full_text, re.DOTALL)
        
        for match in matches:
            article_num = match.group(1)
            article_text = match.group(2).strip()
            self.text_by_article[f"Art. {article_num}"] = article_text
            self.articles.append((f"Art. {article_num}", article_text))
            
        return self.text_by_article
    
    def extract_keywords(self, text: str, count: int = 5) -> list:
        """Extrai palavras-chave de um texto."""
        # Esta seria uma implementação mais sofisticada com NLP
        # Por enquanto, retornamos algumas palavras importantes do texto
        common_words = ["deliberação", "Membros", "edifício", "atos", "poder"]
        return common_words[:count]
    
    def get_paragraph_with_context(self, article_id: str, keyword: str) -> Tuple[str, List[int]]:
        """
        Retorna um parágrafo contendo a palavra-chave e suas posições.
        
        Args:
            article_id: ID do artigo (ex: "Art. 1")
            keyword: Palavra-chave a ser destacada
            
        Returns:
            Tuple contendo o parágrafo e uma lista de posições iniciais da palavra-chave
        """
        if article_id not in self.text_by_article:
            return "", []
            
        text = self.text_by_article[article_id]
        paragraphs = text.split('\n')
        
        for paragraph in paragraphs:
            if keyword.lower() in paragraph.lower():
                positions = []
                lower_para = paragraph.lower()
                lower_keyword = keyword.lower()
                start = 0
                
                while True:
                    pos = lower_para.find(lower_keyword, start)
                    if pos == -1:
                        break
                    positions.append(pos)
                    start = pos + len(lower_keyword)
                
                return paragraph, positions
                
        return "", []