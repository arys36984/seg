from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from random import choice
from loans.models import Book
from loans.forms import BookForm
from django.core.paginator import Paginator

ITEMS_PER_PAGE = 25

# Create your views here.
def welcome(request):
    slogans = ["Libraries make shhh happen.",
               "Believe in your shelf.",
               "Need a good read? We've got you covered.",
               "Check us out. And maybe one of our books too.",
               "Get a better read on the world.",
               "Having fun isn't hard when you've got a library card"]

    context = {'slogan':choice(slogans)}
    return render(request, 'welcome.html', context)

def books(request):
    book_list = Book.objects.all().order_by('id')
    paginator = Paginator(book_list, ITEMS_PER_PAGE)
    page_number = request.GET.get("page")
    page_object = paginator.get_page(page_number)
    context = {'page_object': page_object}
    return render(request, 'books.html', context)

def get_book(request, book_id):
    try:
        book = Book.objects.get(pk = book_id)
        context = {'book':book}
        return render(request, 'book.html', context)
    except Book.DoesNotExist:
        raise Http404(f"Could not find book with primary key {book_id}")
    
def create_book(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except:
                form.add_error(None, "The book was not saved.")
            else:
                path = reverse('books')
                return HttpResponseRedirect(path)
        else:
            return render(request, 'create_book.html', {'form': form})
    else:
        form = BookForm()
        return render(request, 'create_book.html', {'form': form})

def update_book(request, book_id):
    try:
        book = Book.objects.get(pk = book_id)
    except Book.DoesNotExist:
        raise Http404(f"Could not find book with primary key {book_id}")
    else:
        if request.method == "POST":
            form = BookForm(request.POST, instance=book)
            if form.is_valid():
                try:
                    form.save()
                except:
                    form.add_error(None, "The book was not updated.")
                else:
                    path = reverse('books')
                    return HttpResponseRedirect(path)
        else:
            form = BookForm(instance=book)
            return render(request, 'update_book.html', {'form': form})

def delete_book(request, book_id):
    book = Book.objects.get(pk = book_id)
    if request.method == "POST":
        book.delete()
        path = reverse('books')
        return HttpResponseRedirect(path)
    else:
        return render(request, 'delete_book.html', {'book': book})

    