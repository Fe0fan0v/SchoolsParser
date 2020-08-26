# Установка и запуск скрипта на сервере Wordpress

1. В wordpress устанавливаем плагин Insert PHP
2. Вставляем `main.py` и `requirements.txt` в папку с плагином
3. В нужную страницу вставляем код, где указываем полный путь по питонного скрипта:  
`[insert_php]`   
`$requirements = 'pip install -r requirements.txt';`  
`$python = 'python /home/user/main.py';`  
`echo $requirements;`  
`echo $python;`  
`[/insert_php]`  
При загрузке этой страницы скрипт должен срабатывать.

