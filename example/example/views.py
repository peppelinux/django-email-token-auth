from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse


@login_required
def home(request):
    return HttpResponse('Home page - {}'.format(request.user.email))
