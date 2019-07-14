from __future__ import unicode_literals

from itertools import count

from django.db import migrations, models


temp_counter = count()
def temp_count():
    return next(temp_counter)


def renumber_slots(apps, schema_editor):
    Queue = apps.get_model('register', 'Queue')
    for queue in Queue.objects.all():
        counter = count()
        for slot in queue.slots.order_by('timestamp'):
            slot.monotonic_position = next(counter)
            slot.save()


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0003_remove_accomm_special_needs'),
    ]

    operations = [
        migrations.AddField(
            model_name='queueslot',
            name='monotonic_position',
            field=models.IntegerField(default=temp_count),
            preserve_default=False,
        ),
        migrations.RunPython(renumber_slots),
        migrations.AlterUniqueTogether(
            name='queueslot',
            unique_together=set([('queue', 'monotonic_position')]),
        ),
    ]
