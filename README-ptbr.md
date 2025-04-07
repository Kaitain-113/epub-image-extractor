> Escolha o idioma: **Português**, [Inglês](https://github.com/kaetaen/epub-image-extractor/blob/main/README.md)

# EPUB Image Extractor

## Descrição

O **EPUB Image Extractor** é uma aplicação web desenvolvida com **FastAPI** que permite o upload de arquivos EPUB, extrai as imagens contidas no arquivo e retorna um arquivo ZIP contendo todas as imagens extraídas. Após o envio do arquivo ZIP, os arquivos temporários (EPUB, imagens e ZIP) são automaticamente removidos para manter o ambiente limpo.

## Diagrama de Fluxo

<img src="docs/application_flow.png" width="500px"/>

## Tecnologias Utilizadas

- **Python 3.10+**
- **FastAPI**: Framework para construção de APIs rápidas e eficientes.
- **Uvicorn**: Servidor ASGI para executar a aplicação.
- **Jinja2**: Para renderização de templates HTML.
- **EbookLib**: Biblioteca para manipulação de arquivos EPUB.

## Funcionalidades

- Upload de arquivos EPUB.
- Extração de imagens contidas no arquivo EPUB.
- Compactação das imagens extraídas em um arquivo ZIP.
- Retorno do arquivo ZIP como resposta para download.
- Limpeza automática de arquivos temporários após o envio.

## To-Do

### Novos recursos

- [ ] Melhorias de design no front-end
- [ ] Suporte a upload de multiplos arquivos
- [ ] Opção de envio do arquivo compactado para o e-mail do usuário

### Débitos técnicos

- [ ] Testes unitários
- [ ] Verifiação de testes unitários e análise do código com Ruff no pipeline de CI/CD

## Estrutura do Projeto

```plaintext
epub-image-extractor/
├── docs
│   ├── application-flow.drawio
│   ├── application_flow.png
│   └── EPUB_Image_Extractor.postman_collection.json
├── epub-image-extractor
│   ├── helpers.py
│   ├── __init__.py
│   ├── main.py
│   └── services.py
├── static
│   ├── css
│   │   └── bootstrap
│   │       └── bootstrap.min.css
│   ├── images
│   │   └── favicon.png
│   └── js
│       └── bootstrap
│           └── bootstrap.bundle.min.js
├── templates
│   └── upload.jinja
├── pyproject.toml
├── README.md
├── README-ptbr.md
└── uv.lock
```

- `docs`: Contém arquivos de documentação do projeto
- `epub-image-extractor/main.py`: Ponto de entrada do projeto
- `epub-image-extractor/helpers.py`: Funções auxiliares para tarefas repetitivas
- `epub-image-extractor/services.py`: Responsável pela camada de Serviços
- `templates`: Contém os arquivos de template do front-end (Jinja)
- `static`: Arquivos estáticos utilizados pelo front-end.

## Instalação

1. **Instale o uv** 

Instale o **uv** em seu sistema seguindo os passos [desta página](https://docs.astral.sh/uv/getting-started/installation/)

2. **Clone o repositório**:

```bash
git clone https://github.com/kaetaen/epub-image-extractor.git
cd epub-image-extractor
```

3. **Instale as dependencias**

```bash
uv sync
```

## Uso

1. **Habilite o ambiente virtual**

```bash
source .venv/bin/activate 
```

2. **Inicie o servidor**:

```bash
uv run task serve
```

3. **Acesse a aplicação**:

> Abra o navegador e vá para: [http://localhost:8000](http://localhost:8000)

4. **Faça o upload de um arquivo EPUB**:
   - Acesse a página inicial.
   - Faça o upload de um arquivo EPUB.
   - Após o processamento o download será feito automáticamente.


## Endpoints

### `GET /`
- Renderiza a página de upload.

### `POST /upload`
- **Descrição**: Recebe um arquivo EPUB, extrai as imagens, compacta em um ZIP e retorna o arquivo.
- **Parâmetros**:
  - `epub_file` (form-data): Arquivo EPUB enviado pelo usuário.
- **Resposta**:
  - `FileResponse`: Arquivo ZIP contendo as imagens extraídas.


## Autor

Desenvolvido por **Rubens dos Santos**