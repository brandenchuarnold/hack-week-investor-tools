from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import View


class HomePageView(View):

    def dispatch(request, *args, **kwargs):
        response_text = '''\
            <html>
            <head>
                <title>Investor Tools</title>
            </head>
            <body>
                <h1>Investor Tools</h1>
                <p>Hello, world!</p>
            </body>
            </html>
        '''
        return HttpResponse(response_text)
