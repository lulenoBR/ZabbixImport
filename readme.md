Importação de Ícones no Zabbix via API
Este script Python foi desenvolvido para facilitar a importação de ícones para o Zabbix usando a API JSON-RPC. Ele permite que você adicione múltiplos ícones de uma vez, verifica se os ícones já existem no Zabbix antes de importá-los e mantém um registro de quais ícones foram importados com sucesso ou não.

Pré-requisitos
Python: Certifique-se de que o Python esteja instalado na sua máquina. Você pode baixá-lo em python.org.
A versão utilizada neste script foi a 3.12.4.

Bibliotecas Python: O script usa as seguintes bibliotecas Python, que podem ser instaladas usando o pip:

pip install requests
(ou veja o arquivo requirements.txt)

Configuração do Zabbix:

Certifique-se de ter acesso admin ao Zabbix.
Conheça a URL do frontend do Zabbix e as credenciais de acesso.

Configuração
Arquivo de Configuração (config.cfg):

Este arquivo contém as configurações necessárias para se conectar ao Zabbix. Se não existir, o script criará um arquivo de configuração padrão na primeira execução.
Edite o arquivo config.cfg com as seguintes informações:

[Zabbix]
url = http://seu-endereco-zabbix/zabbix/api_jsonrpc.php
username = seu_usuario_admin
password = sua_senha_admin

Diretório de Ícones (importar):

Coloque os ícones que deseja importar para o Zabbix no diretório importar. Os ícones devem estar no formato .png. 
Caso a pasta não exista, será criada na primeira execução do script.

Uso
Execução do Script:

Abra um terminal ou prompt de comando.
Navegue até o diretório onde o script está localizado.
Execute o script com o comando:

python ZabbixImport.py

O script verificará se o diretório importar existe. Se não existir, ele será criado.
Em seguida, ele verificará cada arquivo no diretório importar, tentando importá-los para o Zabbix.
Um arquivo de log (icones_nao_importados.log) será criado ou atualizado no mesmo diretório para registrar quais ícones não foram importados, se houver algum problema.

Monitoramento do Progresso:

Durante a execução, o script imprimirá mensagens no terminal indicando o status de cada ícone sendo processado.
Após a conclusão, uma mensagem será exibida informando que a importação de ícones foi concluída.