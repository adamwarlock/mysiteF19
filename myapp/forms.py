from django import forms
from myapp.models import Order, Review


class SearchForm(forms.Form):
    CATEGORY_CHOICES = [
        ('S', 'Scinece&Tech'),
        ('F', 'Fiction'),
        ('B', 'Biography'),
        ('T', 'Travel'),
        ('O', 'Other')
    ]
    your_name = forms.CharField(max_length=100, required=False)
    select_a_category = forms.ChoiceField(widget=forms.RadioSelect, required=False,
                                          choices=CATEGORY_CHOICES)
    maximum_price = forms.IntegerField(min_value=0)


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['books', 'member', 'order_type']
        widgets = {'books': forms.CheckboxSelectMultiple(), 'order_type': forms.RadioSelect}
        labels = {'member': u'Member name', }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['reviewer', 'book', 'rating', 'comments']
        widgets = {'reviewer': forms.EmailInput, 'book': forms.RadioSelect,
                   'rating': forms.NumberInput,
                   'comments': forms.Textarea}
        labels = {'reviewer': u'Please enter a valid email',
                  'rating': u'Rating: An integer between 1 (worst) and 5 (best)'}
