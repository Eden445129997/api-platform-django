# Generated by Django 3.0.6 on 2020-11-16 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qa_platform', '0020_auto_20201116_0012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='api',
            name='method',
            field=models.CharField(choices=[('GET', 'GET'), ('POST', 'POST'), ('PUT', 'PUT'), ('DELETE', 'DELETE')], max_length=255, verbose_name='请求方式'),
        ),
    ]