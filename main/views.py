from django.shortcuts import render
from .forms import RoteiroForm 

def roteiro(request):
    if request.method == 'POST':
        form = RoteiroForm(request.POST)
        if form.is_valid():
            form.save() 
            return render(request, 'index.html')
    else:
        form = RoteiroForm()
    return render(request, 'index.html', {'form': form})
