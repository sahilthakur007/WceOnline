# Generated by Django 4.1.1 on 2022-09-29 18:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eApp', '0004_remove_assignment_student_assignment_teacher'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='instruction',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='question',
            field=models.FileField(upload_to='assignments/pdf'),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eApp.teacher'),
        ),
        migrations.AlterField(
            model_name='student',
            name='courses',
            field=models.ManyToManyField(default='', to='eApp.course'),
        ),
        migrations.AlterField(
            model_name='student',
            name='email',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='student',
            name='firstname',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='student',
            name='lastname',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='student',
            name='mobile',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='student',
            name='password',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='submission',
            name='answer',
            field=models.FileField(upload_to='solutions/pdf'),
        ),
    ]