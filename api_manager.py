"""
Gerencia a comunicação com a API do ChatGPT (LLM), incluindo leitura segura da chave e tratamento de erros.
"""
import os
import requests
from dotenv import load_dotenv

class APIManager:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("Chave da API OpenAI não encontrada. Configure no arquivo .env.")
        self.api_url = os.getenv("OPENAI_API_URL", "https://api.openai.com/v1/chat/completions")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4-1106-preview")

    def send_question(self, texto):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "Você é um assistente especializado em resolver questões do LeetCode."},
                {"role": "user", "content": texto}
            ],
            "max_tokens": 1024,
            "temperature": 0.2
        }
        try:
            resp = requests.post(self.api_url, headers=headers, json=data, timeout=30)
            resp.raise_for_status()
            resposta = resp.json()
            return resposta["choices"][0]["message"]["content"]
        except requests.exceptions.HTTPError as e:
            if resp.status_code == 401:
                raise Exception("Chave de API inválida ou não autorizada.")
            elif resp.status_code == 429:
                raise Exception("Limite de uso da API atingido. Tente novamente mais tarde.")
            else:
                raise Exception(f"Erro HTTP: {resp.status_code} - {resp.text}")
        except Exception as e:
            raise Exception(f"Erro ao conectar à API: {e}")