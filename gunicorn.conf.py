bind = "unix:/run/gunicorn.sock"
workers = 3
accesslog = "/var/log/gunicorn.access.log"
errorlog = "/var/log/gunicorn.error.log"
capture_output = True
loglevel = "error"

