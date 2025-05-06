from django import forms
from django.contrib.auth import get_user_model
from .models import CustomUser
from allauth.account.forms import SignupForm
from django.contrib.auth.forms import UserChangeForm

# Get the CustomUser model dynamically
CustomUser = get_user_model()

# Profile update form
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'phonenumber', 'address', 'gender', 'dateofbirth', 'bio', 'profilepicture']

    # Adding a custom validation (optional) for phone number format
    def clean_phonenumber(self):
        phonenumber = self.cleaned_data['phonenumber']
        # Add validation for phone number format if needed
        return phonenumber


class UserSignupForm(SignupForm):
    name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={
        'placeholder':'FullName',
    })
                           )
    phonenumber = forms.CharField(max_length=15, required=True)
    email = forms.EmailField(required=True)
    address = forms.CharField(required=False) 
    gender = forms.ChoiceField(required=True, choices=[('M', 'Male'), ('F', 'Female')])
    dateofbirth = forms.DateField(required=False, widget=forms.DateInput(attrs={
        'type': 'date'
    }))
    profilepicture = forms.ImageField(required=False)
    bio = forms.CharField(required=False, widget=forms.Textarea(attrs= {
        "placeholder": "Enter your Bio"
    }))
    class Meta(CustomUser):
        FIELDS = (
            'name',
            'phonenumber',
            'email',
            'address',
            "gender",
            'dateofbirth',
            'profilepicture',
            'bio'
        )

    def cleanPhonenumber(self):
        phonenumber = self.cleaned_data['phonenumber'] 
        if CustomUser.objects.filter(phonenumber = phonenumber).exists():
            raise ValidationError('This Phonenumber already exist')
        return phonenumber
    
    def save(self,request):
        user = super(UserSignupForm,self).save(request)
        user.name = self.cleaned_data['name']
        user.phonenumber = self.cleaned_data['phonenumber']
        user.dateofbirth = self.cleaned_data['dateofbirth']
        user.profilepicture = self.cleaned_data['profilepicture']
        user.bio = self.cleaned_data['bio']
        user.address = self.cleaned_data['address']
        user.gender = self.cleaned_data['gender']
        user.save()
        return user

