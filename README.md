# Alego-manus

Um sistema interativo de aprendizado para legislação da Alego, inspirado nos modelos do Duolingo e Mimo.

## Sobre o Projeto

Alego-manus é uma aplicação educativa que transforma o estudo de legislações em uma experiência interativa e gamificada. O sistema foi desenvolvido especialmente para ajudar estudantes a memorizar e compreender melhor os textos legislativos, tornando o processo de estudo mais envolvente e eficaz.

### Principais Características

- **Aprendizado Progressivo**: O sistema utiliza três fases de dificuldade crescente:
  - Fase 1: Seleção de palavras-chave no contexto da legislação
  - Fase 2: Redução gradual de dicas disponíveis
  - Fase 3: Digitação das palavras sem dicas

- **Foco em Legislação**: Inicialmente projetado para a Resolução 1.218 da Alego, mas facilmente adaptável para outros documentos legislativos.

## Requisitos

- Python 3.7+
- Streamlit
- PyPDF2

## Instalação

```bash
# Clonar o repositório
git clone https://github.com/dyuliano14/Alego-manus.git
cd Alego-manus

# Criar ambiente virtual (opcional, mas recomendado)
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt
```

## Uso

1. Coloque seus arquivos PDF de legislação na pasta `data/`
2. Execute a aplicação:

```bash
streamlit run src/main.py
```

3. No navegador, selecione o documento de legislação e comece a jogar!

## Estrutura do Projeto

```
alego-manus/
├── data/                  # Diretório para armazenar PDFs e textos extraídos
├── src/                   # Código fonte da aplicação
│   ├── extractor/         # Módulos para extrair texto de PDFs
│   ├── game/              # Lógica do jogo e fases
│   ├── ui/                # Interface do usuário
│   └── main.py            # Ponto de entrada da aplicação
├── tests/                 # Testes unitários
└── README.md              # Documentação do projeto
```

## Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests com melhorias.

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes.# Alego-manus

Um sistema interativo de aprendizado para legislação da Alego, inspirado nos modelos do Duolingo e Mimo.

## Sobre o Projeto

Alego-manus é uma aplicação educativa que transforma o estudo de legislações em uma experiência interativa e gamificada. O sistema foi desenvolvido especialmente para ajudar estudantes a memorizar e compreender melhor os textos legislativos, tornando o processo de estudo mais envolvente e eficaz.

### Principais Características

- **Aprendizado Progressivo**: O sistema utiliza três fases de dificuldade crescente:
  - Fase 1: Seleção de palavras-chave no contexto da legislação
  - Fase 2: Redução gradual de dicas disponíveis
  - Fase 3: Digitação das palavras sem dicas

- **Foco em Legislação**: Inicialmente projetado para a Resolução 1.218 da Alego, mas facilmente adaptável para outros documentos legislativos.

## Requisitos

- Python 3.7+
- Streamlit
- PyPDF2

## Instalação

```bash
# Clonar o repositório
git clone https://github.com/dyuliano14/Alego-manus.git
cd Alego-manus

# Criar ambiente virtual (opcional, mas recomendado)
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt
```

## Uso

1. Coloque seus arquivos PDF de legislação na pasta `data/`
2. Execute a aplicação:

```bash
streamlit run src/main.py
```

3. No navegador, selecione o documento de legislação e comece a jogar!

## Estrutura do Projeto

```
alego-manus/
├── data/                  # Diretório para armazenar PDFs e textos extraídos
├── src/                   # Código fonte da aplicação
│   ├── extractor/         # Módulos para extrair texto de PDFs
│   ├── game/              # Lógica do jogo e fases
│   ├── ui/                # Interface do usuário
│   └── main.py            # Ponto de entrada da aplicação
├── tests/                 # Testes unitários
└── README.md              # Documentação do projeto
```

## Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests com melhorias.

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes.