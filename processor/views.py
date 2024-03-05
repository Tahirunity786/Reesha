from django.shortcuts import render
from core.models import ListApp, Prefdefinelist
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()


@login_required(login_url='/core/public/u/login')
def main(request):
    try:
        user = request.user
        user_account = User.objects.get(email=user)
        if user_account is not None:
            prod = ListApp.objects.filter(user=user_account).order_by("-id")
            lists = Prefdefinelist.objects.all().order_by("-id")
            return render(request, "core/app.html", {"Lists":prod, "predeflist":lists})
        else:
            render(request, "core/app.html", {"Error":"Not list found!"})
    except Exception as e:
        print("Here is the error", e)
        return render(request, "oops.html", {"Error":e})

