# Generated by Django 4.1.7 on 2023-08-20 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
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
                ("caption", models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name="Product",
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
                ("name", models.CharField(max_length=50)),
                ("slug", models.SlugField()),
                ("price", models.IntegerField()),
                ("description", models.TextField(null=True)),
                ("excerpt", models.CharField(max_length=150, null=True)),
                ("image", models.ImageField(upload_to="images")),
                ("tags", models.ManyToManyField(to="Products.tag")),
            ],
        ),
    ]