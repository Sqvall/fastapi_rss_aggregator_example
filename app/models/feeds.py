from tortoise import models, fields

from core.fields import URLField


class Feed(models.Model):
    guid = fields.UUIDField(pk=True)
    source_url = URLField()
    name = fields.CharField(max_length=256)
    title = fields.TextField(default='')
    description = fields.TextField(default='')
    can_updated = fields.BooleanField(default=True)

    def __str__(self):
        return self.name
