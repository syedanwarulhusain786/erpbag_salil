# run_all.py
from django.core.management.base import BaseCommand
import subprocess

class Command(BaseCommand):
    help = 'Run Django server and custom scripts'

    def handle(self, *args, **options):
        # Run your custom scripts sequentially
        subprocess.run(['python', 'manage.py', 'cutting'])
        subprocess.run(['python', 'manage.py', 'cutting2'])
        subprocess.run(['python', 'manage.py', 'printing'])
        subprocess.run(['python', 'manage.py', 'stictching'])
        subprocess.run(['python', 'manage.py', 'stictching2'])
        subprocess.run(['python', 'manage.py', 'packageDispatch'])

        # Start Django development server
        subprocess.run(['python', 'manage.py', 'runserver'])
