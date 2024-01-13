from django.core.mail import send_mail
from django.shortcuts import render
from django.template.loader import render_to_string

from dotenv import load_dotenv
import json
import os
import requests

from django.conf import settings

load_dotenv()


def send_motivational_quote(request):
    if request.method == "POST":
        email = request.POST.get("email")  # Extract email from form data
        response_code, response_text = fetch_motivational_quote()
        
        # Parse the JSON string into a Python object
        try:
            response_text = json.loads(response_text)
        except json.JSONDecodeError:
            # Handle the exception if the response is not a valid JSON string
            message = "Sorry, something went wrong. Please try again."
            return render(request, "home.html", {"message": message})
        
        # Extracting quote and author
        quote_text = response_text[0]['quote']
        quote_author = response_text[0]['author']
        
        if response_code != 200:
            message = "Sorry, something went wrong. Please try again."
            return render(request, "home.html", {"message": message})
        else:
            subject = "Your daily dose of inspiration"
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = email
            body = render_to_string('email_template.html', 
                                    {'quote_text': quote_text, 'quote_author': quote_author})
            send_mail(subject, body, from_email, [to_email], html_message=body)
        message = "Check your email to feel inspired!"
    else:
        message = ""

    return render(request, "home.html", {"message": message})


def fetch_motivational_quote():
    """ Invokes API Ninja's API to fetch an inspirational quote

    """
    category = 'inspirational'
    api_url = 'https://api.api-ninjas.com/v1/quotes?category={}'.format(category)
    API_NINJAS_API_KEY = os.environ.get('API_NINJAS_API_KEY')
    response = requests.get(api_url, headers={'X-Api-Key': API_NINJAS_API_KEY})
    return response.status_code, response.text
