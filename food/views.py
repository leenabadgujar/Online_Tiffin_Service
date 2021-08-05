from django.shortcuts import redirect, render

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        return render(request, 'food/home.html')
    
    else:
        return redirect('login')