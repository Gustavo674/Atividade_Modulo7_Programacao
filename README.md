# Atividade_Modulo7_Programacao

# Sistema de Auxílio à Tomada de Decisões para Investimento em Criptoativos

## Descrição da Atividade
Este projeto é um sistema de auxílio à tomada de decisões para investimento em criptoativos. Ele utiliza modelos preditivos para analisar o histórico de preços de criptomoedas, como Bitcoin (BTC) e Ethereum (ETH), e indicar o melhor momento para compra ou venda. O sistema inclui coleta automatizada de dados, retreinamento periódico dos modelos, uma API para previsões e um dashboard interativo.

## Estrutura do Projeto
- **collect_data.py**: Script para coletar dados históricos de preços das criptomoedas.
- **schedule_data_collection.py**: Agendamento da coleta automatizada de dados usando o módulo `schedule`.
- **train_pipeline.py**: Pipeline para retreinamento dos modelos com novos dados coletados.
- **main.py**: API construída com FastAPI para realizar previsões e sugerir ações de compra ou venda.
- **dashboard.py**: Dashboard interativo construído com Streamlit para visualização das previsões.
- **models**: Diretório contendo os modelos treinados.

## Termos Técnicos Utilizados
- **SMA (Simple Moving Average)**: Média Móvel Simples, uma média aritmética dos preços de fechamento dos últimos `n` dias, utilizada para suavizar flutuações de preços e identificar tendências.
- **RSI (Relative Strength Index)**: Índice de Força Relativa, um indicador de momento que mede a velocidade e a mudança dos movimentos de preços, indicando condições de sobrecompra ou sobrevenda.
- **Volume**: Quantidade total de uma criptomoeda negociada em um período específico.

## Instalação
1. Clone o repositório:
   ```bash
   git clone <URL_DO_REPOSITORIO>
   cd seu_projeto_crypto

2. Crie um ambiente virtual e ative-o:
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt

## Coleta de Dados
Antes de executar os modelos, é necessário coletar os dados históricos das criptomoedas. Execute o script `schedule_data_collection.py` para iniciar a coleta de dados automatizada:
  ```bash
  python src/api/schedule_data_collection.py
  ```
## Retreinamento dos Modelos
Após coletar os dados, execute o pipeline de retreinamento para atualizar os modelos com os novos dados coletados:
  ```bash
  python src/api/train_pipeline.py
  ```
## Execução da API
Em um terminal, inicie a API FastAPI para permitir que o sistema faça previsões:
  ```bash
  uvicorn src.api.main:app --reload
  ```

## Execução do Dashboard
Em outro terminal, inicie o dashboard interativo para visualizar as previsões:
  ```bash
  streamlit run src/api/dashboard.py
  ```

## Exemplos de Testes

### Testando a Previsão
1. Acesse o dashboard em [http://localhost:8501](http://localhost:8501).
2. Selecione o ativo (BTC ou ETH).
3. Insira os valores para SMA 20 Dias, RSI e Volume. Exemplo:
   - **SMA 20 Dias**: 32000
   - **RSI**: 45
   - **Volume**: 2000
4. Clique em "Prever".

### Resultados Esperados
- **Previsão**: O valor predito para o próximo movimento do preço da criptomoeda.
- **Ação Sugerida**: Indicação de "Compra" se o preço previsto for maior que o atual (SMA 20), ou "Venda" caso contrário.

## Estrutura do Código e Funcionalidades Principais

- **Coleta de Dados**: O script `collect_data.py` coleta dados históricos de preços das criptomoedas usando a API do Yahoo Finance. Os dados são salvos em arquivos CSV para uso posterior no treinamento do modelo.
- **Retreinamento dos Modelos**: O `train_pipeline.py` realiza o retreinamento dos modelos periodicamente usando os novos dados coletados. O pipeline é automatizado com Prefect para fácil configuração de fluxos de trabalho.
- **API e Dashboard**: A API FastAPI (`main.py`) oferece endpoints para previsões, e o dashboard Streamlit (`dashboard.py`) fornece uma interface visual para o usuário interagir com as previsões.

## Considerações Finais

- **Automatização**: O projeto utiliza agendamento de tarefas para coleta de dados e retreinamento dos modelos, garantindo que os modelos estejam sempre atualizados.
- **Documentação**: Toda a estrutura de código está documentada com comentários e este README serve como guia completo para instalação, configuração e execução do sistema.
