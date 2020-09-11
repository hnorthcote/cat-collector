from django.shortcuts import render, redirect

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic  import DetailView, ListView

import uuid
import boto3

from .models import Cat, Toy, Photo
from .forms import FeedingForm


S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'catcollector-seir-629'

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def cats_index(request):
    cats = Cat.objects.all()
    return render(request, 'cats/index.html', {'cats': cats})

def cats_detail(request, cat_id):
    
    cat = Cat.objects.get(id=cat_id)
    feeding_form = FeedingForm()
    toys_cat_doesnt_have = Toy.objects.exclude(id__in=cat.toys.all().values_list('id'))

    return render(request, 'cats/detail.html', {
        'cat': cat,
        'feeding_form': feeding_form,
        'toys': toys_cat_doesnt_have
    })

def add_feeding(request, cat_id):
    form = FeedingForm(request.POST)

    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.cat_id = cat_id
        new_feeding.save()
    
    return redirect('detail', cat_id=cat_id)

def add_photo(request, cat_id):
    # Collect the photo asset from the request
    photo_file = request.FILES.get('photo-file', None)

    # check if a photo asset was provided
    if photo_file:
        # make the s3 utility available locally to this view function
        s3 = boto3.client('s3')
        # create a key that will be used to add a unique identifier to our photo asset
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]

        try:
            # attempt to upload the file to aws
            s3.upload_fileobj(photo_file, BUCKET, key)
            #create the unique photo asset url
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            # create an instance the photo model in memory
            photo = Photo(url=url, cat_id=cat_id)
            # save the photo model
            photo.save()

        except:
            # something went wrong - gracefully do something else
            print('An error occurred uploading file to s3')
    
    return redirect('detail', cat_id=cat_id)




def assoc_toy(request, cat_id, toy_id):
    Cat.objects.get(id=cat_id).toys.add(toy_id)
    return redirect('detail', cat_id=cat_id)


def unassoc_toy(request, cat_id, toy_id):
    Cat.objects.get(id=cat_id).toys.remove(toy_id)
    return redirect('detail', cat_id=cat_id)
    

class CatCreate(CreateView):
    model = Cat
    fields = ['name', 'breed', 'description', 'age']

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

