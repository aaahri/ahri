from django.shortcuts import render

# Create your views here.


def hello(request):
    return render(request, 'editor/ueditor/index.html')
