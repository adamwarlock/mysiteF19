from django.shortcuts import render, get_object_or_404, redirect
from .models import Publisher, Book, Member, Order
from django.http import HttpResponse
from .forms import SearchForm, OrderForm, ReviewForm


# Create your views here.
def index(request):
    booklist = Book.objects.all().order_by('id')[:10]
    return render(request, 'myapp/index.html', {'booklist': booklist})


# def index(request):
#     booklist = Book.objects.all().order_by('id')[:10]
#     return render(request, 'myapp/index0.html', {'booklist': booklist})


# def about(request):
#     return render(request, 'myapp/about0.html')

def about(request):
    return render(request, 'myapp/about.html')


def detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'myapp/detail.html', {'book': book})


# def detail(request, book_id):
#     book = get_object_or_404(Book, id=book_id)
#     return render(request, 'myapp/detail0.html', {'book': book})


def findbooks(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            CATEGORY_CHOICES = {
                'S': 'Scinece&Tech',
                'F': 'Fiction',
                'B': 'Biography',
                'T': 'Travel',
                'O': 'Other'
            }
            name = form.cleaned_data['your_name']
            category = form.cleaned_data['select_a_category']
            price = form.cleaned_data['maximum_price']
            if category:
                booklist = Book.objects.filter(category=category, price__lte=price)
                return render(request, 'myapp/results.html',
                              {'booklist': booklist, 'name': name, 'category': CATEGORY_CHOICES[category]})
            else:
                booklist = Book.objects.filter(price__lte=price)
                return render(request, 'myapp/results.html', {'booklist': booklist, 'name': name})
        else:
            return HttpResponse('Invalid data')
    else:
        form = SearchForm()
        return render(request, 'myapp/findbooks.html', {'form': form})


def place_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            books = form.cleaned_data['books']
            order = form.save(commit=False)
            member = order.member
            type = order.order_type
            order.save()

            if type == 1:
                for b in books:
                    member.borrowed_books.add(b)

            form.save_m2m()

            return render(request, 'myapp/order_response.html', {'books': books, 'order': order})
        else:
            return render(request, 'myapp/placeorder.html', {'form': form})

    else:
        form = OrderForm()
        return render(request, 'myapp/placeorder.html', {'form': form})


def review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data['rating']
            if 1 <= rating <= 5:
                review = form.save(commit=False)
                book = review.book
                book.num_reviews+=1
                book.save()
                review.save()

                return redirect('myapp:index')
            else:
                return render(request, 'myapp/review.html', {'form': form, 'ratingErr': True})
            # books = form.cleaned_data['books']
            # order = form.save(commit=False)
            # member = order.member
            # type = order.order_type
            # order.save()
            # if type == 1:
            #     for b in order.books.all():
            #         member.borrowed_books.add(b)
            #     #member.save()
            #
            # form.save_m2m()


        else:
            return render(request, 'myapp/review.html', {'form': form})

    else:
        form = ReviewForm()
        return render(request, 'myapp/review.html', {'form': form})
