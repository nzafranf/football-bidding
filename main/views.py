from django.shortcuts import render

# Create your views here.
def show_main(request):
    context = {
        'npm' : '2406402542',
        'name': 'Naufal Zafran Fadil',
        'class': 'PBP F'
    }

    return render(request, "main.html", context)