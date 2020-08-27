from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import *

class RegisterForm(forms.ModelForm):
    username = forms.CharField(label=False, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    first_name = forms.CharField(label=False, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(label=False, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    email = forms.EmailField(label=False, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class ListingForm(forms.ModelForm):
    options=[
        'fashion',
        'beauty',
        'appliances',
        'automotive',
        'collectibles',
        'music',
        'electronics',
        'furniture',
        'kitchen',
        'jewelry',
        'software',
        'toys'
    ]
    title = forms.CharField(label=False, widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    description = forms.CharField(label=False, required=False, widget=forms.Textarea(attrs={'placeholder': 'Description'}))
    basePrice = forms.DecimalField(max_digits=7, decimal_places=0, label=False, widget=forms.NumberInput(attrs={'placeholder': 'BasePrice (in rupees)'}))
    photo = forms.URLField(label=False, required=False, widget=forms.URLInput(attrs={'placeholder': 'URL For Photo'}))
    category = forms.ChoiceField(label=False, choices=[(option, option.capitalize()) for option in options])
    class Meta:
        model = Listing
        fields = ['title', 'description', 'basePrice', 'photo', 'category']

class BidForm(forms.ModelForm):
    amount = forms.DecimalField(max_digits=7, decimal_places=0, label=False, widget=forms.NumberInput(attrs={'placeholder': 'Amount (in rupees)'}), error_messages={"max_digits": "WARNING!"})
    class Meta:
        model = Bid
        fields = ['amount']

class CommentForm(forms.ModelForm):
    content = forms.CharField(label=False, widget=forms.Textarea(attrs={'placeholder': 'Comment'}))
    class Meta:
        model = Comment
        fields = ['content']


def hotprice(listing):
    if listing.bids.count() == 0:
        return listing.basePrice
    else:
        maxBid = listing.bids.first()
        for bid in listing.bids.all():
            if bid.amount > maxBid.amount:
                maxBid = bid
        return maxBid.amount

def maxbid(listing):
    if listing.bids.count() == 0:
        return None
    else:
        maxBid = listing.bids.first()
        for bid in listing.bids.all():
            if bid.amount > maxBid.amount:
                maxBid = bid
        return maxBid

def index(request):
    listings = Listing.objects.all()
    activeListings = [listing for listing in listings if listing.active is True]
    hotPrices = []
    for listing in activeListings:
        listing.hotPrice = hotprice(listing)
        
    return render(request, "auctions/index.html", {
        "listings": activeListings
    })


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        if username == "" or password == "":
            return render(request, "auctions/login.html", {
                "message": "Username or Password cannot be empty."
            })
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


def register(request):
    if request.method == "POST":
        registerData = RegisterForm(request.POST)
        if registerData.is_valid():
            username = registerData.cleaned_data["username"]
            first_name = registerData.cleaned_data["first_name"]
            last_name = registerData.cleaned_data["last_name"]
            email = registerData.cleaned_data["email"]
        else:
            return render(request, "auctions/register.html", {
                "message": "All fields are required.",
                "registerForm": registerData
            })
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password == "" or confirmation == "":
            return render(request, "auctions/register.html", {
                "message": "All fields are required.",
                "registerForm": registerData
            })
        if not (first_name.isalpha() and last_name.isalpha()):
            return render(request, "auctions/register.html", {
                "message": "Invalid Name.",
                "registerForm": registerData
            })
        # Ensure password matches confirmation
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match.",
                "registerForm": registerData
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name.capitalize()
            user.last_name = last_name.capitalize()
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken.",
                "registerForm": registerData
            })
        login(request, user)
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html", {
            "registerForm": RegisterForm()
        })

def create(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            listingData = ListingForm(request.POST)
            if listingData.is_valid():
                if listingData.cleaned_data["photo"] == "":
                    listingData.cleaned_data["photo"] = "https://us.123rf.com/450wm/pavelstasevich/pavelstasevich1811/pavelstasevich181101032/112815935-stock-vector-no-image-available-icon-flat-vector-illustration.jpg?ver=6"
                if listingData.cleaned_data["description"] == "":
                    listingData.cleaned_data["description"] = "Got nothing to say!"
            else:
                # either the amount is overlimit or a required field is empty
                return render(request, "auctions/create.html", {
                    "message": "Listing not valid.",
                    "listingForm": listingData
                })
                listing = Listing(
                    title=listingData.cleaned_data["title"],
                    description=listingData.cleaned_data["description"],
                    basePrice=listingData.cleaned_data["basePrice"],
                    photo=listingData.cleaned_data["photo"],
                    category=listingData.cleaned_data["category"],
                    seller=request.user
                    )
                listing.save()
                return HttpResponseRedirect(reverse('auctions:index'))
        else:
            return render(request, "auctions/create.html", {
                "listingForm": ListingForm()
            })
    else:
        return HttpResponseRedirect(reverse('auctions:login'))

def listing(request, listing_id):
    if Listing.objects.filter(id=listing_id).count() == 0:
        return render(request, "auctions/error.html", {
            "message": "INVALID LISTING ID!"
        })
    listing = Listing.objects.get(id=listing_id)
    maxBid = maxbid(listing)

    message = None
    bidData = BidForm()

    if request.user.is_authenticated:
        if request.method == "POST":
            bidData = BidForm(request.POST)
            if bidData.is_valid():
                amount = bidData.cleaned_data['amount']
                if amount > maxBid.amount:  
                    bid = Bid(
                        amount=amount,
                        user=request.user,
                        listing=listing
                        )
                    bid.save()
                    return HttpResponseRedirect(reverse('auctions:listing', kwargs={"listing_id": listing_id}))
                else:
                    message = "Bid must be greater than the Hot Price."
            else:
                message = "Amount must be less than \u20B910000000."          
    else:
        message = "You must be logged in."
    
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "maxBid": maxBid,
        "bidForm": bidData,
        "commentForm": CommentForm(),
        "message": message
    })

def closebid(request, listing_id):
    if Listing.objects.filter(id=listing_id).count() == 0:
        return render(request, "auctions/error.html", {
            "message": "INVALID LISTING ID!"
        })
    listing = Listing.objects.get(id=listing_id)
    if request.user.username != listing.seller.username:
        return render(request, "auctions/error.html", {
            "message": "ONLY THE SELLER CAN CLOSE THE BID!!"
        })
    if not listing.active:
        return render(request, "auctions/error.html", {
            "message": "THE BID IS ALREADY INACTIVE!"
        })
    if maxbid(listing) is None:
        winner = None
    else:
        winner = maxbid(listing).user

    listing.winner = winner
    listing.active = False
    listing.save()
    return HttpResponseRedirect(reverse('auctions:listing', kwargs={"listing_id": listing_id}))


def addcomment(request, listing_id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            commentData = CommentForm(request.POST)
            if commentData.is_valid():
                content = commentData.cleaned_data["content"]
            else:
                return HttpResponseRedirect(reverse('listing', kwargs={"listing_id": listing_id}))

            comment = Comment(
                content=content,
                user=request.user,
                listing=Listing.objects.get(id=listing_id)
            )
            comment.save()
            return HttpResponseRedirect(reverse('auctions:listing', kwargs={"listing_id": listing_id}))
        else:
            return render(request, "auctions/error.html", {
                "message": "LOGIN FIRST!"
            })
    else:
        return render(request, "auctions/error.html", {
            "message": "INVALID REQUEST!"
        })

def watchlist(request):
    if request.user.is_authenticated:
        watchlist = request.user.watchlist.all()
        for listing in watchlist:
            listing.hotPrice = hotprice(listing)
        return render(request, "auctions/watchlist.html", {
            "watchlist": watchlist
        })
    else:
        return render(request, "auctions/error.html", {
            "message": "LOGIN FIRST!"
        })

def addtowatchlist(request, listing_id):
    if not request.user.is_authenticated:
        return render(request, "auctions/error.html", {
            "message": "LOGIN FIRST!"
        })
    request.user.watchlist.add(Listing.objects.get(id=listing_id))
    return HttpResponseRedirect(reverse('auctions:listing', kwargs={"listing_id": listing_id}))

def removefromwatchlist(request, listing_id):
    if not request.user.is_authenticated:
        return render(request, "auctions/error.html", {
            "message": "LOGIN FIRST!"
        })
    request.user.watchlist.remove(Listing.objects.get(id=listing_id))
    return HttpResponseRedirect(reverse('auctions:listing', kwargs={"listing_id": listing_id}))

def categories(request):
    categories = [category.capitalize() for category in Listing.options]
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def category(request, category):
    category_listings = Listing.objects.filter(active=True, category=category)
    for listing in category_listings:
        listing.hotPrice = hotprice(listing)
    return render(request, "auctions/category.html", {
        "category_listings": category_listings,
        "category": category.capitalize()
    })