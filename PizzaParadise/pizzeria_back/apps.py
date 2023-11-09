from django.apps import AppConfig
import os
import sys


class PizzeriaBackConfig(AppConfig):  #при запуске runserver запускается apps и запускается класс и функция, кот запустит нашу очередь в main_queue
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pizzeria_back'

    def ready(self):
        # use an environment variable to run once only
        # check for 'runserver' so migrate etc is avoided

        once_key = 'CMD_RUN_ONCE'
        run_once = os.environ.get(once_key) #запрос на разрешения выполнения 1 раз

        if run_once is not None or 'runserver' not in sys.argv:
            return True

        os.environ[once_key] = 'True'

        # import is done only here after models are loaded
        from pizzeria_back.main_queue_engine import schedule  # run once выполняется из корневой папки PizzaParadise, поэтому нужен путь из корневой папки
        schedule()

        # запускаем вторую очередь один раз
        from pizzeria_back.processing_queue_engine import schedule  # run once выполняется из корневой папки PizzaParadise, поэтому нужен путь из корневой папки
        schedule()

        # запускаем, плдключаем очередь transfer_queue_engine
        from pizzeria_back.transfer_queue_engine import schedule
        schedule()