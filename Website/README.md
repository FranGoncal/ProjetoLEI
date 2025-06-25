<p align="center">
  <img src="Website/static/icon_web_white.png" alt="Gráfico de churn" width="500"/>
</p>


# Website:

  Esta pasta contém todos os ficheiros utilizados na implementação e desenvolvimento de uma aplicação web e PWA.
  O website foi implementado num ambiente cloud Azure, não necessitando de ser alojado numa infraestrutura física própria. Podendo ser acedido através da hiperligação:

# Implementação:

  De modo a fazer a implementação da aplicação web e PWA aqui presentes, tal como foi mencionado será necessário definir uma infraestrutura cloud Azure, para isso poderá fazer uso do ficheiro main.tf que criará um grupo de recursos, um Container Registry e ainda a Base de Dados CosmosDB.
  Após a criação destas, basta dar deploy manual do container através dos seguintes comandos:
  > **Nota:** Este projeto conta com um ficheiro .env na seguinte diretoria o qual possui as seguintes chaves "COSMOS_KEY", "SECRET_KEY", "RECAPTCHA_SECRET", sendo a COSMOS_KEY a chave secreta da CosmosDB, a SECRET_KEY uma chave definida secreta aleatoriamente utilizada pelo Flask e a RECAPTCHA_SECRET a chave privada do RECAPTCHA necessitando esta de ser definida para um dominio especifico em https://cloud.google.com/security/products/recaptcha, as páginas do frontend em /templates também necessitarão da atualização da chave pública nova para o domínio atualizado.
  > No caso de alteração do nome da conta da CosmosDB, da Base de dados ou do container, as alterações terão de ser também feitas no ficheiro app.py. 

    docker login <ContainerRegistryLoginServer>
    
    docker build -t churn_pred .
    
    docker tag churn_pred <ContainerRegistryLoginServer>/webapp:1.0
  
    docker push <ContainerRegistryLoginServer>/webapp:1.0

  Após um deploy bem sucedido basta criar um recurso App Service na plataforma Azure e associar o container do Container Registry mencionado. 
  Caso Possua um nome de dominio próprio, após os passos mencionados basta adicioná-lo em Custom domains dentro do App Service.

  Ao seguir os passos descritos a aplicação web deveria estar disponivel no seu nome de dominio. 
  
# Testes:

  Este repositório possui testes unitários e testes funcionais. É importante referir que de forma a testar as funcionalidades que possuem um captcha de forma automatizada, foi utilizado um ficheiro app_teste.py, o qual tem o mesmo funcionamento que app.py mas com a verificação de RECAPTCHA e comunicação com o CosmosDB removidas, de modo a testar exatamente o mesmo código mas de forma local e automatizada.

  - Testes Unitários:
    Basta correr o seguinte comando na diretoria Website:

        pytest
  - Testes Funcionais:
    Os testes funcionais estão definidos para serem testados utilizando o Chrome, de modo a fazer o seu teste, basta correr cada um dos scripts .py e avaliar o resultado das ações do script comparativamente com o resultado previsto.
    
