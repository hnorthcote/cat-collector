from django.shortcuts import render

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic  import DetailView, ListView

from .models import Cat, Toy

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def cats_index(request):
    cats = Cat.objects.all()
    return render(request, 'cats/index.html', {'cats': cats})

def cats_detail(request, cat_id):
    cat = Cat.objects.get(id=cat_id)
    return render(request, 'cats/detail.html', {'cat': cat})

class CatCreate(CreateView):
    model = Cat
    fields = '__all__'

class CatUpdate(UpdateView):
    model = Cat
    fields = ['breed', 'description', 'age']

class CatDelete(DeleteView):
    model = Cat
    success_url = '/cats/'

class ToyCreate(CreateView):
    model = Toy
    fields = '__all__'

class ToyDetail(DetailView):
    model = Toy

class ToyList(ListView):
    model = Toy

class ToyUpdate(UpdateView):
    model = Toy
    fields = '__all__'


class ToyDelete(DeleteView):
    model = Toy
    success_url = '/toys/'

