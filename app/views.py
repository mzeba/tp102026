from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Home Page</title>
</head>
<body>
    <h1>Welcome to the Home Page</h1>
    <p>This is a simple Django application.</p>
</body>
</html>
"""


def home(request):
    return HttpResponse(HTML)
