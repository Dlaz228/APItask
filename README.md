<h1 align="center">APItask</h1>

<p align="center">
  Проект представляет собой REST API для управления рулонами и статистикой. Реализован с использованием FastAPI, SQLAlchemy и Alembic.
</p>

---

<h2>Выполненные пункты</h2>

<ul>
  <li>
    <strong>1. RESTFull API:</strong>
    <ul>
      <li>a. Добавление нового рулона на склад. Длина и вес — обязательные параметры. В случае успеха возвращает добавленный рулон.</li>
      <li>b. Удаление рулона с указанным id со склада. В случае успеха возвращает удалённый рулон.</li>
      <li>c. Получение списка рулонов со склада с возможностью фильтрации по одному из диапазонов (id/веса/длины/даты добавления/даты удаления со склада).</li>
      <li>d. Получение статистики по рулонам за определённый период:
        <ul>
          <li>Количество добавленных рулонов.</li>
          <li>Количество удалённых рулонов.</li>
          <li>Средняя длина и вес рулонов, находившихся на складе в этот период.</li>
          <li>Максимальная и минимальная длина и вес рулонов, находившихся на складе в этот период.</li>
          <li>Суммарный вес рулонов на складе за период.</li>
          <li>Максимальный и минимальный промежуток между добавлением и удалением рулона.</li>
        </ul>
      </li>
    </ul>
  </li>
  <li>
    <strong>2. Данные по рулонам хранятся в базе данных PostgreSQL.</strong>
  </li>
  <li>
    <strong>3. Обработаны стандартные кейсы ошибок:</strong>
    <ul>
      <li>Недоступна БД.</li>
      <li>Рулон не существует при попытке работы с ним.</li>
    </ul>
  </li>
  <li>
    <strong>4. Используемый стек:</strong>
    <ul>
      <li>FastAPI</li>
      <li>SQLAlchemy</li>
      <li>Pydantic (версия 2.0+)</li>
    </ul>
  </li>
  <li>
    <strong>Бонусные баллы:</strong>
    <ul>
      <li>1. Получение списка рулонов с фильтрацией работает по комбинации нескольких диапазонов сразу.</li>
      <li>2. Получение статистики по рулонам дополнительно возвращает:
        <ul>
          <li>День, когда на складе находилось минимальное и максимальное количество рулонов за указанный период.</li>
          <li>День, когда суммарный вес рулонов на складе был минимальным и максимальным в указанный период.</li>
        </ul>
      </li>
      <li>4. Конфигурации к подключению к БД настраиваются через ENV.</li>
      <li>5. Проект покрыт тестами.</li>
    </ul>
  </li>
</ul>

<h3>Не выполнено:</h3>
<ul>
  <li>3. Проект не обёрнут в Docker (с виндой не получилось быстро разобраться).</li>
  <li>6. Проект проходит mypy, flake8 и прочее (не успел).</li>
</ul>

---

<h2>Структура проекта</h2>

<p>Проект организован следующим образом:</p>

<h3>Основные директории и файлы</h3>

<ul>
  <li>
    <strong><code>src/</code></strong><br>
    Основной код приложения.<br>
    Включает:
    <ul>
      <li>
        <strong><code>rolls/</code></strong><br>
        Модуль для работы с рулонами:
        <ul>
          <li><code>models.py</code> — модели SQLAlchemy для рулонов.</li>
          <li><code>schemas.py</code> — Pydantic схемы для валидации данных.</li>
          <li><code>service.py</code> — бизнес-логика для работы с рулонами.</li>
          <li><code>router.py</code> — FastAPI роутеры для рулонов.</li>
        </ul>
      </li>
      <li>
        <strong><code>stats/</code></strong><br>
        Модуль для работы со статистикой:
        <ul>
          <li><code>models.py</code> — модели SQLAlchemy для статистики.</li>
          <li><code>schemas.py</code> — Pydantic схемы для статистики.</li>
          <li><code>service.py</code> — бизнес-логика для статистики.</li>
          <li><code>router.py</code> — FastAPI роутеры для статистики.</li>
        </ul>
      </li>
      <li><strong><code>database.py</code></strong> — настройки базы данных и подключения.</li>
      <li><strong><code>exceptions.py</code></strong> — пользовательские исключения.</li>
      <li><strong><code>config.py</code></strong> — конфигурация приложения.</li>
      <li><strong><code>main.py</code></strong> — точка входа в приложение.</li>
    </ul>
  </li>
  <li>
    <strong><code>tests/</code></strong><br>
    Тесты для приложения.<br>
    Включает:
    <ul>
      <li>
        <strong><code>rolls/</code></strong><br>
        Тесты для модуля рулонов:
        <ul>
          <li><code>test_router.py</code> — тесты для роутеров.</li>
          <li><code>test_service.py</code> — тесты для сервисов.</li>
        </ul>
      </li>
      <li>
        <strong><code>stats/</code></strong><br>
        Тесты для модуля статистики:
        <ul>
          <li><code>test_router.py</code> — тесты для роутеров.</li>
          <li><code>test_service.py</code> — тесты для сервисов.</li>
        </ul>
      </li>
      <li><strong><code>__init__.py</code></strong> — инициализация тестов.</li>
    </ul>
  </li>
  <li>
    <strong><code>alembic/</code></strong><br>
    Управление миграциями базы данных.<br>
    Включает:
    <ul>
      <li><strong><code>versions/</code></strong> — файлы миграций.</li>
      <li><strong><code>env.py</code></strong> — настройки Alembic.</li>
      <li><strong><code>alembic.ini</code></strong> — конфигурация Alembic.</li>
    </ul>
  </li>
  <li><strong><code>requirements.txt</code></strong> — список зависимостей проекта.</li>
  <li><strong><code>README.md</code></strong> — описание проекта (этот файл).</li>
</ul>

---

<h2>Установка и запуск</h2>

<h3>1. Клонирование репозитория</h3>

<p>Склонируйте репозиторий на ваш компьютер:</p>

<pre><code>git clone https://github.com/Dlaz228/APItask.git
cd APItask</code></pre>

<h3>2. Установка зависимостей</h3>

<p>Установите необходимые зависимости:</p>

<pre><code>pip install -r requirements.txt</code></pre>

<h3>3. Конфигурации к подключению к БД и выбор хоста/порта для сервера uvicorn </h3>

<p>Необходимо создать файл .env в корневой папке проекта:</p>

<pre><code>DB_HOST=localhost
DB_PORT=YOUR_DB_PORT
DB_USER=YOUR_DB_USER
DB_PASS=YOUR_DB_PASS
DB_NAME=YOUR_DB_NAME
APP_HOST=YOUR_APP_HOST
APP_PORT=YOUR_APP_PORT</code></pre>

<h3>4. Настройка базы данных</h3>

<p>База данных и таблица для неё должны создаться автоматически при запуске</p>

<h3>5. Запуск приложения</h3>

<p>Запустите сервер FastAPI:</p>

<pre><code>python src/main.py</code></pre>

---

<h2>Использование API</h2>

<h3>Документация</h3>

<p>После запуска сервера вы можете получить доступ к документации API:</p>

  <p>Пример: <strong>Swagger UI</strong>: <a href="http://127.0.0.1:8000/docs">http://127.0.0.1:8000/docs</a></p>

<h3>Примеры запросов</h3>

<h4>Создание нового рулона</h4>

<pre><code>curl -X POST "http://127.0.0.1:8000/rolls/CreateNewRoll/" \
-H "Content-Type: application/json" \
-d '{"length": 10.0, "weight": 5.0}'</code></pre>

---

<h2>Запуск тестов</h2>

<p>Для запуска тестов выполните:</p>

<pre><code>pytest --cov=src/rolls tests/rolls/
pytest --cov=src/stats tests/stats/</code></pre>

---

<h2>Используемые технологии</h2>

<ul>
  <li><strong>FastAPI</strong> — фреймворк для создания API.</li>
  <li><strong>SQLAlchemy</strong> — ORM для работы с базой данных.</li>
  <li><strong>Alembic</strong> — управление миграциями базы данных.</li>
  <li><strong>Pydantic</strong> — валидация данных.</li>
  <li><strong>Pytest</strong> — тестирование.</li>
</ul>
