# Assistant for potential clients

## Описание

Сервис для ответов на вопросы потенциальных клиентов компании EORA с учетом
некоторых материалов с сайта [компании](https://eora.ru/cases).

Интерфейс реализован в виде Telegram-бота.

## Техногогии

- Aiogram
- GigaChat

## Запуск проекта на Linux (локально)

1. Склонируйте репозиторий и перейдите в директорию проекта
    ```bash
    git clone https://github.com/mign0n/eora_assistant.git && cd eora_assistant
    ```
2. Создайте виртуальное окружение и установите зависимости
    ```bash
    make install
    ```
3. Установите необходимые переменные окружения
    ```bash
    export BOT_TOKEN=<токен-вашего-телеграм-бота>
    export GIGACHAT_CREDENTIALS=<ключ-авторизации-GigaChat>
    export GIGACHAT_VERIFY_SSL_CERTS=False
    ```
4. Запустите бота
    ```bash
    make run
    ```
