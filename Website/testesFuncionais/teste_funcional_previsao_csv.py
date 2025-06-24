from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import time
import os

''' Descrição do teste:
        Este teste funcional verifica se o upload de um CSV na página /prever-csv funciona corretamente.
        Espera-se que, o primeiro csv mal formatado mostre uma mensagem de erro
        após submeter o CSV que corresponde a estrutura do template, a aplicação deve permitir o download dos resultados.'''

def testar_csv(csv_filename, mensagem_esperada):
    chrome_options = Options()
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

    csv_path = os.path.abspath(csv_filename)
    driver = webdriver.Chrome(options=chrome_options)

    
    driver.get("http://localhost:5000/prever-csv")
    time.sleep(2)

    file_input = driver.find_element(By.NAME, "csvfile")
    file_input.send_keys(csv_path)
    time.sleep(1)

    modelo_select = Select(driver.find_element(By.ID, "modeloEscolhido"))
    modelo_select.select_by_value("rf")

    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(4)

    page_source = driver.page_source.lower()
    if mensagem_esperada.lower() in page_source:
        print(f"[SUCESSO] Mensagem esperada encontrada para o ficheiro {csv_filename}: '{mensagem_esperada}'")
    else:
        print(f"[ERRO] Mensagem esperada NÃO encontrada para o ficheiro {csv_filename}.")

    driver.quit()

if __name__ == "__main__":

    testar_csv("csv_mal_estruturado.csv", "Erro ao processar o ficheiro CSV. Consulte o template disponivel nesta página.")
    
    testar_csv("template.csv", "download")