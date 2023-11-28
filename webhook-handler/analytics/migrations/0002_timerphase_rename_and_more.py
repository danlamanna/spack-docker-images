# Generated by Django 4.2.4 on 2023-08-24 20:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("analytics", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel("Phase", "TimerPhase"),
        migrations.AddConstraint(
            model_name="timer",
            constraint=models.UniqueConstraint(
                fields=("hash", "name", "job"), name="unique-hash-name-job"
            ),
        ),
        migrations.AddConstraint(
            model_name="timer",
            constraint=models.CheckConstraint(
                check=models.Q(
                    models.Q(
                        ("cache__isnull", True),
                        ("hash__isnull", True),
                        ("name__startswith", "."),
                    ),
                    models.Q(
                        models.Q(("name__startswith", "."), _negated=True),
                        ("cache__isnull", False),
                        ("hash__isnull", False),
                    ),
                    _connector="OR",
                ),
                name="internal-timer-consistent-hash-and-cache",
            ),
        ),
        migrations.AddField(
            model_name="timerphase",
            name="is_subphase",
            field=models.BooleanField(default=False),
        ),
        migrations.AddConstraint(
            model_name="timerphase",
            constraint=models.UniqueConstraint(
                fields=("path", "timer"), name="unique-phase-path"
            ),
        ),
    ]
