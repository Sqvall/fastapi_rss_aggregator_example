from tortoise import models, fields

from core.fields import URLField


class Feed(models.Model):
    source_url = URLField(unique=True)
    name = fields.CharField(max_length=256, unique=True)
    title = fields.TextField(default='')
    description = fields.TextField(default='')
    can_updated = fields.BooleanField(default=True)
