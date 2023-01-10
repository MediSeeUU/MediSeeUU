# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django import forms


class LockModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        with_lock_fields = {}
        for field in self.fields:
            with_lock_fields[field] = self.fields[field]
            with_lock_fields[f"{field}_locked"] = forms.BooleanField(required=False)
        self.fields = with_lock_fields

    def save(self, commit=True):
        return super().save(commit=commit)
