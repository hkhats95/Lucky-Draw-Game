# Generated by Django 3.2 on 2021-04-27 20:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lucky_draw', '0003_auto_20210428_0044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='raffleticket',
            name='luckydraw',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tickets', to='lucky_draw.luckydraw'),
        ),
    ]
