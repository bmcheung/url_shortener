from django import forms
# from .models import Urls

class UrlForm(forms.Form):
    original = forms.URLField(required=False)
    shortened = forms.URLField(required=False)

    def clean(self):
        cleaned_data = super(UrlForm, self).clean()
        original = cleaned_data.get("original")
        shortened = cleaned_data.get("shortened")

        # if original and shortened:
        #     raise forms.ValidationError(
        #         "Enter either the original or shortened url."
        #     )
        # elif not original and not shortened:
        #     raise forms.ValidationError(
        #         "Enter either the original or shortened url."
        #     )
        # else:
        #
