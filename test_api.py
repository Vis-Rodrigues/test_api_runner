import pytest
import requests
import logging
from config.loader import load_config
from utils.files import load_payload, load_expected_body_file
from utils.masking import mask_sensitive_data
from auth.handler import handle_auth

# Configuração básica do logger
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

config = load_config()
tests = config.get("tests", [])
credentials = config.get("credentials", {})
variables = config.get("variables", {})

def replace_vars(s):
    if isinstance(s, str):
        for k, v in variables.items():
            s = s.replace(f"${{{k}}}", str(v))
    return s

def deep_replace(data):
    if isinstance(data, dict):
        return {k: deep_replace(replace_vars(v)) for k, v in data.items()}
    elif isinstance(data, list):
        return [deep_replace(replace_vars(i)) for i in data]
    else:
        return replace_vars(data)

def make_test_id(test):
    method = test['method'].upper()
    path = test['path'].strip('/').replace('/', '_').replace('{', '').replace('}', '')
    return f"{method}_{path}"

tests = [deep_replace(t) for t in config['tests']]
test_ids = [make_test_id(t) for t in tests]

@pytest.mark.parametrize("test", tests, ids=test_ids)
def test_api(test):
    base_url = config['base_url']
    url = base_url + test['path']
    method = test['method'].upper()
    payload = test.get('payload', {})
    headers = test.get('headers', {})
    params = test.get('query_params', {})
    expected_status = test['expected_status']

    if test.get("apikey"):
        headers["x-api-key"] = credentials.get("apikey")

    auth_type = test.get("auth")
    if auth_type:
        handle_auth(auth_type, headers, credentials)

    if test.get("payload_file"):
        payload = load_payload(test["payload_file"])

    # Log da requisição
    logging.info(f"[REQUEST] {method} - {url}")
    logging.info(f"[REQUEST] Headers: {mask_sensitive_data(headers)}")
    logging.info(f"[REQUEST] Query Params: {params}")
    logging.info(f"[REQUEST] Payload: {payload}")

    response = requests.request(method, url, json=payload, headers=headers, params=params)

    # Log da resposta
    logging.info(f"==========================================")
    logging.info(f"[RESPONSE] Status Code: {response.status_code}")
    logging.info(f"[RESPONSE] Body: {response.json()}")
    logging.info(f"[RESPONSE] Headers: {response.headers}")

    try:
        expected_status = int(expected_status)  # Converte para inteiro
    except ValueError as e:
        raise ValueError(f"Erro ao converter expected_status para inteiro: {e}")

    assert response.status_code == expected_status, (
        f"{method} {url} - Esperado: {expected_status}, Recebido: {response.status_code}"
    )

    if 'expected_body_file' in test:
        json_response = response.json()
        expected_body = load_expected_body_file(test['expected_body_file'])
        assert json_response == expected_body, (
                f"{url} - Esperado body: {expected_body}, Recebido: {json_response}"
            )

    if 'expected_body' in test:
        try:
            json_response = response.json()
        except Exception:
            pytest.fail(f"{url} - Resposta não é JSON válido.")
        for key, value in test['expected_body'].items():
            assert json_response.get(key) == value, (
                f"{url} - Esperado body[{key}]: {value}, Recebido: {json_response.get(key)}"
            )

    if 'expected_headers' in test:
        for key, val in test['expected_headers'].items():
            actual_value = response.headers.get(key)
            assert actual_value == val, (
                f"{url} - Esperado header[{key}]: {val}, Recebido: {actual_value}"
            )
