from django import forms

class PassRangeParameters(forms.Form):
    # max value should be looked into
    addition_left_min = forms.IntegerField(initial=2, max_value=1000, required=True, widget=forms.TextInput(attrs={"class": "range-input"}))
    addition_left_max = forms.IntegerField(initial="100", max_value=1000, required=True, widget=forms.TextInput(attrs={"class": "range-input"}))
    addition_right_min = forms.IntegerField(initial="2", max_value=1000, required=True, widget=forms.TextInput(attrs={"class": "range-input"}))
    addition_right_max = forms.IntegerField(initial="100", max_value=1000, required=True, widget=forms.TextInput(attrs={"class": "range-input"}))

    multiplication_left_min = forms.IntegerField(initial="2", max_value=1000, required=True, widget=forms.TextInput(attrs={"class": "range-input"}))
    multiplication_left_max = forms.IntegerField(initial="12", max_value=1000, required=True, widget=forms.TextInput(attrs={"class": "range-input"}))
    multiplication_right_min = forms.IntegerField(initial="2", max_value=1000, required=True, widget=forms.TextInput(attrs={"class": "range-input"}))
    multiplication_right_max = forms.IntegerField(initial="2", max_value=1000, required=True, widget=forms.TextInput(attrs={"class": "range-input"}))

    duration = forms.IntegerField(required=False)