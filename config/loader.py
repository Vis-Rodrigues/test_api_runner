import os
import yaml
import logging

def get_env_variable(env_name):
    value = os.getenv(env_name.replace("$", ""))
    if value is None:
        logging.error(f"Erro ao recuperar variável de ambiente '{env_name}'.")
        raise EnvironmentError(f"A variável de ambiente '{env_name}' não está definida.")
    return value

def load_config():
    try:
        env = get_env_variable("environment").lower()
    except EnvironmentError:
        logging.error("[ENV] - Erro ao recuperar a variável de ambiente environment")

    
    test_file = f"test-config-{env}.yml"
    logging.info(f"[ENV] - Executando os testes no ambiente {env.upper()}.")
    with open(test_file, 'r') as f:
        raw = f.read()
        raw = os.path.expandvars(raw)
        return yaml.safe_load(raw)
