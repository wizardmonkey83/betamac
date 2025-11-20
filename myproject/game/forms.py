from django import forms

class PassRangeParameters(forms.Form):
    # max value should be looked into
    addition_left_min = forms.IntegerField(initial=2, max_value=1000, required=False, widget=forms.TextInput(attrs={"class": "range-input"}))
    addition_left_max = forms.IntegerField(initial="100", max_value=1000, required=False, widget=forms.TextInput(attrs={"class": "range-input"}))
    addition_right_min = forms.IntegerField(initial="2", max_value=1000, required=False, widget=forms.TextInput(attrs={"class": "range-input"}))
    addition_right_max = forms.IntegerField(initial="100", max_value=1000, required=False, widget=forms.TextInput(attrs={"class": "range-input"}))

    multiplication_left_min = forms.IntegerField(initial="2", max_value=1000, required=False, widget=forms.TextInput(attrs={"class": "range-input"}))
    multiplication_left_max = forms.IntegerField(initial="12", max_value=1000, required=False, widget=forms.TextInput(attrs={"class": "range-input"}))
    multiplication_right_min = forms.IntegerField(initial="2", max_value=1000, required=False, widget=forms.TextInput(attrs={"class": "range-input"}))
    multiplication_right_max = forms.IntegerField(initial="100", max_value=1000, required=False, widget=forms.TextInput(attrs={"class": "range-input"}))

    addition_enabled = forms.BooleanField(initial=True, required=False)
    subtraction_enabled = forms.BooleanField(initial=True, required=False)
    multiplication_enabled = forms.BooleanField(initial=True, required=False)
    division_enabled = forms.BooleanField(initial=True, required=False)

    distractions_enabled = forms.BooleanField(initial=False, required=False)

class PassHostParameters(forms.Form):
    addition_left_min = forms.IntegerField(initial=2, max_value=1000, required=False, widget=forms.TextInput(attrs={"class": "range-input"}))
    addition_left_max = forms.IntegerField(initial="100", max_value=1000, required=False, widget=forms.TextInput(attrs={"class": "range-input"}))
    addition_right_min = forms.IntegerField(initial="2", max_value=1000, required=False, widget=forms.TextInput(attrs={"class": "range-input"}))
    addition_right_max = forms.IntegerField(initial="100", max_value=1000, required=False, widget=forms.TextInput(attrs={"class": "range-input"}))

    multiplication_left_min = forms.IntegerField(initial="2", max_value=1000, required=False, widget=forms.TextInput(attrs={"class": "range-input"}))
    multiplication_left_max = forms.IntegerField(initial="12", max_value=1000, required=False, widget=forms.TextInput(attrs={"class": "range-input"}))
    multiplication_right_min = forms.IntegerField(initial="2", max_value=1000, required=False, widget=forms.TextInput(attrs={"class": "range-input"}))
    multiplication_right_max = forms.IntegerField(initial="100", max_value=1000, required=False, widget=forms.TextInput(attrs={"class": "range-input"}))

    addition_enabled = forms.BooleanField(initial=True, required=False)
    subtraction_enabled = forms.BooleanField(initial=True, required=False)
    multiplication_enabled = forms.BooleanField(initial=True, required=False)
    division_enabled = forms.BooleanField(initial=True, required=False)

    distractions_enabled = forms.BooleanField(initial=False, required=False)

    lobby_code = forms.CharField(required=True)

class Joinlobby(forms.Form):
    lobby_code = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "lobby-input"}))

