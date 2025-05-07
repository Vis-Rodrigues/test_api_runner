import base64
import logging
import requests
from config.config import config

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

access_token_cache = None

def handle_auth(auth_type, headers, credentials):
    # Recupera as variáveis user e password
    user = credentials.get("user", "")
    password = credentials.get("pass", "")

    if not user or not password:
        raise EnvironmentError("Variáveis 'user' ou 'pass' não configuradas.")

    auth_string = f"{user}:{password}"
    base64_auth = base64.b64encode(auth_string.encode()).decode()

    if auth_type.lower() == "basic":
        headers["Authorization"] = f"Basic {base64_auth}"
        logging.info("[AUTH] - Authorization configurado com Basic.")
    elif auth_type.lower() == "oauth2":
        global access_token_cache
        if not access_token_cache:
            oauth_url = config.OAUTH_URL

            logging.info(f"[AUTH] - Fazendo requisição OAuth2 para URL: {oauth_url}")
            
            response = requests.post(
                oauth_url,
                headers={"Authorization": f"Basic {base64_auth}", "Content-Type": "application/x-www-form-urlencoded"},
                data={"grant_type": "client_credentials"}
            )
            if response.status_code != 200:
                raise EnvironmentError("Erro ao obter token OAuth2.")
            access_token_cache = response.json().get("access_token", "")

        headers["Authorization"] = f"Bearer {access_token_cache}"

        logging.info("[AUTH] - Authorization configurado com Bearer (OAuth2).")

    else:
        raise ValueError(f"Tipo de autenticação desconhecido: {auth_type}")
