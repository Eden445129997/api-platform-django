# Generated by Django 3.0.6 on 2020-11-12 07:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('qa_platform', '0003_auto_20201112_1528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='b',
            name='a',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='qa_platform.A'),
        ),
        migrations.AlterField(
            model_name='host',
            name='project_id',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='qa_platform.Project'),
        ),
    ]