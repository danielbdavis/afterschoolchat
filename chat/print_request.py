from __future__ import unicode_literals, print_function

import re
import colorama


header_regex = re.compile('^HTTP_')

def print_header(key, value):
    if not value:
        return

    header = header_regex.sub('', key).replace('_', ' ').title().replace(' ', '-')
    print(colorama.Fore.CYAN, header, sep='', end='')
    print(colorama.Style.RESET_ALL, ': ', sep='', end='')
    print(colorama.Fore.YELLOW, value, sep='')


def print_request(request):
    print('\n', end='')
    print(
        colorama.Fore.GREEN,
        request.method, ' ',
        colorama.Style.RESET_ALL,
        request.path,
        sep='',
    )

    print_header('CONTENT_TYPE', request.META.get('CONTENT_TYPE'))
    print_header('CONTENT_LENGTH', request.META.get('CONTENT_LENGTH'))
    for key, value in request.META.items():
        if key.startswith('HTTP_'):
            print_header(key, request.META.get(key))
    print('\n', end='')
    print(colorama.Style.RESET_ALL, request.body, sep='')


def print_response(response):
    print('\n', end='')
    print('\n', end='')
    print(
        colorama.Fore.GREEN,
        response.status_code, ' ',
        colorama.Style.RESET_ALL,
        response.reason_phrase,
        sep='',
    )
    for key, value in response.items():
        print_header(key, value)
    print('\n', end='')
    print(colorama.Style.RESET_ALL, response.content, sep='')
    print('\n', end='')