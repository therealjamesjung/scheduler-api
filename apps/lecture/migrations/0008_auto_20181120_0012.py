# Generated by Django 2.1.3 on 2018-11-19 15:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lecture', '0007_auto_20181119_2206'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.IntegerField(choices=[(0, '없음'), (1, '상경계'), (2, '인문학'), (3, '사회과학'), (4, '국방/군사/경찰'), (5, '과학/공학'), (6, '예술'), (7, '언어'), (8, '진로'), (9, '취미/생활')], default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subcategory', models.IntegerField(choices=[(0, '없음'), (1, '경제'), (2, '경영'), (3, '마케팅'), (4, '철학'), (5, '문학'), (6, '역사/문화'), (7, '행정'), (8, '심리'), (9, '교육학'), (10, '법'), (11, '사회학'), (12, '언론/신문/방송'), (13, '기계/전기/전자'), (14, '도시/토목/건설'), (15, '물리학'), (16, '생물학'), (17, '수학'), (18, '천문/지구과학'), (19, '화학'), (20, '컴퓨터'), (21, '무용'), (22, '미술'), (23, '음악'), (24, '연극/영화'), (25, '대중문화'), (26, '국어'), (27, '영어'), (28, '일본어'), (29, '중국어'), (30, '창업/취업'), (31, '진로'), (32, '논술/면접대비'), (33, '공무원/자격증'), (34, '고시'), (35, '자기능력계발'), (36, '리빙'), (37, '레저/스포츠'), (38, '여성/패션')], default=0)),
            ],
        ),
        migrations.RemoveField(
            model_name='lecture',
            name='category',
        ),
        migrations.RemoveField(
            model_name='lecture',
            name='subcategory',
        ),
        migrations.AddField(
            model_name='subcategory',
            name='lecture',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='lecture.Lecture'),
        ),
        migrations.AddField(
            model_name='category',
            name='lecture',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='lecture.Lecture'),
        ),
    ]