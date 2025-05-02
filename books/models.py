from django.db import models

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    PURCHASE_CHOICES = [
        ('bought', 'Bought'),
        ('borrowed', 'Borrowed'),
    ]
    STATUS_CHOICES = [
        ('read', 'Read'),
        ('reading', 'Reading'),
        ('unread', 'Unread'),
    ]

    title = models.CharField(max_length=255)
    purchase_type = models.CharField(max_length=10, choices=PURCHASE_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    rating = models.PositiveIntegerField(null=True, blank=True, help_text="Rating out of 10")
    date_started = models.DateField(null=True, blank=True)
    date_finished = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title
    
    class Meta: 
        indexes = [
            models.Index(fields=['purchase_type']),
            models.Index(fields=['status']),
            models.Index(fields=['date_finished']),
        ]


class BookTag(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('book', 'tag')  # Ensures no duplicate book-tag pairs
        # indexes = [
        #     models.Index(fields=['purchase_type']),
        #     models.Index(fields=['status']),
        #     models.Index(fields=['date_finished']),
        # ]

    def __str__(self):
        return f"{self.book.title} - {self.tag.name}"
