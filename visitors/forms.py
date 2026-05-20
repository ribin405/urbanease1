from django import forms
from .models import VisitorRequest


class VisitorRequestForm(forms.ModelForm):

    class Meta:
        model = VisitorRequest

        fields = [
            'visitor_name',
            'phone_number',
            'purpose',
            'visit_date',
        ]