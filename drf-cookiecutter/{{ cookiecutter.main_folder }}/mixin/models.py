from copy import deepcopy
from uuid import uuid4

from django.db import models
from django.forms.models import model_to_dict
from django.utils import timezone


class BaseMixin(models.Model):
    created = models.DateTimeField(auto_created=True, default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    uuid = models.UUIDField(unique=True, default=uuid4)

    class Meta:
        abstract = True


def normalize_diff_dict(d):
    for k, v in d.items():
        if v == "":
            d[k] = None
        elif type(v) is str:
            d[k] = v.lower()

    return d


class ModelDiffMixin:
    relation_fields = {}

    def __init__(self, *args, **kwargs):
        super(ModelDiffMixin, self).__init__(*args, **kwargs)
        self.__initial = deepcopy(self._dict)

    @property
    def diff(self):
        d1 = normalize_diff_dict(self.__initial)
        d2 = normalize_diff_dict(self._dict)
        diffs = [(k, (v, d2[k])) for k, v in d1.items() if v != d2[k]]

        return dict(diffs)

    @property
    def has_changed(self):
        return bool(self.diff)

    @property
    def changed_fields(self):
        return self.diff.keys()

    def get_field_diff(self, field_name):
        """
        Returns a diff for field if it's changed and None otherwise.
        """
        return self.diff.get(field_name, None)

    @property
    def _dict(self):
        return model_to_dict(self, fields=[field.name for field in self._meta.fields])

    @property
    def diff_without_id(self):
        diff = self.diff

        if "id" in diff:
            del diff["id"]

        return diff

    @property
    def initial_without_id(self):
        initial = self.__initial

        if "id" in initial:
            del initial["id"]

        return initial

    def reset_type(self):
        self.__initial["type"] = self._dict["type"]
