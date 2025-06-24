from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import time
import os

# Configurar opções do Chrome
chrome_options = Options()
chrome_options.add_argument("--log-level=3")
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

# Caminho absoluto para o ficheiro CSV de teste
csv_path = os.path.abspath("template.csv")
#csv_path = os.path.abspath("csv_mal_estruturado.csv")

# Inicializar driver
driver = webdriver.Chrome(options=chrome_options)

driver.get("http://localhost:5000/prever-csv")
time.sleep(2)

file_input = driver.find_element(By.NAME, "csvfile")
file_input.send_keys(csv_path)
time.sleep(1)

modelo_select = Select(driver.find_element(By.ID, "modeloEscolhido"))
modelo_select.select_by_value("rf")

driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

# Esperar resposta (ajusta o tempo se necessário)
time.sleep(4)

# Verificar se a previsão foi processada corretamente
if "previsão" in driver.page_source.lower() or "download" in driver.page_source.lower():
    print("[SUCESSO] Teste funcional de previsão CSV correu com sucesso! 🎉")
else:
    print("[ERRO] A previsão CSV não foi encontrada na página de resposta.")


driver.quit()
