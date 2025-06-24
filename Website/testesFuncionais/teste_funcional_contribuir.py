from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# Configurar opções para suprimir logs do Chrome
chrome_options = Options()
chrome_options.add_argument("--log-level=3")
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

driver = webdriver.Chrome(options=chrome_options)

driver.get("http://localhost:5000/contribuir")
time.sleep(2)

driver.find_element(By.ID, "name").send_keys("André Nunes")
driver.find_element(By.ID, "ccnif").send_keys("123456789")

# Checkbox dependentes
dependents_checkbox = driver.find_element(By.ID, "idDependentsSwitch")
if not dependents_checkbox.is_selected():
    dependents_checkbox.click()

driver.find_element(By.ID, "tenure").send_keys("24")

# Seleção serviço internet
internet_service = driver.find_element(By.ID, "internetService")
for option in internet_service.find_elements(By.TAG_NAME, 'option'):
    if option.get_attribute("value") == "fiber_optic":
        option.click()
        break

# Checkboxes onlineSecurity, techSupport, paperlessBilling
for checkbox_id in ["idOnlineSecuritySwitch", "idTechSupportSwitch", "idPaperlessBillingSwitch"]:
    checkbox = driver.find_element(By.ID, checkbox_id)
    if not checkbox.is_selected():
        checkbox.click()

# Tipo contrato
contract_select = driver.find_element(By.ID, "contract")
for option in contract_select.find_elements(By.TAG_NAME, 'option'):
    if option.get_attribute("value") == "two_year":
        option.click()
        break

# Método pagamento
payment_select = driver.find_element(By.ID, "paymentMethod")
for option in payment_select.find_elements(By.TAG_NAME, 'option'):
    if option.get_attribute("value") == "credit_card":
        option.click()
        break

driver.find_element(By.ID, "monthlyCharges").send_keys("89.99")

# Checkbox churn (abandono serviço)
churn_checkbox = driver.find_element(By.ID, "idChurngSwitch")
if not churn_checkbox.is_selected():
    churn_checkbox.click()

# Espera para o JS mostrar os campos opcionais
time.sleep(1)

# Preencher campos opcionais visíveis após ativar churn
motivo = driver.find_element(By.ID, "motivo")
motivo.send_keys("Mudança de operadora pela melhor oferta.")

contramedida = driver.find_element(By.ID, "contramedida")
contramedida.send_keys("Ofertas mais competitivas poderiam ter evitado a saída.")

pais = driver.find_element(By.ID, "pais")
pais.send_keys("Portugal")

print("[INFO] A submeter o formulário...")
driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

# Espera resposta depois de submeter
time.sleep(3)

# Verificação de confirmação na página
page_source = driver.page_source.lower()
if "obrigado" in page_source or "sucesso" in page_source or "recebido" in page_source:
    print("[SUCESSO] Formulário submetido com sucesso!")
else:
    print("[AVISO] Não consegui confirmar a submissão com mensagem clara na página.")


driver.quit()
