import os

class Config:
    OAUTH_URL = os.getenv("API_URL", "https://rl7-sandbox-api.useredecloud.com.br/oauth2/token")

class DevelopmentConfig(Config):
    OAUTH_URL= "https://rl7-sandbox-api.useredecloud.com.br/oauth2/token"

class HomologationConfig(Config):
    OAUTH_URL = "https://dev-api.example.com/oauth/token"

# Escolher configuração baseada na variável de ambiente ENV
ENV = os.getenv("environment", "hom")

if ENV == "hom":
    config = HomologationConfig()
else:
    config = DevelopmentConfig()
