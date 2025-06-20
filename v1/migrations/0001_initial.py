# Generated by Django 4.2.5 on 2025-06-19 20:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('school', '0001_initial'),
        ('teachers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('number', models.PositiveIntegerField()),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['number'],
            },
        ),
        migrations.CreateModel(
            name='ClassModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_name', models.CharField(max_length=20)),
                ('section', models.CharField(max_length=10)),
                ('academic_year', models.CharField(max_length=20)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classes', to='school.schoolprofile')),
            ],
            options={
                'unique_together': {('school', 'class_name', 'section', 'academic_year')},
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=20, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('class_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subjects', to='v1.classmodel')),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('number', models.PositiveIntegerField()),
                ('description', models.TextField(blank=True, null=True)),
                ('is_completed', models.BooleanField(default=False)),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topics', to='v1.chapter')),
            ],
            options={
                'ordering': ['number'],
                'unique_together': {('chapter', 'number')},
            },
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('video_link', models.URLField(blank=True, null=True)),
                ('text_content', models.TextField(blank=True, null=True)),
                ('order', models.PositiveIntegerField(default=1)),
                ('is_active', models.BooleanField(default=True)),
                ('is_completed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contents', to='v1.topic')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.AddField(
            model_name='chapter',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chapters', to='v1.subject'),
        ),
        migrations.CreateModel(
            name='TeacherSubjectAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assigned_on', models.DateField(auto_now_add=True)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigned_teachers', to='v1.subject')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subject_assignments', to='teachers.teacherprofile')),
            ],
            options={
                'unique_together': {('subject', 'teacher')},
            },
        ),
        migrations.AlterUniqueTogether(
            name='chapter',
            unique_together={('subject', 'number')},
        ),
    ]
