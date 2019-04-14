import os
import time

from django.core.exceptions import ValidationError
from django.db import models

from app.elections.models import Pool, Vote
from app.school.services import get_student_info


def candidate_image_path(instance, filename):
    ext = os.path.splitext(filename)[-1]
    now = str(time.time()).replace('.', '')
    full_name = str(instance)
    return os.path.join('candidate', '{}-{}{}'.format(now, full_name, ext))


class Candidate(models.Model):
    image = models.ImageField('照片', upload_to=candidate_image_path)
    std_no = models.CharField('學號', max_length=15)
    name = models.CharField('姓名', max_length=30)
    klass = models.CharField('課程', max_length=30)
    politics = models.TextField('政見', max_length=1000, blank=True)
    pool = models.ForeignKey(
        Pool,
        models.PROTECT,
        'candidates',
        verbose_name='選舉類型'
    )

    class Meta:
        unique_together = (
            ('std_no', 'pool'),
        )

    def __str__(self):
        return f'{self.pool}-{self.std_no}-{self.name}'

    def clean(self):
        if self.pk is not None and Vote.objects.count() > 0:
            raise ValidationError('Vote started so can\'t edit candidate.')

        try:
            info = get_student_info(self.std_no, ['std_name', 'class_name'])
        except Exception:
            raise ValidationError({'std_no': 'Student number not valid.'})

        self.name = info['std_name']
        self.klass = info['class_name']
