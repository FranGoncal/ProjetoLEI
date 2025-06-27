<p align="center">
  <img src="Website/static/icon_web_white.png" alt="Gráfico de churn" width="500"/>
</p>


# Descrição do Projeto:

  No âmbito da unidade curricular de Projeto II, estão disponíveis os ficheiros .ipynb utilizados durante o desenvolvimento do projeto, os datasets selecionados e todos os ficheiros relacionados com o desenvolvimento da aplicação web e PWA dentro da pasta /Website.
  Este projeto foi desenvolvido com o intuito de criar um modelo de previsão de abandono de um serviço (customer churn) de telecomunicações utilizando algoritmos de Machine Learning.
  Sendo este conceito, posto em demonstração de forma acessivel, a partir da aplicação web e PWA criadas.
  A aplicação está disponivel a partir da seguinte hiperligação: *site*

# Estrutura do Repositório:

  - /Website : Esta pasta contém todos os ficheiros relacionados com a implementação da aplicação web e PWA.
  - /data : Esta pasta contém os datasets utilizados.
  - ibm_only.ipynb : Ficheiro que contem todo o código, gráficos e resultados apresentados no relatório do projeto nos capítulos 5 e 6 relativamente ao dataset da IBM.
  - kaggle_only.ipynb : Ficheiro que contem todo o código, gráficos e resultados apresentados no relatório do projeto nos capítulos 5 e 6 relativamente ao dataset do Kaggle.
  - validacao_independente.ipynb : Ficheiro que contem todo o código e resultados apresentados no relatório do projeto no capítulo 7.
  - validacao_independente_undersampling.ipynb :  Ficheiro que contem todo o código e resultados apresentados no relatório do projeto no capítulo 7 utilizando undersampling.

# Resultados de Validação Cruzada (Com Otimização de Hiperparâmetros)

  Os resultados previsivos dos modelos treinados no estudo presente neste repositório, estão presentes na tabela abaixo. 
  Tendo sido estes os modelos exportados para a aplicação web desenvolvida. 

| Algoritmo | Precision     | Accuracy      | Recall         | F1-Score       | AUC            |
|:----------|:---------------|:--------------|:---------------|:---------------|:---------------|
| RF        | **85.2% ±1%**  | **86.2% ±1%** | **89.2% ±2%**  | **86.2% ±1%**  | **93.1% ±1%**  |
| SVM       | 81.1% ±2%      | 80.4% ±2%     | 80.4% ±2%      | 80.3% ±2%      | 86.2% ±2%      |
| XGBoost   | 84.7% ±3%      | 84.5% ±3%     | 84.5% ±3%      | 84.4% ±3%      | 91.9% ±3%      |
| DT        | 80.5% ±3%      | 80.2% ±2%     | 80.2% ±2%      | 80.1% ±2%      | 86.5% ±2%      |
| LR        | 79.3% ±2%      | 79.2% ±1%     | 79.2% ±1%      | 79.2% ±1%      | 87.3% ±1%      |
| NB        | 79.3% ±2%      | 79.2% ±1%     | 79.2% ±1%      | 79.2% ±1%      | 87.3% ±1%      |
