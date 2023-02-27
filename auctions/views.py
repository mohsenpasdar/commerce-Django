from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import AuctionListing, User, Bid
from django.urls import reverse
from .forms import AuctionListingForm, BidForm
from datetime import datetime
from django.contrib import messages
from django.utils import timezone


def index(request):
    active_listings = AuctionListing.objects.filter(status='active')
    listings_with_bids = []
    
    for listing in active_listings:
        highest_bid = Bid.objects.filter(listing=listing).order_by('-amount').first()
        if highest_bid:
            current_bid = highest_bid.amount
        else:
            current_bid = listing.starting_bid
        
        listings_with_bids.append({
            'listing': listing,
            'current_bid': current_bid
        })
    
    context = {'listings_with_bids': listings_with_bids}
    return render(request, 'auctions/index.html', context)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def create_listing(request):
    if request.method == 'POST':
        # Create a new form instance and populate it with data from the request
        form = AuctionListingForm(request.POST)

        # Check whether the form is valid
        if form.is_valid():
            # Create a new AuctionListing object and save it to the database
            listing = form.save(commit=False)
            listing.seller = request.user
            listing.save()

            # Redirect the user to the newly created listing
            return redirect('index')
            # return redirect('index', pk=listing.pk)
    else:
        # Display a new, empty form for creating a listing
        form = AuctionListingForm()

    return render(request, 'auctions/create_listing.html', {'form': form})


def listing(request, listing_id):
    # Retrieve the listing from the database
    listing = get_object_or_404(AuctionListing, pk=listing_id)

    # Retrieve the highest bid for the listing
    highest_bid = Bid.objects.filter(listing=listing).order_by('-amount').first()

    # Check if there are any bids for the listing yet
    if highest_bid:
        current_bid = highest_bid.amount
    else:
        current_bid = listing.starting_bid

    # Check if the listing is closed:
    if listing.status == 'closed':
        if listing.winner == request.user:
            winner_message = 'Congratulations! You won this auction!'
        elif listing.winner and request.user == listing.seller:
            winner_message = f"Congratulations! Your listing has been sold to {listing.winner.username} for {current_bid}!"
        elif listing.winner:
            winner_message = f"{listing.winner.username} won this auction."
        else:
            winner_message = 'No one won this auction.'
        return render(request, 'auctions/listing.html', {'listing': listing, 'current_bid': current_bid, 'winner_message': winner_message})
    # Handle form submission
    if request.method == 'POST':
        # Check that the user is not the creator of the listing
        if request.user == listing.seller:
            messages.error(request, 'You cannot bid on your own listing.')
            return redirect('listing', listing_id=listing_id)
        # Retrieve the bid amount from the form
        bid_amount = request.POST['bid_amount']

        # Check that the bid amount is valid
        try:
            bid_amount = float(bid_amount)
        except ValueError:
            messages.error(request, 'Please enter a valid bid amount.')
            return redirect('listing', listing_id=listing_id)

        if bid_amount <= current_bid:
            messages.error(request, 'Your bid must be higher than the current bid.')
            return redirect('listing', listing_id=listing_id)

        # Create the bid object and save it to the database
        bid = Bid(listing=listing, bidder=request.user, amount=bid_amount)
        bid.save()

        # Update the current bid
        current_bid = bid_amount

        # Redirect to the listing page with a success message
        messages.success(request, 'Your bid was successful!')
        return redirect('listing', listing_id=listing_id)

    # Check if user is authenticated to show the bid form
    if request.user.is_authenticated:
        if request.user == listing.seller:
            bid_form = None
        else:
            bid_form = BidForm()
    else:
        bid_form = None

    # Render the template with the listing information and bid form
    return render(request, 'auctions/listing.html', {'listing': listing, 'current_bid': current_bid, 'bid_form': bid_form})

@login_required
def close_bid(request, listing_id):
    # Retrieve the listing from the database
    listing = get_object_or_404(AuctionListing, pk=listing_id)

    # Check that the user is the creator of the listing
    if request.user != listing.seller:
        messages.error(request, 'You are not authorized to perform this action.')
        return redirect('listing', listing_id=listing_id)

    # Set the listing status to closed
    listing.close_listing()

    # Retrieve the highest bid for the listing
    highest_bid = Bid.objects.filter(listing=listing).order_by('-amount').first()

    # Check if there are any bids for the listing
    if highest_bid:
        winning_bid = highest_bid.amount
        winning_bidder = highest_bid.bidder
    else:
        winning_bid = listing.starting_bid
        winning_bidder = None

    # Render the template with the listing information and the winning bid information
    return render(request, 'auctions/close_bid.html', {'listing': listing, 'winning_bid': winning_bid, 'winning_bidder': winning_bidder})
