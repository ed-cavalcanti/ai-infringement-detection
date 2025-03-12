## Classificação de transcrição de vídeos

Repositório utilizado para armazenar os códigos de teste para os experimentos de pesquisa relacionado a detecção de infrações eleitorais em imagens de redes sociais de políticos.

## Requisitos

- Python 3.13.2
- Postgresql 17
- Google Cloud Plataform

## Rodando localmente

Clone o projeto

```bash
  git clone https://github.com/ed-cavalcanti/ai-infringement-detection
```

Entre no diretório do projeto

```bash
  cd ai-infringement-detection
```

Criar o ambiente virtual:

```bash
  python -m venv venv
```

Ativar o ambiente virtual:

No Windows:

```bash
venv\Scripts\activate
```

No macOS/Linux:

```bash
source venv/bin/activate
```

Instalar as dependências:

```bash
pip install -r requirements.txt
```
---

## Subindo o banco de dados

Cria um novo banco de dados no Postgres:

```bash
  CREATE DATABASE image_data;
```

Utilize o arquivo `db.sql` contido dentro da pasta `database` para criar a tabela de dados

No arquivo `send_initial_db` adicione suas credencias do banco de dados Postgress


## Documentação

### Classificação com Gemini, Llama e PaliGemma

Foi utilizado a API do Google CLoud plataform com o pacote `google-cloud-aiplatform` e `vertexai` para realizar chamadas aos modelos `Gemini 2.0 Flash`, `Llama 3.2 Vision` e `PaliGemma 2` rodando em um projeto no GCP.

Antes de executar os arquivos é necessário ter os modelos rodando e com api exposta no GCP, atente-se também as configurações dos arquivo:

- Insira as credenciais do seu banco de dados
- Insira as credenciais relevantes para o progeto no GCP, como endpoint, region, project_id e url

Execute o arquivo:

```bash
  python gemini.py
```

ou

```bash
  python llama.py
```

ou

```bash
  python pali_gemma.py
```

A execução pode demorar algumas horas, aguarde a mensagem de finalização do script.

### Métricas

Foram utilizadas as bibliotecas `sklearn` para cálculo das métricas, e a biblioteca `mlxtend` para plotagem da matriz de confusão

Antes de executar o arquivo `metrics.py`, atente-se as configurações do arquivo:

- Insira as credenciais do seu banco de dados
- Altere o modelo e estratégia de prompt calculada conforme desejado

Execute o arquivo `metrics.py`:

```bash
  python metrics.py
```
