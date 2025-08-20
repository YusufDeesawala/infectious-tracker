#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from dotenv import load_dotenv

load_dotenv()

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'InfectiousTrackerBackend.settings')
    
    # Get the port from the environment variable, default to 8000 if not set
    port = os.getenv('PORT')
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # Run the Django development server with the specified port
    execute_from_command_line([sys.argv[0], 'runserver', f'0.0.0.0:{port}'])

if __name__ == '__main__':
    main()
