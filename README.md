# Sistema de Auxílio à Tomada de Decisões para Investimento em Criptoativos

## Descrição do Projeto

Este projeto é um sistema completo de auxílio à tomada de decisões para investimentos em criptoativos. Ele utiliza modelos preditivos para analisar o histórico de preços de criptomoedas, como Bitcoin (BTC) e Ethereum (ETH), indicando os melhores momentos para compra ou venda. O sistema é composto por:

- **Coleta automatizada de dados**: Scripts que coletam dados históricos e atuais das criptomoedas.
- **Retreinamento periódico dos modelos**: Pipeline que atualiza os modelos preditivos com os novos dados.
- **API para previsões**: Uma API construída com FastAPI que fornece previsões baseadas nos modelos.
- **Dashboard interativo**: Interface visual construída com Streamlit para interação com o usuário.

## Índice

- [Estrutura do Projeto](#estrutura-do-projeto)
- [Termos Técnicos Utilizados](#termos-técnicos-utilizados)
- [Instalação](#instalação)
- [Execução com Docker](#execução-com-docker)
- [Execução sem Docker](#execução-sem-docker)
- [Testando a Previsão](#testando-a-previsão)
- [Explicação sobre a Dockerização](#explicação-sobre-a-dockerização)
- [Considerações Finais](#considerações-finais)

## Estrutura do Projeto

- **src/**
  - **api/**
    - **collect_data.py**: Script para coletar dados históricos de preços das criptomoedas.
    - **schedule_data_collection.py**: Agendamento da coleta automatizada de dados usando o módulo `schedule`.
    - **train_pipeline.py**: Pipeline para retreinamento dos modelos com novos dados coletados.
    - **main.py**: API construída com FastAPI para realizar previsões e sugerir ações de compra ou venda.
    - **dashboard.py**: Dashboard interativo construído com Streamlit para visualização das previsões.
    - **models/**
      - **modelos/**
        - **best_random_forest_model_retrained.pkl**: Modelo treinado para previsões.
    - **Dockerfile.api**: Dockerfile para a API.
    - **Dockerfile.dashboard**: Dockerfile para o dashboard.
    - **Dockerfile.schedule**: Dockerfile para o agendamento de coleta de dados.
- **docker-compose.yml**: Arquivo para orquestração dos containers Docker.
- **requirements.txt**: Arquivo com as dependências do projeto.

## Termos Técnicos Utilizados

- **SMA (Simple Moving Average)**: Média Móvel Simples, uma média aritmética dos preços de fechamento dos últimos `n` dias, utilizada para suavizar flutuações de preços e identificar tendências.
- **RSI (Relative Strength Index)**: Índice de Força Relativa, um indicador que mede a velocidade e a mudança dos movimentos de preços, indicando condições de sobrecompra ou sobrevenda.
- **Volume**: Quantidade total de uma criptomoeda negociada em um período específico.

## Instalação

### Pré-requisitos

- [Docker](https://www.docker.com/get-started) instalado no sistema.
- [Docker Compose](https://docs.docker.com/compose/install/) instalado.
- [WSL](https://learn.microsoft.com/pt-br/windows/wsl/install) instalado.
- Caso não utilize Docker, é necessário ter o Python 3.8 ou superior instalado.

### Clonando o Repositório

```bash
git clone <URL_DO_REPOSITORIO>
cd seu_projeto_crypto
```

## Execução com Docker

### Passo 1: Construir e Iniciar os Containers

No diretório raiz do projeto, execute o seguinte comando para construir as imagens e iniciar os containers:

```bash
docker-compose up --build
```

Este comando irá:
   - Construir as imagens Docker para cada serviço (API, Dashboard e Scheduler).
   - Iniciar os containers e orquestrá-los usando o Docker Compose.

### Passo 2: Acessar os Serviços

- Dashboard: Acesse o dashboard no navegador em http://localhost:8501.
- API: A API estará disponível em http://localhost:5000.
  - A documentação interativa da API (Swagger UI) pode ser acessada em http://localhost:5000/docs.

### Observação

- O serviço de agendamento (schedule) irá executar a coleta de dados periodicamente em segundo plano.

## Execução sem Docker

Caso prefira ou tenha problemas com o Docker, é possível executar o projeto manualmente.

### Passo 1: Criar e Ativar o Ambiente Virtual

```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

### Passo 2: Instalar as Dependências

```bash
pip install -r requirements.txt
```

### Passo 3: Executar a Coleta de Dados

Em um terminal, execute:

```bash
python src/api/schedule_data_collection.py
```

Este script irá iniciar a coleta de dados automatizada. Se preferir executar uma única coleta de dados, pode executar:

```bash
python src/api/collect_data.py
```

### Passo 4: Retreinar os Modelos

Após coletar os dados, execute:

```bash
python src/api/train_pipeline.py
```

### Passo 5: Iniciar a API

Em um terminal separado, execute:

```bash
uvicorn src.api.main:app --reload
```

### Passo 6: Iniciar o Dashboard
Em outro terminal, execute:

```bash
streamlit run src/api/dashboard.py
```

### Observação

Certifique-se de que a API está em execução antes de iniciar o dashboard, pois o dashboard faz requisições à API para obter as previsões.

## Testando a Previsão

1. Acesse o dashboard em http://localhost:8501.
2. Selecione o ativo (BTC ou ETH).
3. Insira os valores para SMA 20 Dias, RSI e Volume. Exemplo:
   - SMA 20 Dias: 32000
   - RSI: 45
   - Volume: 2000
4. Clique em "Prever".
5. Veja a previsão e a ação sugerida (Compra ou Venda) baseada nos modelos preditivos.

## Vídeo de Teste

- [Link para vídeo](https://drive.google.com/file/d/1W2A_Yc1dWItXhr49FMcIWojWxf0-N-Mx/view?usp=drivesdk)

## Explicação sobre a Dockerização

### Por que Dockerizamos as 3 Partes?
- Isolamento de Ambientes: Cada componente (API, Dashboard e Scheduler) roda em seu próprio container, garantindo que as dependências e configurações não conflitem entre si.
- Portabilidade: O Docker permite que o projeto seja executado em qualquer sistema que tenha o Docker instalado, sem a necessidade de configurar ambientes específicos.
- Escalabilidade: Com os containers separados, é possível escalar individualmente cada componente conforme a necessidade (por exemplo, múltiplas instâncias da API para lidar com mais requisições).
- Facilidade de Implantação: Com o Docker Compose, é simples orquestrar e gerenciar todos os serviços do projeto com um único comando.

### Componentes Dockerizados

- API: Contém o serviço FastAPI que fornece previsões através de endpoints REST.
- Dashboard: Executa o aplicativo Streamlit que oferece uma interface amigável para interação com o usuário.
- Scheduler: Responsável pela coleta automática de dados e retreinamento dos modelos em intervalos regulares.

## Considerações Finais

- Automatização: O projeto utiliza agendamento de tarefas para coleta de dados e retreinamento dos modelos, garantindo que os modelos estejam sempre atualizados e precisos.
- Modularidade: A separação em containers distintos para cada componente facilita a manutenção e a escalabilidade do sistema.
- Documentação: Este README serve como guia completo para instalação, configuração e execução do sistema, tanto com Docker quanto sem ele.
