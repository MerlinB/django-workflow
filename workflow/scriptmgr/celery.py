from __future__ import absolute_import, unicode_literals
import os
from celery import Celery, shared_task
import marshal
import types

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'workflow.settings')

app = Celery('workflow') #, broker='amqp://guest@localhost//')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


# @shared_task
@app.task
def run_fct( fct_code, *args, **kwargs ):
    try:
        code = marshal.loads( fct_code )
        func = types.FunctionType(code, globals(), "some_func_name" )
        return func( *args, **kwargs )
    except Exception as exc:
        print(exc)

class MyFunction( object ):
    def __init__(self, fct):
        self.fct_code = marshal.dumps( fct.__code__ )

    def run(self, *args, **kwargs):
        run_fct(self.fct_code, *args, **kwargs)
        # run_fct.apply_async( args=(self,)+args, kwargs=kwargs, serializer='pickle' )
