from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
from selenium.webdriver.chrome.options import Options
import os

# Configurar opções do Chrome
chrome_options = Options()
chrome_options.add_argument("--log-level=3")
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

# Caminho para o teu driver
driver = webdriver.Chrome(options=chrome_options)

# Abrir a página local (ajusta a porta se necessário)
driver.get("http://localhost:5000/prever")
#driver.get("http://churn-predictor.com/prever")

# Aguarda a página carregar (opcional)
time.sleep(2)

# Preencher o campo 'Tempo de permanência no serviço (meses)'
driver.find_element(By.ID, "tenure").send_keys("12")

# Selecionar o serviço de internet
internet_select = Select(driver.find_element(By.ID, "internetService"))
internet_select.select_by_value("fiber_optic")

# Ativar switch de dependentes
driver.find_element(By.ID, "idTestdependents").click()

# Ativar segurança online
driver.find_element(By.ID, "idTestonlineSecurity").click()

# Ativar suporte técnico
driver.find_element(By.ID, "idTesttechSupport").click()

# Selecionar tipo de contrato
contract_select = Select(driver.find_element(By.ID, "contract"))
contract_select.select_by_value("two_year")

# Ativar faturação eletrónica
driver.find_element(By.ID, "idTestpaperlessBilling").click()

# Selecionar método de pagamento
payment_select = Select(driver.find_element(By.ID, "paymentMethod"))
payment_select.select_by_value("credit_card")

# Preencher mensalidade
driver.find_element(By.ID, "monthlyCharges").send_keys("89.99")

# Selecionar modelo de previsão
modelo_select = Select(driver.find_element(By.ID, "modeloEscolhido"))
modelo_select.select_by_value("rf")

# Submeter o formulário
driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

# Opcional: aguardar página de resultado
time.sleep(3)

# Validar se a submissão correu bem (ajustar para o conteúdo da tua resposta)
if "previsão" in driver.page_source.lower():
    print("[SUCESSO] Teste funcional correu com sucesso!")
else:
    print("[ERRO] A previsão não foi encontrada na página de resposta.")

# Fechar o browser
driver.quit()
