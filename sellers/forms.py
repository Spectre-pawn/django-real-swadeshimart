
from django import forms

from sellers.models import Seller, Variation

class  variationform(forms.ModelForm):
    class Meta:
        model =Variation
        fields ='__all__'

class SalerAddressForm(forms.ModelForm):
	shop_Address = forms.CharField(widget=forms.TextInput(attrs={}))
	locality = forms.CharField(required =True)
	city = forms.CharField(required =True)
	alternate_mobile = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Alternate Mobile No(optional)'}), required = False)
	landmark = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Landmark(optional)'}), required = False)
	class Meta:
		model = Seller
		fields = [
			'mobile',
			'shop_Name',
			'alternate_mobile',
			'shop_Address',
			'pincode',
			'landmark',
			'locality',
			'city',
			'state',
		]
class UpdateSalerDetailForm(forms.ModelForm):
	class Meta:
		model = Seller
		fields = [
            'username',
            'first_name',
            'last_name',
            'password',
            'email',
			'photo',
			'mobile',
			'shop_Name',
			'gst_Number',
			'alternate_mobile',
			'shop_Address',
			'pincode',
			'landmark',
			'locality',
			'city',
			'state',
		]

class UpdateSalerAccountDetailForm(forms.ModelForm):
	class Meta:
		model = Seller
		fields = [
			'account_Holder_Name',
			'account_Number',
			'ifsc_Code',
			]