from django import forms
from ecommerce.models import CustomerDetails
from django.contrib.auth.models import User
from sellers.models import ReviewRating
from django.contrib.auth.forms import UserCreationForm

class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['subject', 'review', 'rating']


class UserUpdateForm(forms.ModelForm):
	class Meta:
		model = User
		fields = [
			'first_name',
			 'last_name',
			 'email',
		]

class UpdateUserDetailForm(forms.ModelForm):
	class Meta:
		model = CustomerDetails
		fields = [
			'dob',
			'photo',
			'mobile',
			'alternate_mobile',
			'address',
			'pincode',
			'landmark',
			'locality',
			'city',
			'state',
			'gender',
		]

class UserAddressForm1(forms.ModelForm):
	class Meta:
		model = User
		fields = [
			'first_name',
			 'last_name',
		]
class UserAddressForm(forms.ModelForm):
	address = forms.CharField(widget=forms.TextInput(attrs={}))
	locality = forms.CharField(required =True)
	city = forms.CharField(required =True)
	alternate_mobile = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Alternate Mobile No(optional)'}), required = False)
	landmark = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Landmark(optional)'}), required = False)
	class Meta:
		model = CustomerDetails
		fields = [
			'mobile',
			'alternate_mobile',
			'address',
			'pincode',
			'landmark',
			'locality',
			'city',
			'state',
		]

