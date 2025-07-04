# Generated by Django 4.2.23 on 2025-07-01 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0004_breaksystem_suspensionsystem_delete_chassisandbrakes'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Brands',
            new_name='Brand',
        ),
        migrations.RenameModel(
            old_name='Categories',
            new_name='Category',
        ),
        migrations.AlterField(
            model_name='color',
            name='hex_code',
            field=models.CharField(default='ffd', help_text='Наприклад: #FF0000', max_length=7, verbose_name='HEX код'),
            preserve_default=False,
        ),
        migrations.AlterModelTable(
            name='category',
            table='category',
        ),
    ]
