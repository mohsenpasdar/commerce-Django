from django import forms
from .models import AuctionListing

class AuctionListingForm(forms.ModelForm):
    class Meta:
        model = AuctionListing
        fields = ['title', 'description', 'starting_bid', 'image_url', 'category']
        widgets = {'category': forms.Select(choices=AuctionListing.CATEGORY_CHOICES)}

    def __init__(self, *args, **kwargs):
        super(AuctionListingForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['starting_bid'].widget.attrs.update({'class': 'form-control'})
        self.fields['image_url'].widget.attrs.update({'class': 'form-control'})
        self.fields['category'].widget.attrs.update({'class': 'form-control'})


class BidForm(forms.Form):
    bid_amount = forms.DecimalField(
        max_digits=10, decimal_places=2, min_value=0.01, label="Bid Amount"
    )