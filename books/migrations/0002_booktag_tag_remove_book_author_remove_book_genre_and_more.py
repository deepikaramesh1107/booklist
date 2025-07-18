# Generated by Django 4.2.20 on 2025-03-27 19:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="BookTag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.RemoveField(model_name="book", name="author",),
        migrations.RemoveField(model_name="book", name="genre",),
        migrations.DeleteModel(name="Author",),
        migrations.DeleteModel(name="Genre",),
        migrations.AddField(
            model_name="booktag",
            name="book",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="books.book"
            ),
        ),
        migrations.AddField(
            model_name="booktag",
            name="tag",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="books.tag"
            ),
        ),
        migrations.AlterUniqueTogether(
            name="booktag", unique_together={("book", "tag")},
        ),
    ]
