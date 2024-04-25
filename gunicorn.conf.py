bind = "unix:/run/gunicorn.sock"
workers = 3
accesslog = "/home/josh/logs/gunicorn.access.log"
errorlog = "/home/josh/logs/gunicorn.error.log"
capture_output = True
loglevel = "error"

