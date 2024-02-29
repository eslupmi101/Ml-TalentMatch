# ResParse by Team Pixel

## Кейс 1. Алгоритм для структурирования информации в резюме кандидатов [ML TalentMatch]

![Скриншот фронтенда](https://github.com/eslupmi101/Ml-TalentMatch/blob/main/image.jpg)

### Описание:

Сервис для обработки резюме и получения данных в фиксированном json

### Как запустить проект локально

Скопировать .env.example в рабочий .env

```
cp .env.example .env
```

Запустить проект через docker

```
docker-compose -f docker-compose.yml up -d
```

### Получить ответ через http API

В таком видео будет работать http API через который можно будет получать json response. Например через Postman

- Отправить запрос по endpoint - localhost:8001/api/v1/resumes/
- Добавить в тело запроса file - файл с резюме и api_key - токен ChatGPT

### Получить ответ через веб интерфейс

Дождаться пока фронтенд запустится и подключиться к хосту

```
localhost:3000
```

# Команда

Андреев Айсен - backend developer @aisen_andreev

Слепцов Гаврил - ML developer @NaeSaLaN6

Ужинский Николай - ML developer @koluzh
