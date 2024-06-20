from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Lista de números de telefone
phone_numbers = [
    "+55 11 991668852"
]

# Mensagem a ser enviada
message = "Olá, esta é uma mensagem automatizada."

# Configurar o serviço do ChromeDriver
service = Service(executable_path='/Users/bruna/Downloads/chromedriver-mac-arm64/chromedriver')  # Altere para o caminho correto do seu ChromeDriver

# Iniciar o navegador
driver = webdriver.Chrome(service=service)
driver.get("https://web.whatsapp.com")

# Esperar o usuário escanear o código QR
input("Pressione Enter após escanear o código QR e o WhatsApp Web estiver carregado completamente.")

for number in phone_numbers:
    # Construir o URL corretamente
    url = f"https://web.whatsapp.com/send?phone={number.replace(' ', '').replace('+', '')}&text={message}"
    driver.get(url)
    try:
        # Aguardar até que o campo de mensagem esteja presente
        message_box = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[@title='Type a message' or @contenteditable='true']"))
        )
        time.sleep(3)  # Tempo adicional para garantir que a página carregue completamente
        
        # Simular pressionamento da tecla Enter
        message_box.send_keys(Keys.ENTER)
        time.sleep(5)  # Tempo para garantir que a mensagem foi enviada
    except Exception as e:
        print(f"Não foi possível enviar mensagem para {number}: {e}")

driver.quit()
