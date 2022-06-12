# Newsletter
Новостная лента на Django, с созданием/редактированием статей, постерами, учетными записями, комментариями, аватарами.

## Запуск
```
git clone https://github.com/interlark/django-newsletter && cd django-newsletter
 
export DJANGO_SECRET_KEY=123 

pip install -r requirements.txt

python manage.py makemigrations accounts news
python manage.py migrate
python manage.py runserver
```

### Повышение привилегий пользователя
```
sqlite3 db.sqlite3 'update auth_user set is_superuser = 1 where username = "<имя пользователя>"'
```