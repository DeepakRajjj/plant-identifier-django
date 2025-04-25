from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import PlantSale, Purchase
from .forms import PlantForm, PurchaseForm

def market_home(request):
    query = request.GET.get('query', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')

    plants = PlantSale.objects.filter(is_sold=False)

    # Apply search filters if provided
    if query:
        plants = plants.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    if min_price:
        plants = plants.filter(price__gte=float(min_price))

    if max_price:
        plants = plants.filter(price__lte=float(max_price))

    return render(request, 'marketplace/market_home.html', {
        'plants': plants,
        'query': query,
        'min_price': min_price,
        'max_price': max_price
    })

@login_required
def add_plant(request):
    if request.method == 'POST':
        form = PlantForm(request.POST, request.FILES)
        if form.is_valid():
            plant = form.save(commit=False)
            plant.seller = request.user
            plant.save()
            messages.success(request, 'Your plant has been listed for sale!')
            return redirect('market_home')
    else:
        form = PlantForm()
    return render(request, 'marketplace/add_plant.html', {'form': form})

@login_required
def buy_plant(request, plant_id):
    plant = get_object_or_404(PlantSale, id=plant_id)

    # Check if the plant is out of stock
    if plant.quantity_available <= 0:
        messages.error(request, 'Sorry, this plant is out of stock.')
        return redirect('market_home')

    # Prevent users from buying their own plants
    if plant.seller == request.user:
        messages.error(request, 'You cannot buy your own plant.')
        return redirect('market_home')

    if request.method == 'POST':
        # Print the POST data for debugging
        print(f"POST data: {request.POST}")

        # Get quantity directly from POST data
        try:
            quantity = int(request.POST.get('quantity', 1))
            if quantity < 1:
                quantity = 1
            if quantity > plant.quantity_available:
                quantity = plant.quantity_available
        except (ValueError, TypeError):
            quantity = 1

        print(f"Parsed quantity: {quantity}")

        # Create the form with the POST data
        form = PurchaseForm(request.POST)

        # If the form is valid, process the purchase
        if form.is_valid():
            # Create a purchase record
            purchase = form.save(commit=False)
            purchase.plant = plant
            purchase.buyer = request.user
            purchase.quantity = quantity  # Use our parsed quantity
            purchase.save()

            # Update plant quantity
            plant.quantity_available -= quantity

            # If no more plants are available, mark as sold
            if plant.quantity_available <= 0:
                plant.is_sold = True

            plant.save()

            messages.success(request, f'You have successfully purchased {quantity} {plant.name}!')
            return redirect('purchase_confirmation', purchase_id=purchase.id)
        else:
            # Print form errors for debugging
            print(f"Form errors: {form.errors}")

            # Try to fix the form by setting the quantity field
            if 'quantity' in form.errors:
                # Create a new form with the correct quantity
                initial_data = request.POST.copy()
                initial_data['quantity'] = quantity
                form = PurchaseForm(initial_data)

                # Add a message about the quantity issue
                messages.warning(request, f'We\'ve adjusted the quantity to {quantity}.')
    else:
        form = PurchaseForm()

    return render(request, 'marketplace/buy_plant.html', {
        'plant': plant,
        'form': form
    })

@login_required
def purchase_confirmation(request, purchase_id):
    purchase = get_object_or_404(Purchase, id=purchase_id, buyer=request.user)
    return render(request, 'marketplace/purchase_confirmation.html', {'purchase': purchase})

@login_required
def my_purchases(request):
    purchases = Purchase.objects.filter(buyer=request.user).order_by('-purchase_date')
    return render(request, 'marketplace/my_purchases.html', {'purchases': purchases})

@login_required
def my_listings(request):
    active_listings = PlantSale.objects.filter(seller=request.user, is_sold=False).order_by('-date_listed')
    sold_listings = PlantSale.objects.filter(seller=request.user, is_sold=True).order_by('-date_listed')

    return render(request, 'marketplace/my_listings.html', {
        'active_listings': active_listings,
        'sold_listings': sold_listings
    })
