from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Lista de números de telefone
phone_numbers = [
    "+55 11 94147-6605", "+55 11 94396-3629", "+55 11 94680-0026", "+55 11 94836-2923",
    "+55 11 94836-3315", "+55 11 94836-9256", "+55 11 94861-2599", "+55 11 96575-8266",
    "+55 11 96734-2242", "+55 11 96853-5740", "+55 11 96916-0771", "+55 11 97413-6789",
    "+55 11 97701-7915", "+55 11 97959-3331", "+55 11 98291-3355", "+55 11 98441-4500",
    "+55 11 98621-5666", "+55 11 99473-2170", "+55 11 99818-1950", "+55 13 97414-1346",
    "+55 15 99116-7730", "+55 16 99773-3222", "+55 17 99219-9090", "+55 18 99624-0556",
    "+55 19 98970-8931", "+55 21 96445-9793", "+55 21 97108-9021", "+55 21 97162-1297",
    "+55 21 98583-6775", "+55 21 99478-5822", "+55 22 99737-4150", "+55 22 99826-5359",
    "+55 24 99876-0009", "+55 28 99882-9926", "+55 62 8104-6876", "+55 81 9358-8455",
    "+55 81 9437-2435"
]

# Mensagem a ser enviada
message = "Olá, encontrei seu número em um grupo criado para dar golpes. Talvez você seja solicitado a fazer algum depósito sob a promessa de receber uma grana por um trabalho. NÃO FAÇA ESSE DEPÓSITO!"

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
        # Aguardar até que o botão de envio esteja presente
        send_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='compose-btn-send']"))
        )
        send_button.click()
        time.sleep(5)  # Tempo para garantir que a mensagem foi enviada
    except Exception as e:
        print(f"Não foi possível enviar mensagem para {number}: {e}")

driver.quit()
