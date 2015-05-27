# Front-end
Front-end Webapp for Vigilant

##Setup

Flask Angularjs Dashbaord

```bash
$ bower install
$ pip3 install requirements.txt

# development
$ ./dashboard.py

# optional nginx local development
$ ./nginx.sh
```

## Nginx real deployment

Nginx configuration:

```bash
$ cat /etc/nginx/sites-available/default
server {
    listen 80;
    server_name dashboard.vigilantlabs.co.uk;

    location / { try_files $uri @yourapplication; }
    location @yourapplication {
    include uwsgi_params;
        uwsgi_pass unix:/tmp/uwsgi.sock;
    }
}
```

Run the app.

```bash
$ sudo uwsgi -s /tmp/uwsgi.sock -w dashboard:app --chown-socket www-data:www-data --uid www-data --gid www-data
```
