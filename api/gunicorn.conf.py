import gunicorn
from uvicorn.workers import UvicornWorker

# These are our gunicorn configuration settings
# Because of the naming and placement of this file, they will automatically be loaded when gunicorn starts
keepalive = 10
preload_app = True
workers = 3
timeout = 90

worker_class = 'uvicorn.workers.UvicornWorker'


# forwarded_allow_ips = '*'

# Logging
# log to stdout
accesslog = '-'
errorlog = '-'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
loglevel = 'info'
