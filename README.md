# API Test Runner - Framework de Testes Automatizados de API

Automação **No-Code** que executa testes de APIs REST a partir de arquivos YAML. Suporta autenticação Basic e OAuth2, apikey, payloads externos e validação de resposta. 
Ela foi escrita em Python. Executa os cenários de teste com o TaaC e os resultados podem ser utilizados nas mudanças.

## 🧪 Como utilizar?

**Link de projeto utilizando automação:** #TODO

### 📄 Exemplo de configuração no projeto

Para utilizar essa automação, basicamente precisará configurar dois arquivos dentro da pasta */tests*: 
 - **YAML** com dados dos testes por ambiente
> Nome do arquivo ```test-config-dev.yml``` ou ```test-config-hom.yml```.

 - Arquivo de **testspec**
``` YAML
#TODO add arquivo de testspec
```

### Exemplo do test-config com ApiKey

```YAML

base_url: "https://api.exemplo.com"

credentials:
  apikey: $APIKEY # Nome da variável de ambiente para a API Key iniciando com $

variables:
  id: 12345

tests:
  - method: GET
    path: "/clientes/${id}"
    apikey: true
    expected_status: 200

```

### Exemplo do test-config com oAuth

```YAML

base_url: "https://api.exemplo.com"

credentials:
  user: "$USER" #clientId
  pass: "$PASS" #clientSecret

variables:
  id: 12345

tests:
  - method: GET
    path: "/clientes/${id}"
    expected_status: 200
    auth: "oauth" # (Opcional) Tipo de autenticação (oauth ou basic)

```

### 🔐 Autenticação

A automação aceita as autenticações:

- **Basic**: Transforma o *user* e *pass* do YAML em base64 e envia o valor no header `Authorization`.
- **oAuth2**: Realiza a requisição do oAuth da Rede usando *user* e *pass*, envia o access_token no header `Authorization`, esse dado é armazenado em cache para não ficar gerando o token.
- **ApiKey**: Recupera o valor da variável de ambiente e envia no header `x-api-key`.

### 🧰 Recursos

Essa automação disponibiliza diversos recursos para validar as APIs. As configurações são feitas no arquivo de test-config.

- Parametrização via YAML
- Headers, payloads e bodies validados
- **Máscara de logs**: headers como Authorization e x-api-key são ocultados nos logs
- **Payloads externos**: payload_file e expected_body_file suportados como JSON

### Parâmetros do Arquivo YAML

Esta tabela descreve cada parâmetro aceito no arquivo YAML utilizado no projeto.

| **Nome**                | **Descrição**                                                              | **Obrigatório** |
|-------------------------|--------------------------------------------------------------------------|----------------|
| `variables`             | Agrupamento de variáveis globais.                                        | Opcional       |
| `base_url`              | URL base da API a ser testada.                                           | Obrigatório    |
| `credentials`           | Agrupamento de credenciais para autenticação.                            | Obrigatório    |
| `credentials.apikey`    | Nome da variável de ambiente que armazena a API Key. Deve começar com `$`. | Opcional    |
| `credentials.user`      | Identificador do usuário (não sensível).                                | Opcional       |
| `credentials.pass`      | Senha do usuário (não sensível).                                        | Opcional       |
| `tls`                   | Configuração de TLS para certificados.                                  | Opcional       |
| `tls.crt`               | Caminho para o arquivo de certificado.                                  | Opcional       |
| `tls.key`               | Caminho para a chave privada.                                           | Opcional       |
| `tests`                 | Lista de testes com os detalhes dos endpoints.                         | Obrigatório    |
| `tests.path`            | Caminho do endpoint relativo à URL base.                               | Obrigatório    |
| `tests.method`          | Método HTTP utilizado no teste (GET, POST, etc.).                      | Obrigatório    |
| `tests.expected_status` | Código de status HTTP esperado para o teste.                           | Opcional       |
| `tests.apikey`          | Indica se a autenticação por API Key será usada (true/false).         | Opcional       |
| `tests.auth`            | Tipo de autenticação utilizada (basic, oauth2).                       | Opcional       |
| `tests.headers`         | Cabeçalhos adicionais para a requisição HTTP.                         | Opcional       |
| `tests.payload_file`    | Caminho do arquivo que contém o corpo da requisição JSON.             | Opcional       |
| `tests.payload`         | Corpo da requisição JSON diretamente no YAML.                         | Opcional       |
| `tests.expected_body_file` | Arquivo contendo o corpo esperado na resposta.                     | Opcional       |
| `tests.expected_body`   | Estrutura esperada no corpo da resposta da API.                       | Opcional       |
| `tests.expected_headers` | Cabeçalhos esperados na resposta da API.                             | Opcional       |

Exemplo de arquivo com testes: [internal-test-config-dev.yml](/exemplo/internal-test-config-dev.yml)

## 📁 Estrutura da Automação

- `config/loader.py`: Carrega configurações e variáveis de ambiente
- `auth/handler.py`: Configura headers de autenticação
- `utils/files.py`: Lê arquivos de payloads e respostas esperadas
- `utils/masking.py`: Mascaramento de dados sensíveis nos logs
- `test_api.py`: Executa os testes com Pytest
- `exemplo/internal-test-config-dev.yml`: Exemplo de configuração dos testes

## Pré-requisitos da Automação

- Python 3.8+
> `pip install -r requirements.txt`
- Variáveis de ambiente necessárias:
  - `environment`

---

## 🚀 Executando Automação

```bash
environment=hom pytest test_api.py -v --junitxml=report_junit.xml --log-cli-level=INFO
```

## ✅ Requisitos

- Python 3.8+
- requests, pyyaml, pytest

## 🙌 Contribuindo

A sua contribuição é super bem-vinda! =D
Siga os passos abaixo para implementar melhorias.

1. Fork o repositório
2. Crie uma branch: 
> `git checkout -b minha-feature`
3. Envie PRs!

---