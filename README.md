# Newsletter
Новостная лента на Django, с созданием/редактированием статей, постерами, учетными записями, комментариями, аватарами.

<details>
  <summary>Скриншоты</summary>
  <img alt="Main list" src="https://user-images.githubusercontent.com/20641837/173237295-c38a2889-163c-4400-b2ad-52e15e59e93e.png"/>
  <img alt="Comments" src="https://user-images.githubusercontent.com/20641837/173237291-0165350c-a220-4c52-9b40-0e1b3c9b1278.png"/>
</details>

## Запуск
```bash
git clone https://github.com/interlark/django-newsletter && cd django-newsletter
 
export DJANGO_SECRET_KEY=123 

pip install -r requirements.txt

python manage.py makemigrations accounts news
python manage.py migrate
python manage.py runserver
```

## Повышение привилегий пользователя
```bash
sqlite3 db.sqlite3 'update auth_user set is_superuser = 1 where username = "<имя пользователя>"'
```
