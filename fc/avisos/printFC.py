from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Inicializa o driver do Chrome automaticamente
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Abre a URL desejada
driver.get('https://nitter.net/search?f=tweets&q=FogoCruzadoRJ')

# Aguarda um tempo para garantir que a página carregue
time.sleep(5)  # Aguarda 5 segundos (ajuste conforme necessário)

# Define o zoom para 75%
driver.execute_script("document.body.style.zoom='75%'")

# Aguarda um tempo para aplicar o zoom
time.sleep(5)  # Aguarda 2 segundos para garantir que o zoom seja aplicado

# Tira um print da tela
driver.save_screenshot('screenshot.png')

# Fecha o navegador
driver.quit()
