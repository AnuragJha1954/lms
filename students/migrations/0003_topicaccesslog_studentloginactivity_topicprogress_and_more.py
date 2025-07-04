# Generated by Django 4.2.5 on 2025-06-19 20:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0001_initial'),
        ('students', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TopicAccessLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accessed_at', models.DateTimeField(auto_now_add=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topic_access_logs', to='students.studentprofile')),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='access_logs', to='v1.topic')),
            ],
        ),
        migrations.CreateModel(
            name='StudentLoginActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login_time', models.DateTimeField(auto_now_add=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='login_activities', to='students.studentprofile')),
            ],
        ),
        migrations.CreateModel(
            name='TopicProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_completed', models.BooleanField(default=False)),
                ('completion_percentage', models.FloatField(default=0.0)),
                ('last_accessed', models.DateTimeField(auto_now=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topic_progress', to='students.studentprofile')),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='progress', to='v1.topic')),
            ],
            options={
                'unique_together': {('student', 'topic')},
            },
        ),
        migrations.CreateModel(
            name='StudentClassAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assigned_date', models.DateField(auto_now_add=True)),
                ('class_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students', to='v1.classmodel')),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='class_assignment', to='students.studentprofile')),
            ],
            options={
                'unique_together': {('student', 'class_model')},
            },
        ),
        migrations.CreateModel(
            name='ContentProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_completed', models.BooleanField(default=False)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='progress', to='v1.content')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='content_progress', to='students.studentprofile')),
            ],
            options={
                'unique_together': {('student', 'content')},
            },
        ),
    ]
