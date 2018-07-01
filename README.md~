#### README ####
Os passos seguintes foram testados no Ubunto 14.04 LTS recem instalado.


#### Objetivo ####
O objetivo desse trabalho é desenvolver uma aplicação para executar missões de vistoria utilizando drones autonomos.


#### Preparando o ambiente (Fazer isso somente 1 vez) ####
## Clonar o repositorio da aplicação
git clone https://f4b10c0st4@bitbucket.org/dronufba/control-tower.git

## Instalar o virtualenv (para que as dependencias do projeto nao sejam instaladas globalmente)
aptitude install python-dev python-pip virtualenv build-essential

## Cria/instala o diretorio dos arquivos do ambiente virtual 
# venv diretorio que ira armazenar as informacoes do ambiente virtual
# pode-se escolher o diretorio
virtualenv venv

## Ativa o virtualenv
source venv/bin/activate

## No diretorio do control-tower instalar os requirements da aplicação
cd ../control-tower/
pip install -r requirements.txt

## Criar banco de dados
python dbinit.py


#### Rodando a aplicação (Após preparar o ambiente) ####

## Ativa o virtualenv
source venv/bin/activate

## Inicializar a aplicação
python run.py

## Acessar a aplicação
Abrir o browser e acessar o link <localhost:5000>. Caso nao funcione, utilizar o link informado no terminal ao executar o comando anterior.

Acessar a aplicação utilizando as credenciais:
user: admin@admin
password: password
(as credencias são carregadas ao banco no arquivo dbinit.py)

#### Areas da aplição ####
A aplicação contém em principio duas áreas que são Cadastrar Missão e Executar Missão.

## Cadastrar Missão ##
Nessa página o usuário poderá criar uma missão.
Para isso será necessário dar-se um nome a missão e selecionar a area no mapa que o drone irá percorrer. Ao finalizar pressionar o botão de Salvar Missão.

* A principio essa página será necessário conexão com a internet para se carregar o maps.

## Executar Missão ##
Nessa página o usuário poderá criar uma missão.
Para isso o usuário selecionará um drone e uma missão. Após, pressionar o botão de executar missão.

* A principio essa página será necessário conexão com a rede do drone para que se possa fazer a comunicação da missão pro drone.














*Note: Each time the files are changed the application restarts automatically*

## Contribution guidelines ##

**Variables, functions and files-> all in lowercase and/or separated by underline:**

* drone
* drone_new()
* drone_edit.html

**Classes -> Initial capital letter for each word:**

* Drone()
* DroneEdit()

*Note: Everything in English*
