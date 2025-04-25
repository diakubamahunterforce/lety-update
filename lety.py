from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import threading
import time

app = Flask(__name__)

# Sessão global para navegador
class BrowserSession:
    driver = None

session = BrowserSession()

# Iniciar o Navegador e Abrir o YouTube
@app.route('/start', methods=['POST'])
def start_browser():
    def run_browser():
        options = webdriver.ChromeOptions()
        options.binary_location = "/usr/bin/chromium-browser"  # Caminho para o Chromium
        options.add_argument("--start-maximized")
        # Ativar o modo headless se não precisar de interface gráfica
        # options.add_argument("--headless")

        session.driver = webdriver.Chrome(options=options)
        session.driver.get("https://www.youtube.com")

    thread = threading.Thread(target=run_browser)
    thread.start()
    return jsonify({"status": "success", "message": "Navegador iniciado."})

# Enviar Comando
@app.route('/command', methods=['POST'])
def command():
    if not session.driver:
        return jsonify({"status": "error", "message": "Navegador não iniciado. Use /start."})

    data = request.get_json()
    action = data.get("action")
    query = data.get("query")

    driver = session.driver

    try:
        if action == "search":
            if not query:
                return jsonify({"status": "error", "message": "Query é necessária para o comando 'search'."})
            
            # Aguarda o carregamento e faz a busca
            time.sleep(2)
            search_input = driver.find_element(By.NAME, "search_query")
            search_input.clear()
            search_input.send_keys(query)
            search_input.send_keys(Keys.ENTER)
            time.sleep(3)
            # Clica no primeiro vídeo
            video = driver.find_element(By.ID, "video-title")
            video.click()

        elif action == "play" or action == "pause":
            body = driver.find_element(By.TAG_NAME, 'body')
            body.send_keys('k')  # k = play/pause

        elif action == "volume_up":
            body = driver.find_element(By.TAG_NAME, 'body')
            body.send_keys(Keys.ARROW_UP)

        elif action == "volume_down":
            body = driver.find_element(By.TAG_NAME, 'body')
            body.send_keys(Keys.ARROW_DOWN)

        else:
            return jsonify({"status": "error", "message": "Comando desconhecido."})

        return jsonify({"status": "success", "command_executed": action})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# Fechar o Navegador
@app.route('/close', methods=['POST'])
def close_browser():
    if session.driver:
        session.driver.quit()
        session.driver = None
        return jsonify({"status": "success", "message": "Navegador fechado."})
    return jsonify({"status": "error", "message": "Navegador não estava aberto."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False) 