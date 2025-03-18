# Сервис мониторинга уровня воды

![CI/CD Status](https://github.com/politeh/IoT_management/actions/workflows/main.yml/badge.svg)

Микросервис для получения и обработки данных об уровне воды от IoT устройств.

## Описание

Сервис принимает HTTP POST запросы с данными об уровне воды и обрабатывает их. При превышении критического уровня (350) выводится предупреждение. Также поддерживается сбор и визуализация метрик ESP устройств.

## Технологии

- Python 3.11
- Flask
- Docker & Docker Compose
- Nginx (для балансировки нагрузки и ограничения частоты запросов)
- Prometheus (для сбора метрик)
- Grafana (для визуализации метрик)
- GitHub Actions (CI/CD)

## Структура проекта

```
.
├── app.py                         # Основной файл приложения
├── test_app.py                    # Модульные тесты
├── requirements.txt               # Зависимости Python
├── Dockerfile                     # Конфигурация Docker
├── docker-compose.yml             # Конфигурация Docker Compose
├── docker-compose-dev.yml         # Конфигурация Docker Compose для разработки
├── nginx.conf                     # Конфигурация Nginx
├── prometheus.yml                 # Конфигурация Prometheus
├── grafana/                       # Конфигурация Grafana
│   ├── provisioning/              # Автоматическое конфигурирование
│   │   ├── datasources/           # Источники данных
│   │   └── dashboards/            # Конфигурация дашбордов
│   └── dashboards/                # JSON файлы дашбордов
└── .github/workflows              # Конфигурация CI/CD
```

## API

### Endpoint: POST /water-level

Принимает JSON-данные следующего формата:
```json
{
  "water_level": 450
}
```

#### Параметры
- `water_level`: число (целое или дробное), уровень воды

#### Ответ
```json
{
  "status": "ok"
}
```

#### Коды ответов
- 200: Успешная обработка
- 400: Ошибка в запросе (неверный формат данных)
- 500: Внутренняя ошибка сервера

### Endpoint: POST /esp-metrics

Принимает JSON-данные с метриками ESP устройства:
```json
{
  "uptime": 3600,
  "free_heap": 180000,
  "wifi_rssi": -55
}
```

#### Параметры
- `uptime`: число, время работы устройства в секундах
- `free_heap`: число, свободная память в байтах
- `wifi_rssi`: число, уровень сигнала WiFi в dBm

#### Ответ
```json
{
  "status": "ok"
}
```

#### Коды ответов
- 200: Успешная обработка
- 400: Ошибка в запросе (неверный формат данных)
- 500: Внутренняя ошибка сервера

### Endpoint: GET /health

Проверка работоспособности сервиса.

#### Ответ
```json
{
  "status": "healthy"
}
```

### Endpoint: GET /metrics

Метрики Prometheus (используется для внутреннего мониторинга).

## Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd IoT_management
```

2. Запустите через Docker Compose:
```bash
docker compose up -d
```

Сервисы будут доступны по следующим адресам:
- API: `http://localhost:5055`
- Prometheus: `http://localhost:8084`
- Grafana: `http://localhost:8085` (логин: admin, пароль: admin)

### Разработка и тестирование

Для локальной разработки и тестирования без конфликтов с основным развертыванием используйте:

```bash
docker compose -f docker-compose-dev.yml up -d
```

Сервисы для разработки будут доступны по следующим адресам:
- API: `http://localhost:5056`
- Web-интерфейс: `http://localhost:8080`
- Prometheus: `http://localhost:8086`
- Grafana: `http://localhost:8087` (логин: admin, пароль: admin)

Для запуска тестов:

```bash
pytest test_app.py
```

## Особенности

- Ограничение частоты запросов: не чаще 1 запроса в 5 секунд для /water-level
- Автоматическое развертывание при push в ветку main
- Автоматическое тестирование перед деплоем
- Масштабируемость через Docker Compose
- Поддержка дробных значений уровня воды
- Визуализация метрик ESP устройств через Grafana
- Сбор метрик с помощью Prometheus

## CI/CD

Настроен автоматический процесс тестирования и развертывания через GitHub Actions:
1. При каждом push в ветку main запускаются тесты
2. При успешном прохождении тестов происходит автоматический деплой
3. Развертывание происходит на сервере через Docker Compose

## Мониторинг

Для мониторинга используется связка Prometheus + Grafana:
1. Prometheus собирает метрики с эндпоинта /metrics
2. Grafana визуализирует собранные метрики
3. Предустановленный дашборд содержит графики:
   - Время работы ESP устройства
   - Свободная память ESP устройства
   - Уровень сигнала WiFi
   - Уровень воды

## Требования к системе

- Docker
- Docker Compose
- Доступ к портам 5055, 8084, 8085
