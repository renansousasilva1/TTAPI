import json, os, time, io, re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv
from django.http import JsonResponse
from django.views import View
from .models import TweetData, TweetDataPenhaRJ, TweetDataPonteRJ, TweetDataCOR, TweetDataVOZ, TweetDataTREM, TweetDataPMERJ, TweetDataCAZETV  # Importando o modelo TweetData

# Carregar variáveis de ambiente
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")



def listar_tweets(request):
    """Retorna os tweets salvos no banco de dados em formato JSON."""
    tweets = list(TweetData.objects.all().order_by('-id').values())  # Ordena do mais recente para o mais antigo
    return JsonResponse({"tweets": tweets}, safe=False)

def listar_tweets_penharj(request):
    """Retorna os tweets da model TweetDataPenhaRJ em formato JSON."""
    tweets = list(TweetDataPenhaRJ.objects.all().order_by('-id').values())
    return JsonResponse({"tweets": tweets}, safe=False)

def listar_tweets_ponterj(request):
    """Retorna os tweets da model TweetDataPonteRJ em formato JSON."""
    tweets = list(TweetDataPonteRJ.objects.all().order_by('-id').values())
    return JsonResponse({"tweets": tweets}, safe=False)


def listar_tweets_COR(request):
    """Retorna os tweets da model TweetDataCOR em formato JSON."""
    tweets = list(TweetDataCOR.objects.all().order_by('-id').values())
    return JsonResponse({"tweets": tweets}, safe=False)


def listar_tweets_VOZ(request):
    """Retorna os tweets da model TweetDataCOR em formato JSON."""
    tweets = list(TweetDataVOZ.objects.all().order_by('-id').values())
    return JsonResponse({"tweets": tweets}, safe=False)


def listar_tweets_TREM(request):
    """Retorna os tweets da model TweetDataTREM em formato JSON."""
    tweets = list(TweetDataTREM.objects.all().order_by('-id').values())
    return JsonResponse({"tweets": tweets}, safe=False)


def listar_tweets_PMERJ(request):
    """Retorna os tweets da model TweetDataPMERJ em formato JSON."""
    tweets = list(TweetDataPMERJ.objects.all().order_by('-id').values())
    return JsonResponse({"tweets": tweets}, safe=False)


def listar_tweets_cazetv(request):
    """Retorna os tweets da model TweetDataPMERJ em formato JSON."""
    tweets = list(TweetDataCAZETV.objects.all().order_by('-id').values())
    return JsonResponse({"tweets": tweets}, safe=False)






def upload_to_gemini(image_bytes, mime_type="image/png"):
    """Faz o upload da imagem para o Gemini e retorna a URI."""
    try:
        file = genai.upload_file(image_bytes, mime_type=mime_type)
        return file
    except Exception as e:
        print(f"Erro ao fazer upload da imagem: {e}")
        return None


def processar_imagem(image_path):
    """Processa a imagem recebida como input."""
    try:
        image = Image.open(image_path)
        return image
    except Exception as e:
        print(f"Erro ao processar a imagem: {e}")
        return None


class ProcessNitterViewCAZETV(View):
    def get(self, request):
        try:
            # Configurar Selenium para capturar o screenshot
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
            driver.get('https://nitter.net/CazeTVOficial')
            time.sleep(5)  # Aguarda a página carregar
            driver.execute_script("document.body.style.zoom='33%'")  # Ajusta o zoom para capturar a tela toda
            time.sleep(5)  # Aguarda o zoom ser aplicado
            screenshot_path = 'screenshotCAZE.png'
            driver.save_screenshot(screenshot_path)  # Salva a captura da tela
            driver.quit()  # Fecha o navegador

            # Chama a função para processar a imagem e obter os dados do Gemini
            self.process_image_with_gemini(screenshot_path)

            # Retorna uma mensagem de sucesso
            return JsonResponse({"message": "Screenshot capturado com sucesso!"})

        except Exception as e:
            return JsonResponse({"error": f"Ocorreu um erro: {str(e)}"}, status=500)

    def process_image_with_gemini(self, image_path):
        """Processa a imagem com Gemini."""
        # Abrir imagem com PIL
        image = processar_imagem(image_path)
        if image:
            # Converter imagem para bytes para upload
            image_bytes = io.BytesIO()
            image.save(image_bytes, format="PNG")
            image_bytes.seek(0)

            # Fazer upload para Gemini
            file = upload_to_gemini(image_bytes)

            if file:
                try:
                    # Criar a sessão de chat
                    chat_session = model.start_chat(history=[{"role": "user", "parts": [file]}])

                    # Enviar o prompt para o modelo
                    prompt = (
                        "Transcreva a imagem do screenshot anexada. Foque em transcrever somente os tweets exibidos. "
                        "Formate o texto de cada tweet em algo com uma formatação parecida com um arquivo JSON. "
                        "Foque em pegar somente os seguintes dados que vou te falar agora: "
                        "author, username, timestamp, text, retweeted_by, replies, retweets, likes."
                    )
                    response = chat_session.send_message(prompt)
                    
                    # Verifique se a IA retornou algum texto
                    if response.text.strip():
                        # Limpar delimitadores Markdown da resposta
                        limpa_resposta = re.sub(r"```json|```", "", response.text.strip()).strip()

                        try:
                            response_data = json.loads(limpa_resposta)

                            # Armazenar dados da IA na model TweetData
                            for tweet in response_data:
                                TweetDataCAZETV.objects.create(
                                    author=tweet.get('author'),
                                    username=tweet.get('username'),
                                    timestamp=tweet.get('timestamp'),
                                    text=tweet.get('text'),
                                    retweeted_by=tweet.get('retweeted_by'),
                                    replies=tweet.get('replies', 0),
                                    retweets=tweet.get('retweets', 0),
                                    likes=tweet.get('likes', 0)
                                )

                            # Exibir os dados formatados como JSON
                            print("Dados da IA em Formato JSON:", response_data)

                        except json.JSONDecodeError as e:
                            print(f"Erro ao decodificar o JSON retornado pela IA: {e}")
                    else:
                        print("Nenhuma resposta foi retornada pela IA.")
                except Exception as e:
                    print(f"Erro ao processar a imagem no Gemini: {e}")
            else:
                print("Imagem não processada corretamente.")
        else:
            print("Erro ao processar a imagem com Gemini.")











def upload_to_gemini(image_bytes, mime_type="image/png"):
    """Faz o upload da imagem para o Gemini e retorna a URI."""
    try:
        file = genai.upload_file(image_bytes, mime_type=mime_type)
        return file
    except Exception as e:
        print(f"Erro ao fazer upload da imagem: {e}")
        return None


def processar_imagem(image_path):
    """Processa a imagem recebida como input."""
    try:
        image = Image.open(image_path)
        return image
    except Exception as e:
        print(f"Erro ao processar a imagem: {e}")
        return None


class ProcessNitterViewPMERJ(View):
    def get(self, request):
        try:
            # Configurar Selenium para capturar o screenshot
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
            driver.get('https://nitter.net/PMERJ')
            time.sleep(5)  # Aguarda a página carregar
            driver.execute_script("document.body.style.zoom='33%'")  # Ajusta o zoom para capturar a tela toda
            time.sleep(5)  # Aguarda o zoom ser aplicado
            screenshot_path = 'screenshotPMERJ.png'
            driver.save_screenshot(screenshot_path)  # Salva a captura da tela
            driver.quit()  # Fecha o navegador

            # Chama a função para processar a imagem e obter os dados do Gemini
            self.process_image_with_gemini(screenshot_path)

            # Retorna uma mensagem de sucesso
            return JsonResponse({"message": "Screenshot capturado com sucesso!"})

        except Exception as e:
            return JsonResponse({"error": f"Ocorreu um erro: {str(e)}"}, status=500)

    def process_image_with_gemini(self, image_path):
        """Processa a imagem com Gemini."""
        # Abrir imagem com PIL
        image = processar_imagem(image_path)
        if image:
            # Converter imagem para bytes para upload
            image_bytes = io.BytesIO()
            image.save(image_bytes, format="PNG")
            image_bytes.seek(0)

            # Fazer upload para Gemini
            file = upload_to_gemini(image_bytes)

            if file:
                try:
                    # Criar a sessão de chat
                    chat_session = model.start_chat(history=[{"role": "user", "parts": [file]}])

                    # Enviar o prompt para o modelo
                    prompt = (
                        "Transcreva a imagem do screenshot anexada. Foque em transcrever somente os tweets exibidos. "
                        "Formate o texto de cada tweet em algo com uma formatação parecida com um arquivo JSON. "
                        "Foque em pegar somente os seguintes dados que vou te falar agora: "
                        "author, username, timestamp, text, retweeted_by, replies, retweets, likes."
                    )
                    response = chat_session.send_message(prompt)
                    
                    # Verifique se a IA retornou algum texto
                    if response.text.strip():
                        # Limpar delimitadores Markdown da resposta
                        limpa_resposta = re.sub(r"```json|```", "", response.text.strip()).strip()

                        try:
                            response_data = json.loads(limpa_resposta)

                            # Armazenar dados da IA na model TweetData
                            for tweet in response_data:
                                TweetDataPMERJ.objects.create(
                                    author=tweet.get('author'),
                                    username=tweet.get('username'),
                                    timestamp=tweet.get('timestamp'),
                                    text=tweet.get('text'),
                                    retweeted_by=tweet.get('retweeted_by'),
                                    replies=tweet.get('replies', 0),
                                    retweets=tweet.get('retweets', 0),
                                    likes=tweet.get('likes', 0)
                                )

                            # Exibir os dados formatados como JSON
                            print("Dados da IA em Formato JSON:", response_data)

                        except json.JSONDecodeError as e:
                            print(f"Erro ao decodificar o JSON retornado pela IA: {e}")
                    else:
                        print("Nenhuma resposta foi retornada pela IA.")
                except Exception as e:
                    print(f"Erro ao processar a imagem no Gemini: {e}")
            else:
                print("Imagem não processada corretamente.")
        else:
            print("Erro ao processar a imagem com Gemini.")














def upload_to_gemini(image_bytes, mime_type="image/png"):
    """Faz o upload da imagem para o Gemini e retorna a URI."""
    try:
        file = genai.upload_file(image_bytes, mime_type=mime_type)
        return file
    except Exception as e:
        print(f"Erro ao fazer upload da imagem: {e}")
        return None


def processar_imagem(image_path):
    """Processa a imagem recebida como input."""
    try:
        image = Image.open(image_path)
        return image
    except Exception as e:
        print(f"Erro ao processar a imagem: {e}")
        return None


class ProcessNitterViewTremRJ(View):
    def get(self, request):
        try:
            # Configurar Selenium para capturar o screenshot
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
            driver.get('https://nitter.net/SuperVia_trens')
            time.sleep(5)  # Aguarda a página carregar
            driver.execute_script("document.body.style.zoom='75%'")  # Ajusta o zoom para capturar a tela toda
            time.sleep(5)  # Aguarda o zoom ser aplicado
            screenshot_path = 'screenshotTREM.png'
            driver.save_screenshot(screenshot_path)  # Salva a captura da tela
            driver.quit()  # Fecha o navegador

            # Chama a função para processar a imagem e obter os dados do Gemini
            self.process_image_with_gemini(screenshot_path)

            # Retorna uma mensagem de sucesso
            return JsonResponse({"message": "Screenshot capturado com sucesso!"})

        except Exception as e:
            return JsonResponse({"error": f"Ocorreu um erro: {str(e)}"}, status=500)

    def process_image_with_gemini(self, image_path):
        """Processa a imagem com Gemini."""
        # Abrir imagem com PIL
        image = processar_imagem(image_path)
        if image:
            # Converter imagem para bytes para upload
            image_bytes = io.BytesIO()
            image.save(image_bytes, format="PNG")
            image_bytes.seek(0)

            # Fazer upload para Gemini
            file = upload_to_gemini(image_bytes)

            if file:
                try:
                    # Criar a sessão de chat
                    chat_session = model.start_chat(history=[{"role": "user", "parts": [file]}])

                    # Enviar o prompt para o modelo
                    prompt = (
                        "Transcreva a imagem do screenshot anexada. Foque em transcrever somente os tweets exibidos. "
                        "Formate o texto de cada tweet em algo com uma formatação parecida com um arquivo JSON. "
                        "Foque em pegar somente os seguintes dados que vou te falar agora: "
                        "author, username, timestamp, text, retweeted_by, replies, retweets, likes."
                    )
                    response = chat_session.send_message(prompt)
                    
                    # Verifique se a IA retornou algum texto
                    if response.text.strip():
                        # Limpar delimitadores Markdown da resposta
                        limpa_resposta = re.sub(r"```json|```", "", response.text.strip()).strip()

                        try:
                            response_data = json.loads(limpa_resposta)

                            # Armazenar dados da IA na model TweetData
                            for tweet in response_data:
                                TweetDataTREM.objects.create(
                                    author=tweet.get('author'),
                                    username=tweet.get('username'),
                                    timestamp=tweet.get('timestamp'),
                                    text=tweet.get('text'),
                                    retweeted_by=tweet.get('retweeted_by'),
                                    replies=tweet.get('replies', 0),
                                    retweets=tweet.get('retweets', 0),
                                    likes=tweet.get('likes', 0)
                                )

                            # Exibir os dados formatados como JSON
                            print("Dados da IA em Formato JSON:", response_data)

                        except json.JSONDecodeError as e:
                            print(f"Erro ao decodificar o JSON retornado pela IA: {e}")
                    else:
                        print("Nenhuma resposta foi retornada pela IA.")
                except Exception as e:
                    print(f"Erro ao processar a imagem no Gemini: {e}")
            else:
                print("Imagem não processada corretamente.")
        else:
            print("Erro ao processar a imagem com Gemini.")







def upload_to_gemini(image_bytes, mime_type="image/png"):
    """Faz o upload da imagem para o Gemini e retorna a URI."""
    try:
        file = genai.upload_file(image_bytes, mime_type=mime_type)
        return file
    except Exception as e:
        print(f"Erro ao fazer upload da imagem: {e}")
        return None


def processar_imagem(image_path):
    """Processa a imagem recebida como input."""
    try:
        image = Image.open(image_path)
        return image
    except Exception as e:
        print(f"Erro ao processar a imagem: {e}")
        return None


class ProcessNitterViewVOZ(View):
    def get(self, request):
        try:
            # Configurar Selenium para capturar o screenshot
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
            driver.get('https://nitter.net/search?f=tweets&q=vozdacomunidade')
            time.sleep(5)  # Aguarda a página carregar
            driver.execute_script("document.body.style.zoom='75%'")  # Ajusta o zoom para capturar a tela toda
            time.sleep(5)  # Aguarda o zoom ser aplicado
            screenshot_path = 'screenshotVOZ.png'
            driver.save_screenshot(screenshot_path)  # Salva a captura da tela
            driver.quit()  # Fecha o navegador

            # Chama a função para processar a imagem e obter os dados do Gemini
            self.process_image_with_gemini(screenshot_path)

            # Retorna uma mensagem de sucesso
            return JsonResponse({"message": "Screenshot capturado com sucesso!"})

        except Exception as e:
            return JsonResponse({"error": f"Ocorreu um erro: {str(e)}"}, status=500)

    def process_image_with_gemini(self, image_path):
        """Processa a imagem com Gemini."""
        # Abrir imagem com PIL
        image = processar_imagem(image_path)
        if image:
            # Converter imagem para bytes para upload
            image_bytes = io.BytesIO()
            image.save(image_bytes, format="PNG")
            image_bytes.seek(0)

            # Fazer upload para Gemini
            file = upload_to_gemini(image_bytes)

            if file:
                try:
                    # Criar a sessão de chat
                    chat_session = model.start_chat(history=[{"role": "user", "parts": [file]}])

                    # Enviar o prompt para o modelo
                    prompt = (
                        "Transcreva a imagem do screenshot anexada. Foque em transcrever somente os tweets exibidos. "
                        "Formate o texto de cada tweet em algo com uma formatação parecida com um arquivo JSON. "
                        "Foque em pegar somente os seguintes dados que vou te falar agora: "
                        "author, username, timestamp, text, retweeted_by, replies, retweets, likes."
                    )
                    response = chat_session.send_message(prompt)
                    
                    # Verifique se a IA retornou algum texto
                    if response.text.strip():
                        # Limpar delimitadores Markdown da resposta
                        limpa_resposta = re.sub(r"```json|```", "", response.text.strip()).strip()

                        try:
                            response_data = json.loads(limpa_resposta)

                            # Armazenar dados da IA na model TweetData
                            for tweet in response_data:
                                TweetDataVOZ.objects.create(
                                    author=tweet.get('author'),
                                    username=tweet.get('username'),
                                    timestamp=tweet.get('timestamp'),
                                    text=tweet.get('text'),
                                    retweeted_by=tweet.get('retweeted_by'),
                                    replies=tweet.get('replies', 0),
                                    retweets=tweet.get('retweets', 0),
                                    likes=tweet.get('likes', 0)
                                )

                            # Exibir os dados formatados como JSON
                            print("Dados da IA em Formato JSON:", response_data)

                        except json.JSONDecodeError as e:
                            print(f"Erro ao decodificar o JSON retornado pela IA: {e}")
                    else:
                        print("Nenhuma resposta foi retornada pela IA.")
                except Exception as e:
                    print(f"Erro ao processar a imagem no Gemini: {e}")
            else:
                print("Imagem não processada corretamente.")
        else:
            print("Erro ao processar a imagem com Gemini.")






def upload_to_gemini(image_bytes, mime_type="image/png"):
    """Faz o upload da imagem para o Gemini e retorna a URI."""
    try:
        file = genai.upload_file(image_bytes, mime_type=mime_type)
        return file
    except Exception as e:
        print(f"Erro ao fazer upload da imagem: {e}")
        return None


def processar_imagem(image_path):
    """Processa a imagem recebida como input."""
    try:
        image = Image.open(image_path)
        return image
    except Exception as e:
        print(f"Erro ao processar a imagem: {e}")
        return None


class ProcessNitterViewCOR(View):
    def get(self, request):
        try:
            # Configurar Selenium para capturar o screenshot
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
            driver.get('https://nitter.net/search?f=tweets&q=OperacoesRio')
            time.sleep(5)  # Aguarda a página carregar
            driver.execute_script("document.body.style.zoom='75%'")  # Ajusta o zoom para capturar a tela toda
            time.sleep(5)  # Aguarda o zoom ser aplicado
            screenshot_path = 'screenshotcor.png'
            driver.save_screenshot(screenshot_path)  # Salva a captura da tela
            driver.quit()  # Fecha o navegador

            # Chama a função para processar a imagem e obter os dados do Gemini
            self.process_image_with_gemini(screenshot_path)

            # Retorna uma mensagem de sucesso
            return JsonResponse({"message": "Screenshot capturado com sucesso!"})

        except Exception as e:
            return JsonResponse({"error": f"Ocorreu um erro: {str(e)}"}, status=500)

    def process_image_with_gemini(self, image_path):
        """Processa a imagem com Gemini."""
        # Abrir imagem com PIL
        image = processar_imagem(image_path)
        if image:
            # Converter imagem para bytes para upload
            image_bytes = io.BytesIO()
            image.save(image_bytes, format="PNG")
            image_bytes.seek(0)

            # Fazer upload para Gemini
            file = upload_to_gemini(image_bytes)

            if file:
                try:
                    # Criar a sessão de chat
                    chat_session = model.start_chat(history=[{"role": "user", "parts": [file]}])

                    # Enviar o prompt para o modelo
                    prompt = (
                        "Transcreva a imagem do screenshot anexada. Foque em transcrever somente os tweets exibidos. "
                        "Formate o texto de cada tweet em algo com uma formatação parecida com um arquivo JSON. "
                        "Foque em pegar somente os seguintes dados que vou te falar agora: "
                        "author, username, timestamp, text, retweeted_by, replies, retweets, likes."
                    )
                    response = chat_session.send_message(prompt)
                    
                    # Verifique se a IA retornou algum texto
                    if response.text.strip():
                        # Limpar delimitadores Markdown da resposta
                        limpa_resposta = re.sub(r"```json|```", "", response.text.strip()).strip()

                        try:
                            response_data = json.loads(limpa_resposta)

                            # Armazenar dados da IA na model TweetData
                            for tweet in response_data:
                                TweetDataCOR.objects.create(
                                    author=tweet.get('author'),
                                    username=tweet.get('username'),
                                    timestamp=tweet.get('timestamp'),
                                    text=tweet.get('text'),
                                    retweeted_by=tweet.get('retweeted_by'),
                                    replies=tweet.get('replies', 0),
                                    retweets=tweet.get('retweets', 0),
                                    likes=tweet.get('likes', 0)
                                )

                            # Exibir os dados formatados como JSON
                            print("Dados da IA em Formato JSON:", response_data)

                        except json.JSONDecodeError as e:
                            print(f"Erro ao decodificar o JSON retornado pela IA: {e}")
                    else:
                        print("Nenhuma resposta foi retornada pela IA.")
                except Exception as e:
                    print(f"Erro ao processar a imagem no Gemini: {e}")
            else:
                print("Imagem não processada corretamente.")
        else:
            print("Erro ao processar a imagem com Gemini.")











def upload_to_gemini(image_bytes, mime_type="image/png"):
    """Faz o upload da imagem para o Gemini e retorna a URI."""
    try:
        file = genai.upload_file(image_bytes, mime_type=mime_type)
        return file
    except Exception as e:
        print(f"Erro ao fazer upload da imagem: {e}")
        return None


def processar_imagem(image_path):
    """Processa a imagem recebida como input."""
    try:
        image = Image.open(image_path)
        return image
    except Exception as e:
        print(f"Erro ao processar a imagem: {e}")
        return None


class ProcessNitterViewPonteRJ(View):
    def get(self, request):
        try:
            # Configurar Selenium para capturar o screenshot
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
            driver.get('https://nitter.net/search?f=tweets&q=_ecoponte')
            time.sleep(5)  # Aguarda a página carregar
            driver.execute_script("document.body.style.zoom='75%'")  # Ajusta o zoom para capturar a tela toda
            time.sleep(5)  # Aguarda o zoom ser aplicado
            screenshot_path = 'screenshotponterj.png'
            driver.save_screenshot(screenshot_path)  # Salva a captura da tela
            driver.quit()  # Fecha o navegador

            # Chama a função para processar a imagem e obter os dados do Gemini
            self.process_image_with_gemini(screenshot_path)

            # Retorna uma mensagem de sucesso
            return JsonResponse({"message": "Screenshot capturado com sucesso!"})

        except Exception as e:
            return JsonResponse({"error": f"Ocorreu um erro: {str(e)}"}, status=500)

    def process_image_with_gemini(self, image_path):
        """Processa a imagem com Gemini."""
        # Abrir imagem com PIL
        image = processar_imagem(image_path)
        if image:
            # Converter imagem para bytes para upload
            image_bytes = io.BytesIO()
            image.save(image_bytes, format="PNG")
            image_bytes.seek(0)

            # Fazer upload para Gemini
            file = upload_to_gemini(image_bytes)

            if file:
                try:
                    # Criar a sessão de chat
                    chat_session = model.start_chat(history=[{"role": "user", "parts": [file]}])

                    # Enviar o prompt para o modelo
                    prompt = (
                        "Transcreva a imagem do screenshot anexada. Foque em transcrever somente os tweets exibidos. "
                        "Formate o texto de cada tweet em algo com uma formatação parecida com um arquivo JSON. "
                        "Foque em pegar somente os seguintes dados que vou te falar agora: "
                        "author, username, timestamp, text, retweeted_by, replies, retweets, likes."
                    )
                    response = chat_session.send_message(prompt)
                    
                    # Verifique se a IA retornou algum texto
                    if response.text.strip():
                        # Limpar delimitadores Markdown da resposta
                        limpa_resposta = re.sub(r"```json|```", "", response.text.strip()).strip()

                        try:
                            response_data = json.loads(limpa_resposta)

                            # Armazenar dados da IA na model TweetData
                            for tweet in response_data:
                                TweetDataPonteRJ.objects.create(
                                    author=tweet.get('author'),
                                    username=tweet.get('username'),
                                    timestamp=tweet.get('timestamp'),
                                    text=tweet.get('text'),
                                    retweeted_by=tweet.get('retweeted_by'),
                                    replies=tweet.get('replies', 0),
                                    retweets=tweet.get('retweets', 0),
                                    likes=tweet.get('likes', 0)
                                )

                            # Exibir os dados formatados como JSON
                            print("Dados da IA em Formato JSON:", response_data)

                        except json.JSONDecodeError as e:
                            print(f"Erro ao decodificar o JSON retornado pela IA: {e}")
                    else:
                        print("Nenhuma resposta foi retornada pela IA.")
                except Exception as e:
                    print(f"Erro ao processar a imagem no Gemini: {e}")
            else:
                print("Imagem não processada corretamente.")
        else:
            print("Erro ao processar a imagem com Gemini.")






def upload_to_gemini(image_bytes, mime_type="image/png"):
    """Faz o upload da imagem para o Gemini e retorna a URI."""
    try:
        file = genai.upload_file(image_bytes, mime_type=mime_type)
        return file
    except Exception as e:
        print(f"Erro ao fazer upload da imagem: {e}")
        return None


def processar_imagem(image_path):
    """Processa a imagem recebida como input."""
    try:
        image = Image.open(image_path)
        return image
    except Exception as e:
        print(f"Erro ao processar a imagem: {e}")
        return None


class ProcessNitterView(View):
    def get(self, request):
        try:
            # Configurar Selenium para capturar o screenshot
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
            driver.get('https://nitter.net/search?f=tweets&q=FogoCruzadoRJ')
            time.sleep(5)  # Aguarda a página carregar
            driver.execute_script("document.body.style.zoom='75%'")  # Ajusta o zoom para capturar a tela toda
            time.sleep(5)  # Aguarda o zoom ser aplicado
            screenshot_path = 'screenshot.png'
            driver.save_screenshot(screenshot_path)  # Salva a captura da tela
            driver.quit()  # Fecha o navegador

            # Chama a função para processar a imagem e obter os dados do Gemini
            self.process_image_with_gemini(screenshot_path)

            # Retorna uma mensagem de sucesso
            return JsonResponse({"message": "Screenshot capturado com sucesso!"})

        except Exception as e:
            return JsonResponse({"error": f"Ocorreu um erro: {str(e)}"}, status=500)

    def process_image_with_gemini(self, image_path):
        """Processa a imagem com Gemini."""
        # Abrir imagem com PIL
        image = processar_imagem(image_path)
        if image:
            # Converter imagem para bytes para upload
            image_bytes = io.BytesIO()
            image.save(image_bytes, format="PNG")
            image_bytes.seek(0)

            # Fazer upload para Gemini
            file = upload_to_gemini(image_bytes)

            if file:
                try:
                    # Criar a sessão de chat
                    chat_session = model.start_chat(history=[{"role": "user", "parts": [file]}])

                    # Enviar o prompt para o modelo
                    prompt = (
                        "Transcreva a imagem do screenshot anexada. Foque em transcrever somente os tweets exibidos. "
                        "Formate o texto de cada tweet em algo com uma formatação parecida com um arquivo JSON. "
                        "Foque em pegar somente os seguintes dados que vou te falar agora: "
                        "author, username, timestamp, text, retweeted_by, replies, retweets, likes."
                    )
                    response = chat_session.send_message(prompt)
                    
                    # Verifique se a IA retornou algum texto
                    if response.text.strip():
                        # Limpar delimitadores Markdown da resposta
                        limpa_resposta = re.sub(r"```json|```", "", response.text.strip()).strip()

                        try:
                            response_data = json.loads(limpa_resposta)

                            # Armazenar dados da IA na model TweetData
                            for tweet in response_data:
                                TweetData.objects.create(
                                    author=tweet.get('author'),
                                    username=tweet.get('username'),
                                    timestamp=tweet.get('timestamp'),
                                    text=tweet.get('text'),
                                    retweeted_by=tweet.get('retweeted_by'),
                                    replies=tweet.get('replies', 0),
                                    retweets=tweet.get('retweets', 0),
                                    likes=tweet.get('likes', 0)
                                )

                            # Exibir os dados formatados como JSON
                            print("Dados da IA em Formato JSON:", response_data)

                        except json.JSONDecodeError as e:
                            print(f"Erro ao decodificar o JSON retornado pela IA: {e}")
                    else:
                        print("Nenhuma resposta foi retornada pela IA.")
                except Exception as e:
                    print(f"Erro ao processar a imagem no Gemini: {e}")
            else:
                print("Imagem não processada corretamente.")
        else:
            print("Erro ao processar a imagem com Gemini.")





def upload_to_gemini(image_bytes, mime_type="image/png"):
    """Faz o upload da imagem para o Gemini e retorna a URI."""
    try:
        file = genai.upload_file(image_bytes, mime_type=mime_type)
        return file
    except Exception as e:
        print(f"Erro ao fazer upload da imagem: {e}")
        return None


def processar_imagem(image_path):
    """Processa a imagem recebida como input."""
    try:
        image = Image.open(image_path)
        return image
    except Exception as e:
        print(f"Erro ao processar a imagem: {e}")
        return None


class ProcessNitterViewPenhaRJ(View):
    def get(self, request):
        try:
            # Configurar Selenium para capturar o screenshot
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
            driver.get('https://nitter.net/search?f=tweets&q=PenhaNewsRJ')
            time.sleep(5)  # Aguarda a página carregar
            driver.execute_script("document.body.style.zoom='75%'")  # Ajusta o zoom para capturar a tela toda
            time.sleep(5)  # Aguarda o zoom ser aplicado
            screenshot_path = 'screenshotPENHA.png'
            driver.save_screenshot(screenshot_path)  # Salva a captura da tela
            driver.quit()  # Fecha o navegador

            # Chama a função para processar a imagem e obter os dados do Gemini
            self.process_image_with_gemini(screenshot_path)

            # Retorna uma mensagem de sucesso
            return JsonResponse({"message": "Screenshot capturado com sucesso!"})

        except Exception as e:
            return JsonResponse({"error": f"Ocorreu um erro: {str(e)}"}, status=500)

    def process_image_with_gemini(self, image_path):
        """Processa a imagem com Gemini."""
        # Abrir imagem com PIL
        image = processar_imagem(image_path)
        if image:
            # Converter imagem para bytes para upload
            image_bytes = io.BytesIO()
            image.save(image_bytes, format="PNG")
            image_bytes.seek(0)

            # Fazer upload para Gemini
            file = upload_to_gemini(image_bytes)

            if file:
                try:
                    # Criar a sessão de chat
                    chat_session = model.start_chat(history=[{"role": "user", "parts": [file]}])

                    # Enviar o prompt para o modelo
                    prompt = (
                        "Transcreva a imagem do screenshot anexada. Foque em transcrever somente os tweets exibidos. "
                        "Formate o texto de cada tweet em algo com uma formatação parecida com um arquivo JSON. "
                        "Foque em pegar somente os seguintes dados que vou te falar agora: "
                        "author, username, timestamp, text, retweeted_by, replies, retweets, likes."
                    )
                    response = chat_session.send_message(prompt)
                    
                    # Verifique se a IA retornou algum texto
                    if response.text.strip():
                        # Limpar delimitadores Markdown da resposta
                        limpa_resposta = re.sub(r"```json|```", "", response.text.strip()).strip()

                        try:
                            response_data = json.loads(limpa_resposta)

                            # Armazenar dados da IA na model TweetData
                            for tweet in response_data:
                                TweetDataPenhaRJ.objects.create(
                                    author=tweet.get('author'),
                                    username=tweet.get('username'),
                                    timestamp=tweet.get('timestamp'),
                                    text=tweet.get('text'),
                                    retweeted_by=tweet.get('retweeted_by'),
                                    replies=tweet.get('replies', 0),
                                    retweets=tweet.get('retweets', 0),
                                    likes=tweet.get('likes', 0)
                                )

                            # Exibir os dados formatados como JSON
                            print("Dados da IA em Formato JSON:", response_data)

                        except json.JSONDecodeError as e:
                            print(f"Erro ao decodificar o JSON retornado pela IA: {e}")
                    else:
                        print("Nenhuma resposta foi retornada pela IA.")
                except Exception as e:
                    print(f"Erro ao processar a imagem no Gemini: {e}")
            else:
                print("Imagem não processada corretamente.")
        else:
            print("Erro ao processar a imagem com Gemini.")





