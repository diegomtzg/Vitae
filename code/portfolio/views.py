from django.shortcuts import render

# Create your views here.
def portfolio_action(request):
    if request.method == 'GET':
        return render(request, 'portfolio/portfolio.html', {})