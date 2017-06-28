import uuid

import datetime
from django.contrib.auth import authenticate
from django.db import OperationalError, connection
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django_api_token.models import Token


@csrf_exempt
def token(request):
    """ The method to retrieve an API token to call further endpoints"""

    # Some validation (This could be a bit better in explicitly telling what error it was)

    if request.method != 'POST':
        return JsonResponse({'error': 'This endpoint only allows POST requests.'}, status=415)

    username = request.POST.get('username')
    password = request.POST.get('password')

    if not username:
        return JsonResponse({'error': 'You need to provide an attribute username with a value'}, status=409)

    if not password:
        return JsonResponse({'error': 'You need to provide an attribute password with a value'}, status=409)

    user = authenticate(username=username, password=password)

    # Need to have some security in a sense that clients cannot brute-force passwords
    if user is None:
        return JsonResponse({'error': 'Invalid credentials.'}, status=403)

    # Update the token
    try:
        token, created = Token.objects.get_or_create(user=user)

        # Make it expire in one hour so it can be tested
        token.expires_at = datetime.datetime.now() + datetime.timedelta(hours=1)
        token.token = uuid.uuid4().hex
        token.save()

        return JsonResponse({'token': token.token, 'expires_at': token.expires_at.isoformat()})

    except OperationalError:
        connection.close()
        return JsonResponse({'error': 'Internal problems. Please try again in a few minutes'}, status=503)

