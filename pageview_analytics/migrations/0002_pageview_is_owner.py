from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pageview_analytics', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pageview',
            name='is_owner',
            field=models.BooleanField(db_index=True, default=False),
        ),
    ]
