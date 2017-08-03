# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-03 06:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import markymark.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LegalText',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Legal text')),
                ('slug', models.SlugField(max_length=64, unique=True, verbose_name='Slug')),
            ],
            options={
                'verbose_name_plural': 'Legal texts',
                'ordering': ('name',),
                'verbose_name': 'Legal text',
            },
        ),
        migrations.CreateModel(
            name='LegalTextCheckbox',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', markymark.fields.MarkdownField(verbose_name='Text')),
            ],
            options={
                'verbose_name_plural': 'Legal text Checkboxes',
                'ordering': ('legaltext_version',),
                'verbose_name': 'Legal text checkbox',
            },
        ),
        migrations.CreateModel(
            name='LegalTextVersion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valid_from', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Valid from')),
                ('content', markymark.fields.MarkdownField(verbose_name='Text')),
                ('legaltext', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='legaltext.LegalText', verbose_name='Legal text')),
            ],
            options={
                'verbose_name_plural': 'Legal text versions',
                'ordering': ('legaltext__slug', '-valid_from'),
                'verbose_name': 'Legal text version',
            },
        ),
        migrations.AddField(
            model_name='legaltextcheckbox',
            name='legaltext_version',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='checkboxes', to='legaltext.LegalTextVersion', verbose_name='Legal text version'),
        ),
    ]
