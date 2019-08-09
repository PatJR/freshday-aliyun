from django.shortcuts import render

# Create your views here.


def test(request):
    print(request)
    return render(request, 'basetest.html', {'name': 'patrick'})


def t2(request):

    return render(request, 'son.html', {'age': '12'})
