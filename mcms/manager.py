from django.db import models
from django.db.models.query import QuerySet

class BaseQuerySet(QuerySet):

    def active_items(self):
        return self.filter(active=2)

    def get_or_none(self, *args, **kwargs):
        try:
            return self.get(*args, **kwargs)
        except self.model.DoesNotExist:
            return None

    def one(self, *args, **kwargs):
        return self.filter(*args, **kwargs).order_by('pk')[0]

