# Generated by Django 3.0.6 on 2020-11-12 08:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('qa_platform', '0006_auto_20201112_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apiassert',
            name='data_id',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='qa_platform.Project'),
        ),
        migrations.AlterField(
            model_name='apiassert',
            name='model_id',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='qa_platform.Project'),
        ),
        migrations.AlterField(
            model_name='b',
            name='a',
            field=models.ForeignKey(db_column='test', db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='qa_platform.A'),
        ),
    ]