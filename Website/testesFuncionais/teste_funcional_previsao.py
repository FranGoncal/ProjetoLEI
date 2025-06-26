from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--log-level=3")
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=chrome_options)

#Abrir a pagina do site
driver.get("http://localhost:5000/prever")
#driver.get("http://churn-predictor.com/prever")

# Esperar que a pagina carregue
time.sleep(2)

# Preencher o campo tenure
driver.find_element(By.ID, "tenure").send_keys("12")

# Selecionar o servico de internet
internet_select = Select(driver.find_element(By.ID, "internetService"))
internet_select.select_by_value("fiber_optic")

# Ativar switch de dependentes
driver.find_element(By.ID, "idTestdependents").click()

# Ativar segurança online
driver.find_element(By.ID, "idTestonlineSecurity").click()

# Ativar suporte tecnico
driver.find_element(By.ID, "idTesttechSupport").click()

# Selecionar tipo de contrato
contract_select = Select(driver.find_element(By.ID, "contract"))
contract_select.select_by_value("two_year")

# Ativar faturacao eletronica
driver.find_element(By.ID, "idTestpaperlessBilling").click()

# Selecionar metodo de pagamento
payment_select = Select(driver.find_element(By.ID, "paymentMethod"))
payment_select.select_by_value("credit_card")

# Preencher mensalidade
driver.find_element(By.ID, "monthlyCharges").send_keys("89.99")

# Selecionar modelo de previsao
modelo_select = Select(driver.find_element(By.ID, "modeloEscolhido"))
modelo_select.select_by_value("rf")

# Submeter o formulário
driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

# Aguardar página de resultado
time.sleep(3)

# Validar se a submissão correu bem
if "previsão" in driver.page_source.lower():
    print("[SUCESSO] Teste funcional correu com sucesso!")
else:
    print("[ERRO] A previsão não foi encontrada na página de resposta.")

# Fechar o browser
driver.quit()
