#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import re
import sys


def read_env():
    """ Reads local default environment variables from a .env file
    located in the project root directory.
    https://gist.github.com/bennylope/2999704
    """
    try:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')) as f:
            content = f.read()
    except IOError:
        content = ''

    for line in content.splitlines():
        m1 = re.match(r'\A([A-Za-z_0-9]+)=(.*)\Z', line)
        if m1:
            key, val = m1.group(1), m1.group(2)
            m2 = re.match(r"\A'(.*)'\Z", val)
            if m2:
                val = m2.group(1)
            m3 = re.match(r'\A"(.*)"\Z', val)
            if m3:
                val = re.sub(r'\\(.)', r'\1', m3.group(1))
            os.environ.setdefault(key, val)


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cbseevents.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    read_env()
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
