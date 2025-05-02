from django import forms
from .models import Book, Tag, BookTag

class BookForm(forms.ModelForm):

    date_started = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}), required=False
    )
    date_finished = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}), required=False
    )

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Book
        fields = ['title', 'purchase_type', 'status', 'rating', 'date_started', 'date_finished', 'tags']

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']

