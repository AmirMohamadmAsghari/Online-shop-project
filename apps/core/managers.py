from django.db import models


class LogicalQuerySet(models.QuerySet):
    def undelete(self):
        return self.update(is_deleted=False)

    def delete(self):
        return self.update(is_deleted=True)

    def activate(self):
        return self.update(is_active=True)

    def deactivate(self):
        return self.update(is_active=False)


class LogicalManager(models.Manager):
    def get_queryset(self):
        return LogicalQuerySet(self.model, using=self._db).filter(is_deleted=False)

    def all_with_deleted(self):
        return LogicalQuerySet(self.model, using=self._db)

    def deleted(self):
        return LogicalQuerySet(self.model, using=self._db).filter(is_deleted=True)

