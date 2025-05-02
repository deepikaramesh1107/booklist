

from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.db import connection
from .models import Book, Tag, BookTag
from .forms import BookForm, TagForm
from django.db.models import Avg, Count, Min, Max, F, ExpressionWrapper, DurationField
from django.utils.timezone import now
from datetime import timedelta

def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()

            # Add the selected tags
            selected_tags = form.cleaned_data['tags']
            for tag in selected_tags:
                BookTag.objects.create(book=book, tag=tag)

            return redirect('book_list')

    else:
        form = BookForm()

    return render(request, 'books/book_form.html', {'form': form})


def tag_create(request):
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save()
            next_url = request.GET.get('next', 'book_create')  # Default to book_create if next is not provided
            return redirect(next_url)

    else:
        form = TagForm()
    
    return render(request, 'books/tag_form.html', {'form': form})



def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)

    # Get the tags currently associated with the book
    existing_tags = Tag.objects.filter(booktag__book=book)

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            book = form.save()

            # Clear existing tags
            BookTag.objects.filter(book=book).delete()

            # Add the selected tags using a prepared statement
            selected_tags = form.cleaned_data['tags']
            with connection.cursor() as cursor:
                cursor.executemany(
                    "INSERT INTO books_booktag (book_id, tag_id) VALUES (?, ?)",
                    [(book.id, tag.id) for tag in selected_tags]
                )

            return redirect('book_list')  # Redirect to book list or any desired page

    else:
        form = BookForm(instance=book)
        form.fields['tags'].queryset = Tag.objects.all()  # Ensure all tags are available
        form.initial['tags'] = existing_tags

    return render(request, 'books/book_edit.html', {'form': form, 'book': book})



def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list') 
    return render(request, 'books/book_confirm_delete.html', {'book': book})

def book_list(request):
    purchase_type = request.GET.get('purchase_type')
    tag_id = request.GET.get('tag_id')

    books = Book.objects.all()

    if purchase_type:
        books = books.filter(purchase_type=purchase_type)

    if tag_id:
        books = books.filter(booktag__tag__id=tag_id)

    # For filter buttons
    purchase_types = Book.objects.values_list('purchase_type', flat=True).distinct()
    tags = Tag.objects.all()

    avg_rating = books.aggregate(Avg('rating'))['rating__avg']

    last_book = books.filter(date_finished__isnull=False).order_by('-date_finished').first()

    total_bought = books.filter(purchase_type='bought').count()
    borrowed_books = books.filter(purchase_type='borrowed').count()

    # Least favorite book (lowest non-null rating)
    least_favorite = books.exclude(rating__isnull=True).order_by('rating').first()

    # Book that took the least time to finish
    from django.db.models.functions import Cast
    finished_books = books.exclude(date_started__isnull=True).exclude(date_finished__isnull=True).annotate(
        duration=ExpressionWrapper(F('date_finished') - F('date_started'), output_field=DurationField())
    ).order_by('duration')

    quickest_book = finished_books.first()

    total_books = Book.objects.count()
    completed_books = Book.objects.filter(status='read').count()

    # Most frequent tag (based on tag usage in filtered book list)
    from django.db.models import Count
    tag_counts = BookTag.objects.filter(book__in=books).values('tag__name').annotate(count=Count('tag')).order_by('-count')
    most_frequent_tag = tag_counts.first()['tag__name'] if tag_counts else None

    context = {
        'books': books,
        'purchase_types': purchase_types,
        'tags': tags,
        'selected_purchase_type': purchase_type,
        'selected_tag_id': tag_id,
        'avg_rating': round(avg_rating, 2) if avg_rating else None,
        'last_book': last_book,
        'least_favorite': least_favorite,
        'quickest_book': quickest_book,
        'total_bought': total_bought,
        'borrowed_books': borrowed_books,
        'completed_books': completed_books,
        'most_frequent_tag': most_frequent_tag,
    }

    return render(request, 'books/book_list.html', {
        'books': books,
        'purchase_types': purchase_types,
        'tags': tags,
        'selected_purchase_type': purchase_type,
        'selected_tag_id': tag_id,
        'avg_rating': round(avg_rating, 2) if avg_rating else None,
        'last_book': last_book,
        'least_favorite': least_favorite,
        'quickest_book': quickest_book,
        'total_bought': total_bought,
        'borrowed_books': borrowed_books,
        'completed_books': completed_books,
        'most_frequent_tag': most_frequent_tag,
    })


    # books = Book.objects.all()
    # return render(request, 'books/book_list.html', {'books': books})




