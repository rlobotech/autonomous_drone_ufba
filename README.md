# README
Os passos seguintes foram testados no Ubunto 14.04 LTS recem instalado.


## Objetivo
O objetivo desse trabalho é desenvolver uma aplicação para executar missões de vistoria utilizando drones autonomos.


## Preparando o ambiente (Fazer isso somente 1 vez)
##### Clonar o repositorio da aplicação
```
git clone https://github.com/rlobotech/autonomous_drone_ufba.git
```

##### Instalar o virtualenv 
Necessario para que as dependencias do projeto nao sejam instaladas globalmente.
```
aptitude install python-dev python-pip virtualenv build-essential
```

##### Criar o virtualenv
**venv** é o diretorio do virtualenv
```
virtualenv venv
```

##### Ativar o virtualenv
```
source venv/bin/activate
```

##### Instalar os requirements da app
```
cd ../autonomous_drone_ufba/control-tower/
pip install -r requirements.txt
```

##### Criar o banco de dados
```
python dbinit.py
```


## Executar a aplicação 
Somente após preparar o ambiente.

##### Ativar o virtualenv
```
source venv/bin/activate
```

##### Inicializar a app
```
cd ../autonomous_drone_ufba/control-tower/
python run.py
```

##### Acessar a app
Abrir o browser e acessar o link **localhost:5000**. 
Caso nao funcione, utilizar o link informado no terminal.

Acessar a aplicação utilizando as credenciais:
```
user: admin@admin
password: password
```
*As credencias que são carregadas no banco de dados estão no arquivo dbinit.py.*


# Areas da APP
A aplicação contém em principio duas áreas que são **Cadastrar Missão** e **Executar Missão**.

## Cadastrar Missão
Nessa página o usuário poderá criar uma missão.
Para isso será necessário dar-se um nome a missão e selecionar a area no mapa que o drone irá percorrer. 
Ao finalizar pressionar o botão `Salvar Missão`.

A principio será necessário conexão com a internet para se carregar o maps.

## Executar Missão
Nessa página o usuário poderá criar uma missão.
Para isso o usuário selecionará um drone e uma missão. Após, pressionar o botão de executar missão.

A principio será necessário conexão com a rede do ar drone para que se possa fazer a comunicação da app pro drone.



