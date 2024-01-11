from django.shortcuts import render


def send_motivational_quote(request):
    return render(request, "home.html", \
                  {"message" : "Check your email to feel inspired!"})