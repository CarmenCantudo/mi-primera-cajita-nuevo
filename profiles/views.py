from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import UserProfileForm

from checkout.models import Order
from products.models import Product


@login_required
def profile(request):
    """
    Display the user's profile
    from CI Boutique Ado
    """
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request,
                           'Update failed. Please ensure the form is valid.')
    else:
        form = UserProfileForm(instance=profile)
    orders = profile.orders.all()

    template = 'profiles/profile.html'
    context = {
        'form': form,
        'orders': orders,
        'on_profile_page': True
    }

    return render(request, template, context)


def order_history(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)


def favourites(request, product_id):
    """
    Add/Remove a product to favourites
    """
    product = get_object_or_404(Product, pk=product_id)

    if product.favourites.filter(id=request.user.id).exists():
        product.favourites.remove(request.user)
    else:
        product.favourites.add(request.user)

    return redirect(reverse('product_detail', args=[product.id]))


def favourite_list(request):
    """
    Favourite Products List Page
    """
    user = request.user
    favourite_products = user.favourites.all()

    context = {
        'add_favourite': favourite_products
    }

    return render(request, 'profiles/favourites.html', context)
