# Generated by Django 3.1.4 on 2021-04-07 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agravamento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datahora_cadastro', models.DateTimeField(auto_now_add=True)),
                ('datahora_alteracao', models.DateTimeField(auto_now=True)),
                ('titulo', models.CharField(max_length=144)),
                ('descricao', models.TextField()),
                ('fator', models.IntegerField()),
                ('imagem', models.ImageField(blank=True, null=True, upload_to='image_fatores/', verbose_name='Imagem')),
            ],
            options={
                'ordering': ['-datahora_cadastro'],
            },
        ),
    ]
