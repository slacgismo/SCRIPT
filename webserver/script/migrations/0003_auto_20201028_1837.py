# Generated by Django 2.2.4 on 2020-10-28 18:37

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('script', '0002_auto_20201022_2007'),
    ]

    operations = [
        migrations.RenameField(
            model_name='costbenefit',
            old_name='values',
            new_name='uncontrolled_values',
        ),
        migrations.RenameField(
            model_name='emission',
            old_name='values',
            new_name='uncontrolled_values',
        ),
        migrations.RenameField(
            model_name='gasconsumption',
            old_name='values',
            new_name='uncontrolled_values',
        ),
        migrations.RenameField(
            model_name='loadprofile',
            old_name='values',
            new_name='uncontrolled_values',
        ),
        migrations.RenameField(
            model_name='netpresentvalue',
            old_name='values',
            new_name='uncontrolled_values',
        ),
        migrations.AddField(
            model_name='costbenefit',
            name='controlled_values',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={}),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='emission',
            name='controlled_values',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={}),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gasconsumption',
            name='controlled_values',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={}),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='loadprofile',
            name='controlled_values',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={}),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='netpresentvalue',
            name='controlled_values',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={}),
            preserve_default=False,
        ),
    ]
