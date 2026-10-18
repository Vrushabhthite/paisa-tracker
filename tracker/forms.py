from django import forms
from .models import Transaction
class TxnForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["type", "amount", "category", "person", "date", "note"]
        widgets = {"date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d")}
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        for f in self.fields.values():
            f.widget.attrs["class"] = "form-select" if f.widget.__class__.__name__ == "Select" else "form-control"
