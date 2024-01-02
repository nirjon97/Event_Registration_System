from django import forms
from .models import UserProfile,Category

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = []



class CategorySelectionForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Select a category")