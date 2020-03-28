# API Desafio Coopersystem

[Python](https://www.python.org/) - **3.6.0**

[Django](https://www.djangoproject.com/) - **2.2.5**

[Django RestFramework](https://www.django-rest-framework.org/) - 3.9.4

[Docker]() - **18.09.7**

[docker-compose --version]() - **1.24.1** 


## Criar o .env da aplicação:

1. Criar o ponto o .env no diretório do manage.py \
**Arquivo do .env será enviado por email**

## Instalação do Desafio com Docker
- Executar o seguinte comando para baixar as depedencias da api:
```
make build
```
- Execute o seguinte comando para subir a imagem do postgresql: 
```
make up-postgresql
```
- Executar os seguintes comandos para criar o banco de dados no postgresql (em sequência):
```
make create-role
```
```
make alter-role
```
```
make create-db
```
- Para subir os ambientes virtuais, execute:
 
```
make up
```

- Para subir os ambientes em modo de desenvolvimento, execute:
 
```
make run

```
- Verificar se os containers estão rodando sem falhas `docker ps`


     
    
### produto:
  * Urls: 
        * api/produto/ \
            * / \
            * /create \
            * /detail-update/{id} \
            * /delete/{id}
### predido:
  
  * Urls: 
        * api/produto/ \
            * / \
            * /create \
            * /detail-update/{id} \
            * /delete/{id}


      
