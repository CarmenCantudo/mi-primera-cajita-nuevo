from django.shortcuts import (
    render, redirect, reverse, HttpResponse, get_object_or_404)
from django.contrib import messages

from products.models import Product


# From CI Boutique Ado
def view_bag(request):
    """ A view that renders the bag contents page """

    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    colour = None
    if 'product_colour' in request.POST:
        colour = request.POST['product_colour']
    bag = request.session.get('bag', {})

    if colour:
        if item_id in list(bag.keys()):
            if colour in bag[item_id]['items_by_colour'].keys():
                bag[item_id]['items_by_colour'][colour] += quantity
                messages.success(request,
                                 f'Updated colour {colour.upper()} '
                                 f'{product.name} quantity to '
                                 f'{bag[item_id]["items_by_colour"][colour]}')
            else:
                bag[item_id]['items_by_colour'][colour] = quantity
                messages.success(request,
                                 f'Added colour {colour.upper()} '
                                 f'{product.name} to your bag')
        else:
            bag[item_id] = {'items_by_colour': {colour: quantity}}
            messages.success(request,
                             f'Added colour {colour.upper()} {product.name} '
                             f'to your bag')
    else:
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
            messages.success(request,
                             f'Updated {product.name} quantity to '
                             f'{bag[item_id]}')
        else:
            bag[item_id] = quantity
            messages.success(request,
                             f'Added {product.name} to your bag')

    request.session['bag'] = bag
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """Adjust the quantity of the specified product to the specified amount"""

    product = Product.objects.get(pk=item_id)
    quantity = int(request.POST.get('quantity'))
    colour = None
    if 'product_colour' in request.POST:
        colour = request.POST['product_colour']
    bag = request.session.get('bag', {})

    if colour:
        if quantity > 0:
            bag[item_id]['items_by_colour'][colour] = quantity
            messages.success(request,
                             f'Updated colour {colour.upper()} {product.name} '
                             f'quantity to '
                             f'{bag[item_id]["items_by_colour"][colour]}')
        else:
            del bag[item_id]['items_by_colour'][colour]
            if not bag[item_id]['items_by_colour']:
                bag.pop(item_id)
            messages.success(request,
                             f'Removed colour {colour.upper()} {product.name} '
                             f'from your bag')
    else:
        if quantity > 0:
            bag[item_id] = quantity
            messages.success(request,
                             f'Updated {product.name} quantity to '
                             f'{bag[item_id]}')
        else:
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag')

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """ Remove the item from the shopping bag """

    try:
        product = Product.objects.get(pk=item_id)
        colour = None
        if 'product_colour' in request.POST:
            colour = request.POST['product_colour']
        bag = request.session.get('bag', {})

        if colour:
            del bag[item_id]['items_by_colour'][colour]
            if not bag[item_id]['items_by_colour']:
                bag.pop(item_id)
            messages.success(request,
                             f'Removed colour {colour.upper()} {product.name} '
                             f'from your bag')
        else:
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag')

        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)
