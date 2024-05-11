from celery import Celery
from flask import app

def make_celery(app=None):
  app = app or current_app
  celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
  celery.conf.update(app.config)
  celery.config.update({
      'CELERY_RESULT_BACKEND': app.config['CELERY_RESULT_BACKEND'],
  })
  celery.init_app(app)
  return celery

app = Flask(__name__)
app.config.update({
    'CELERY_BROKER_URL': 'redis://localhost:6379',  # Adjust if using a different Redis instance
    'CELERY_RESULT_BACKEND': 'redis://localhost:6379',  # Adjust if using a different Redis instance
})

celery = make_celery(app)
