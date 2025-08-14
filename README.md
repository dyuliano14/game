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

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes.

# Jogo de Missões – Controlador de Estudos

Gere missões a partir de PDFs (leis/resoluções) e treine com lacunas. Mapa “gamer” com progressão, salvamento de status e UI simplificada para estudo.

## Recursos
- Upload de PDF e geração automática de missões.
- Mapa de missões em zigue-zague com bloqueio de fases.
- Tela de jogo com lacunas, feedback visual e progresso.
- Salvar/Carregar status local por documento.
- Estilo visual alinhado ao dashboard.

## Estrutura
```
src/
  main.py
  extractor/
    pdf_extractor.py
  ui/
    app.py
    routes.py
    components.py
    init_state.py
    text_format.py
    static/
      styles.css
.streamlit/
  config.toml
requirements.txt
```

## Rodar local (Windows)
1) Criar ambiente e instalar dependências:
```
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```
2) Executar:
```
python -m streamlit run src\main.py
```

## Deploy – Streamlit Community Cloud (recomendado)
1) Suba o repositório no GitHub.
2) Em https://share.streamlit.io → New app:
   - Repo/branch do projeto
   - Main file: `src/main.py`
3) Deploy. A URL ficará algo como `https://seu-app.streamlit.app/`.
4) Opcional: Settings → Domains → domínio custom.

Para incorporar no seu site:
```
<iframe src="https://seu-app.streamlit.app/?embed=true"
        style="width:100%;height:90vh;border:0;border-radius:14px;"></iframe>
```

## Deploy com Docker (opcional)
```
docker build -t jogo-alego .
docker run -p 8501:8501 jogo-alego
```

## Dicas
- Para problemas de “múltiplos botões iguais”, adicione `key=` único nos componentes Streamlit.
- Mantendo `requirements.txt` mínimo, o deploy fica mais rápido e confiável.

Licença: MIT