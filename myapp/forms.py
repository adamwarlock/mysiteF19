from django import forms

class SearchForm(forms.Form):
    CATEGORY_CHOICES = [
        ('S', 'Scinece&Tech'),
        ('F', 'Fiction'),
        ('B', 'Biography'),
        ('T', 'Travel'),
        ('O', 'Other')
    ]
    your_name = forms.CharField(max_length=100, required=False)
    select_a_category =   forms.ChoiceField(widget=forms.RadioSelect, required=False,
                                        choices = CATEGORY_CHOICES)
    maximum_price= forms.IntegerField(min_value=0)
