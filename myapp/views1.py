from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Publisher, Book, Member, Order


# Create your views here.
# def index(request):
#     response = HttpResponse()
#     booklist = Book.objects.all().order_by('id')[:10]
#     publisherlist = Publisher.objects.all().order_by('-city')
#     heading1 = '<h3>' + 'List of available books: ' + '</h3><br>'
#     response.write(heading1)
#     for book in booklist:
#         para = '<p>' + str(book.id) + ': ' + str(book) + '</p>'
#         response.write(para)
#     response.write('<br><h3>Publishers</h3><br>')
#     for p in publisherlist:
#         para = '<p>' + str(p.id) + ' : ' + p.name + ' ' + p.city + '</p>'
#         response.write(para)
#     return response


# def about(request):
#     response = HttpResponse()
#     response.write('<h3>This is an eBook APP</h3>')
#     return response


# def detail(request, book_id):
#     response = HttpResponse()
# 
#     book = Book.objects.all()
#     for b in book.all():
#         #print(b.id)
#         if book_id == b.id:
#             response.write('<p>Title: ' + b.title.upper() + '  Price: $' + str(b.price) + '  Publisher: ' + b.publisher.name + '</p>')
#             return response
# 
#     response.write('<p>' + str(id) + 'not found</p>')
#     return response


def index(request):
    booklist = Book.objects.all().order_by('id')[:10]
    return render(request, 'myapp/index0.html', {'booklist': booklist})


def about(request):
    return render(request, 'myapp/about0.html')


def detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'myapp/detail0.html', {'book': book})
