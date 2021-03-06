# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-27 11:57
from __future__ import unicode_literals

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0008_auto_20171121_1648'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Editor',
        ),
        migrations.AlterField(
            model_name='article',
            name='article_image',
            field=models.ImageField(blank=True, null=True, upload_to='articles/'),
        ),
        migrations.AlterField(
            model_name='article',
            name='post',
            field=tinymce.models.HTMLField(),
        ),
    ]
