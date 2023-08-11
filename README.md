# Djagno-Adminlte Raspberry


## Configuraciones de Raspberry para Desplegar Django-Adaminlte-3 en Apache2

* `sudo apt-get update`
* `sudo apt-get install apache2`
* `sudo apt-get install libapache2-mod-wsgi-py3`

### .venv
* `sudo apt-get install python3-pip`
* `sudo pip install virtualenv`
* `pip install virutalenv`
* `virtualenv .venv`
* `source .venv/bin/activate`
* `pip install -r requirements.txt`

## Django
* `python manage.py makemigrations`
* `python manage.py migrate`
* `python manage.py collectstatic`



### Apache2
* `sudo nano /etc/apache2/ports.conf`
```
...
Listen #
```

* `sudo nano /etc/apache2/sites-available/file.conf`

```
<VirtualHost *: # >
    Alias /static/ /dir/static/
	<Directory /dir/static>
		Require all granted
	</Directory>

	WSGIScriptAlias / /dir/config/wsgi.py
	WSGIDaemonProcess django python-path=/dir python-home=/dir/.venv
	WSGIProcessGroup django
	WSGIScriptAlias / /dir/config/wsgi.py

	<Directory /dir//config>
		<Files wsgi.py>
			Require all granted
		</Files>
	</Directory>
</VirtualHost>
```
* `sudo a2ensite EAS_HDCA.conf`
* `sudo systemctl reaload apache2`

### Permisos
* `sudo chmod 664 ./db.sqlite3`
* `sudo chmod 777 ./`
* `sudo chown :www-data ./db.sqlite3`
* `sudo chown :www-data ./`
* `sudo service apache2 restart`
