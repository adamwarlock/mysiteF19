from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.template.loader import render_to_string
from django.urls import reverse

from .models import Publisher, Book, Member, Order, Review
from django.http import HttpResponse, HttpResponseRedirect
from .forms import SearchForm, OrderForm, ReviewForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
import random, datetime, json, pytz


# Create your views here.
def index(request):
    if 'last_login' in request.session:
        last_login = request.session['last_login']
    else:
        last_login = 'Your last login was more that one hour ago'
    booklist = Book.objects.all().order_by('id')[:10]
    return render(request, 'myapp/index.html', {'booklist': booklist, 'last_login': last_login})


# def index(request):
#     booklist = Book.objects.all().order_by('id')[:10]
#     return render(request, 'myapp/index0.html', {'booklist': booklist})


# def about(request):
#     return render(request, 'myapp/about0.html')

def about(request):
    response = HttpResponse()
    if request.COOKIES.get('lucky_num'):
        mynum = request.COOKIES.get('lucky_num')

    else:
        mynum = random.randint(1, 100)
        response.set_cookie('lucky_num', mynum, 300)
    temp = render_to_string('myapp/about.html', {'mynum': mynum})

    response.write(temp)
    return response


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
            form.save_m2m()
            price = 0

            for b in order.books.all():
                price += b.price
                if type == 1:
                    member.borrowed_books.add(b)

            return render(request, 'myapp/order_response.html', {'books': books, 'order': order, 'price': price})
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
                book.num_reviews += 1
                book.save()
                review.save()

                return redirect('myapp:index')
            else:
                return render(request, 'myapp/review.html', {'form': form, 'ratingErr': True})

        else:
            return render(request, 'myapp/review.html', {'form': form})

    else:
        form = ReviewForm()
        return render(request, 'myapp/review.html', {'form': form})


# Import necessary classes and models


# Create your views here.
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:

                dt = datetime.datetime.now(pytz.timezone('America/Toronto'))

                request.session['last_login'] = 'Last Login: ' + json.dumps(dt, default=str)
                request.session.set_expiry(3600)
                login(request, user)
                return HttpResponseRedirect(reverse('myapp:index'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myapp/login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse(('myapp:index')))


@login_required
def chk_reviews_index(request):
    booklist = Book.objects.all().order_by('id')[:10]
    return render(request, 'myapp/chk_reviews_index.html', {'booklist': booklist})


@login_required
def chk_reviews(request, book_id):
    try:
        if Member.objects.get(id=request.user.id):
            count = 0
            rating = 0
            b = {}
            for r in Review.objects.filter(book__id=book_id):
                count += 1
                rating += r.rating
            if rating != 0:
                b['avgRating'] = round(rating / count, 2)
            else:
                b['avgRating'] = 'Not rated'

            b['title'] = Book.objects.get(id=book_id).title
            b['price'] = Book.objects.get(id=book_id).price

            return render(request, 'myapp/chk_reviews.html',
                          {'member': request.user.first_name, 'book': b})
    except Member.DoesNotExist:
        return render(request, 'myapp/chk_reviews.html')
    except Book.DoesNotExist:
        return render(request, 'myapp/chk_reviews.html', {'member': request.user.first_name})
