# README

## _Сервис пользовательских рецептов_:

### Для запуска проекта необходимо:

1. Установить Docker / Docker-compose.
Для этого можно воспользоваться официальной документацией [Docker Install](https://docs.docker.com/engine/install/)
или русскоязычной инструкцией (Debian/Ubuntu): 
[Установка Докер](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04-ru)

2. Склонировать репозиторий: 
    ```shell script
    git clone https://github.com/Balubalu27/recipes-fastapi.git
    ```

3. Находясь в корне проекта запустить команду: 
    ```shell script
    docker-compose up -d
    ```

4. После успешного запуска проекта переходим по ссылке: [API docs](http://0.0.0.0:8001/docs)

5. Доступ к API предоставляется только авторизованным пользователям. Поэтому для начала необходимо зарегистрироваться:
[Sign Up](http://0.0.0.0:8001/docs#/Auth/sign_up_auth_sign_up_post).

6. После регистрации необходимо авторизоваться, нажав Authorize и ввести указанный при регистрации логин/пароль

7. Для доступа к Admin API пользователю необходимо иметь статус суперюзера. 
Для этого необходимо в таблице users поле is_superuser выставить в True.