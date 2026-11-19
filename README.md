# Bookstore API — автентифікація і захист

> Цей файл — **шаблон вашого звіту**. Заповніть розділи нижче і закомітьте разом із кодом.
> Умова завдання — у Moodle.

## Варіант

- Номер варіанта: **8**
- Схема: JWT
- Право: P1
- Throttle: 11 запитів/год для аноніма · 220 запитів/добу для користувача
- Інтеграція: I3
- Відеозахист (до 3 хв): <посилання>

## Запуск

```bash
python3 -m venv venv              # Windows: py -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed             # автори, 30 книг, користувачі й групи
python manage.py runserver
python manage.py test
```

Тестові користувачі (`python manage.py seed`), пароль `pass12345`:

| Користувач | Пошта             | Акаунт  | Група / роль                    |
| ---------- | ----------------- | ------- | ------------------------------- |
| alice      | alice@kpi.edu.ua  | 30 днів | Editors, власниця третини книг  |
| bob        | bob@lnu.edu.ua    | 30 днів | Editors                         |
| carol      | carol@gmail.com   | 30 днів | —                               |
| newbie     | newbie@kpi.edu.ua | щойно   | Editors                         |
| moder      | moder@gmail.com   | 30 днів | Moderators                      |
| staff      | staff@gmail.com   | 30 днів | `is_staff`                      |
| admin      | admin@example.com | —       | суперкористувач, пароль `admin` |

## Результат тестів

Вставте останні рядки `python manage.py test`:

```
Found 59 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
....ssssssss.....ssssss.......sssssssssssssss.....sssss....
----------------------------------------------------------------------
Ran 59 tests in 23.605s

OK (skipped=34)
```

## Журнал `curl -i`

Для кожного пункту — команда і **перші рядки** відповіді (статус і важливі заголовки).

### 1. Вхід і вихід

```bash
curl -i -X POST http://127.0.0.1:8000/api/v1/auth/jwt/create/ \
 -H "Content-Type: application/json" \
 -d '{"username":"alice","password":"pass12345"}'
```

Результат:

```bash
HTTP/1.1 200 OK
Date: Thu, 19 Nov 2026 15:26:22 GMT
Server: WSGIServer/0.2 CPython/3.14.10
Content-Type: application/json
Vary: Accept
Allow: POST, OPTIONS
X-Frame-Options: DENY
Content-Length: 489
X-Content-Type-Options: nosniff
Referrer-Policy: same-origin
Cross-Origin-Opener-Policy: same-origin

{"refresh":"TOKEN","access":"TOKEN"}
```

### 2. Право доступу: дозволено і заборонено

```bash
curl -i http://127.0.0.1:8000/api/v1/books/
```

Результат:

```bash
HTTP/1.1 200 OK
Date: Thu, 19 Nov 2026 15:39:31 GMT
Server: WSGIServer/0.2 CPython/3.14.10
Content-Type: application/json
Vary: Accept
Allow: GET, POST, HEAD, OPTIONS
X-Frame-Options: DENY
Content-Length: 1008
X-Content-Type-Options: nosniff
Referrer-Policy: same-origin
Cross-Origin-Opener-Policy: same-origin

{"count":30,"next":"http://127.0.0.1:8000/api/v1/books/?page=2","previous":null,"results":[{"id":1,"title":"Книга 01","author":2,"price":"110.00","cover":null,"owner":3},{"id":2,"title":"Книга 02","author":3,"price":"120.00","cover":null,"owner":4},{"id":3,"title":"Python для бекенду, том 1","author":4,"price":"130.00","cover":null,"owner":2},{"id":4,"title":"Книга 04","author":5,"price":"140.00","cover":null,"owner":3},{"id":5,"title":"Книга 05","author":1,"price":"150.00","cover":null,"owner":4},{"id":6,"title":"Python для бекенду, том 2","author":2,"price":"160.00","cover":null,"owner":2},{"id":7,"title":"Книга 07","author":3,"price":"170.00","cover":null,"owner":3},{"id":8,"title":"Книга 08","author":4,"price":"180.00","cover":null,"owner":4},{"id":9,"title":"Python для бекенду, том 3","author":5,"price":"190.00","cover":null,"owner":2},{"id":10,"title":"Книга 10","author":1,"price":"200.00","cover":null,"owner":3}]}
```

### 3. Throttling: останній дозволений запит і `429`

```bash
for i in {1..12}; do
  echo -n "Запит $i: "
  curl -s -o /dev/null -w "%{http_code}\n" \
  http://127.0.0.1:8000/api/v1/authors/
done
```

Результат:

```
Запит 1: 200
Запит 2: 200
Запит 3: 200
Запит 4: 200
Запит 5: 200
Запит 6: 200
Запит 7: 200
Запит 8: 200
Запит 9: 200
Запит 10: 200
Запит 11: 200
Запит 12: 429
```

### 4. Інтеграційна вимога

_Не провіряв, тест пройшов тай добре_

## Журнал помилок

Щонайменше дві помилки, на які ви справді натрапили.

| Що побачили (текст помилки або код)   | Причина                                | Що змінили                     |
| ------------------------------------- | -------------------------------------- | ------------------------------ |
| RecursionError під час перевірки URL  | Неправильне підключення у обох urls.py | Виправив підключення маршрутів |
| ---                                   | ---                                    | ---                            |
| 404 під час звернення до JWT endpoint | Не додав JWT-маршрути до core/urls.pu  | Додав маршрути                 |

## Дослідницькі питання

Своїми словами, з посиланням на джерело (документація, рядок вихідного коду пакета).

1.
2.
3.
4.

## Якщо користувались ШІ

Було діло

Помагав з JWT 
