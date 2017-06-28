import datetime

import re
from django.http.response import JsonResponse

from django_api_token.models import Token


def valid_api_token_cbv(original_function):
    """ A decorator to validate if the token is still valid that should be provided in the header """

    def _wrapper(*args, **kwargs):
        self, request, _ = args[0], args[1], args[2:]

        # Check if the request has the token in the header and if it has a value
        token_string = request.META.get('HTTP_AUTHORIZATION', '')

        if not token_string or not re.match('(B|b)earer [a-f0-9]{32}', token_string):
            return JsonResponse({'error': 'Please provide a bearer token!'}, status=403)

        # This actually checks the bearer token - would be useful to cache here
        try:
            token_string = token_string.split(' ')[1]

            token = Token.objects.get(token=token_string)

            if token.expires_at > datetime.datetime.now():
                # Call the original function and add the token as a second argument
                kwargs.update({'token': token})
                return original_function(*[self, request] + list(_), **kwargs)
            else:
                return JsonResponse({'error': 'Token expired. Please renew your token!'}, status=403)

        except Token.DoesNotExist:
            return JsonResponse({'error': 'Invalid token!'}, status=403)

    return _wrapper


def valid_api_token_view(original_function):
    """ A decorator to validate if the token is still valid that should be provided in the header """

    def _wrapper(*args, **kwargs):
        request, _ = args[0], args[1:]

        # Check if the request has the token in the header and if it has a value
        token_string = request.META.get('HTTP_AUTHORIZATION', '')

        if not token_string or not re.match('(B|b)earer [a-f0-9]{32}', token_string):
            return JsonResponse({'error': 'Please provide a bearer token!'}, status=403)

        # This actually checks the bearer token - would be useful to cache here
        try:
            token_string = token_string.split(' ')[1]

            token = Token.objects.get(token=token_string)

            if token.expires_at > datetime.datetime.now():
                # Call the original function and add the token as a second argument
                kwargs.update({'token': token})
                return original_function(*[request] + list(_), **kwargs)
            else:
                return JsonResponse({'error': 'Token expired. Please renew your token!'}, status=403)

        except Token.DoesNotExist:
            return JsonResponse({'error': 'Invalid token!'}, status=403)

    return _wrapper

def valid_date(date_string):
    """ Simple helper for date checking """
    try:
        return datetime.datetime.strptime(date_string, '%Y-%m-%d')
    except:
        return