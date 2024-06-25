import requests
import base64
import os
import json
import configparser
from datetime import datetime

# Nome do arquivo de configuração
config_file = 'config.cfg'

# Configurações padrão
default_config = {
    'Zabbix': {
        'url': 'http://172.20.14.104/zabbix/api_jsonrpc.php',
        'username': 'Admin',
        'password': 'zabbix'
    }
}

# Função para criar um arquivo de configuração padrão
def create_default_config(file_path, config):
    config_parser = configparser.ConfigParser()
    config_parser.read_dict(config)
    with open(file_path, 'w') as configfile:
        config_parser.write(configfile)

# Verificar se o arquivo de configuração existe, caso contrário, criar com configurações padrão
if not os.path.exists(config_file):
    print(f"Arquivo de configuração '{config_file}' não encontrado. Criando um arquivo com as configurações padrão.")
    create_default_config(config_file, default_config)

# Ler configurações do arquivo .cfg
config = configparser.ConfigParser()
config.read(config_file)

# Configurações do Zabbix
zabbix_url = config['Zabbix']['url']
username = config['Zabbix']['username']
password = config['Zabbix']['password']

# Função para realizar login no Zabbix
def login():
    payload = {
        "jsonrpc": "2.0",
        "method": "user.login",
        "params": {
            "username": username,
            "password": password
        },
        "id": 1
    }
    headers = {
        "Content-Type": "application/json-rpc"
    }
    response = requests.post(zabbix_url, json=payload, headers=headers)
    response_data = response.json()
    
    if 'result' in response_data:
        return response_data['result']
    else:
        raise Exception(f"Erro ao realizar login: {response_data.get('error', 'Resposta desconhecida da API')}")

# Função para verificar se um ícone já existe
def icon_exists(auth_token, name):
    payload = {
        "jsonrpc": "2.0",
        "method": "image.get",
        "params": {
            "output": ["imageid"],
            "filter": {
                "name": name
            }
        },
        "auth": auth_token,
        "id": 1
    }
    headers = {
        "Content-Type": "application/json-rpc"
    }
    response = requests.post(zabbix_url, json=payload, headers=headers)
    response_data = response.json()
    
    if 'result' in response_data:
        return len(response_data['result']) > 0
    else:
        raise Exception(f"Erro ao verificar ícone: {response_data.get('error', 'Resposta desconhecida da API')}")

# Função para adicionar um ícone
def add_icon(auth_token, name, image_data):
    payload = {
        "jsonrpc": "2.0",
        "method": "image.create",
        "params": {
            "name": name,
            "image": image_data,
            "imagetype": 1
        },
        "auth": auth_token,
        "id": 1
    }
    headers = {
        "Content-Type": "application/json-rpc"
    }
    response = requests.post(zabbix_url, json=payload, headers=headers)
    response_data = response.json()
    
    if 'result' in response_data:
        return response_data
    else:
        raise Exception(f"Erro ao adicionar ícone: {response_data.get('error', 'Resposta desconhecida da API')}")

# Diretório onde os ícones estarão armazenados
icon_directory = 'importar'

# Verificar se o diretório 'importar' existe, caso contrário, criá-lo
if not os.path.exists(icon_directory):
    os.makedirs(icon_directory)
    print(f"Diretório '{icon_directory}' criado.")

# Arquivo de log para ícones não importados
log_file_path = 'icones_nao_importados.log'

try:
    # Login no Zabbix
    auth_token = login()
    
    # Abrir o arquivo de log em modo de adição
    with open(log_file_path, 'a') as log_file:
        for filename in os.listdir(icon_directory):
            if filename.endswith(".png"):
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                if icon_exists(auth_token, filename):
                    log_file.write(f"{timestamp} - Ícone {filename} não importado: já existe\n")
                    print(f"{timestamp} - Ícone {filename} não importado: já existe")
                else:
                    with open(os.path.join(icon_directory, filename), "rb") as icon_file:
                        encoded_string = base64.b64encode(icon_file.read()).decode('utf-8')
                        response = add_icon(auth_token, filename, encoded_string)
                        print(f"{timestamp} - Adicionado ícone {filename}: {response}")

    print("Importação de ícones concluída.")

except Exception as e:
    print(f"Ocorreu um erro: {e}")
