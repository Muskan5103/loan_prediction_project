from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class LoanForm(forms.Form):

    # ---- Personal Details ----
    gender = forms.ChoiceField(
        choices=[('Male', 'Male'), ('Female', 'Female')],
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    married = forms.ChoiceField(
        label="Marital Status",
        choices=[('Yes', 'Married'), ('No', 'Unmarried')],
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    dependents = forms.ChoiceField(
        choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3+', '3+')],
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    education = forms.ChoiceField(
        choices=[('Graduate', 'Graduate'), ('Not Graduate', 'Not Graduate')],
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    self_employed = forms.ChoiceField(
        choices=[('Yes', 'Yes'), ('No', 'No')],
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    applicant_income = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    coapplicant_income = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    loan_amount = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    loan_term = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    credit_history = forms.ChoiceField(
        choices=[(1, 'Yes'), (0, 'No')],
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    property_area = forms.ChoiceField(
        choices=[('Urban', 'Urban'), ('Semiurban', 'Semi-Urban'), ('Rural', 'Rural')],
        widget=forms.Select(attrs={'class': 'form-select'})
    )


# ✅ RESTORED REGISTER FORM
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
