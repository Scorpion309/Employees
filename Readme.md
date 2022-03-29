## Запуск проекта

- Установите и запустите docker.
- Скачайте проект из репозитория.
- Создайте файл .env и скопируйте в него содержимое файла .env.sample.
- В папке с файлом docker-compose.yml выполните команду:

    ```bash
    docker-compose up --build -d
    ```

- Выполните миграции базы данных, с помощью команд:

    ```bash
    docker-compose exec application python3 manage.py makemigrations --noinput
    ```

    ```bash
    docker-compose exec application python3 manage.py migrate --noinput
    ```
- Если получите следующую ошибку:

  ```
  django.db.utils.OperationalError: FATAL:  database "django_db" does not exist
  ```
- Остановите контейнер командой:

    ```bash
    docker-compose down -v
    ```
- Затем заново создайте образы, запустите контейнеры и примените миграции.

- Далее выполните создание супер пользователя, с помощью команды:

    ```bash
    docker-compose exec application python3 manage.py createsuperuser
    ```
- Запуск проекта осуществляется командой:

  ```bash
    docker-compose up
  ```

- Для проверки запуска проекта зайдите на страницу <http://localhost/admin/>.

Для загрузки данных в проект необходимо выполнить следующие действия:

- Для загрузки данных из файла fixtures/data.json выполните команду:

  ```bash
  docker-compose exec application python3 manage.py loaddata data.json
   ```
- Для генерации случайных данных и загрузки их в проект (используя модуль django-seed) выполните команду:
  ```bash
  docker-compose exec application python3 db_seeder.py --number 10 --relations 1
   ```
  где --number 10 - количество генерируемых пользователей,
      --relations 1 - флаг, указывающий на необходимость генерации и загрузки (отношений).
  
- Если не указывать параметр --number - будет сгенерировано 20 пользователей.
- Если указать параметр --relation 0 - генерации отношений не произойдет.
  (Использутся т.к. имеется проблема с генерацией случайных отношений, т.к. они могут не проходить валидацию).
