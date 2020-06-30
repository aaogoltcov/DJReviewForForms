from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse

from .models import Product, Review
from .forms import ReviewForm


def product_list_view(request):
    template = 'app/product_list.html'
    products = Product.objects.all()
    context = {
        'product_list': products,
    }
    return render(request, template, context)


def is_review(reviews, pk, request):
    for review in reviews:
        try:
            if int(review['review_user_id']) == int(request.session['_auth_user_id']) and int(review['product_id']) == int(pk):
                return True
                break
        except KeyError:
            pass
    return None


def product_view(request, pk):
    template = 'app/product_detail.html'
    product = get_object_or_404(Product, id=pk)
    reviews = Review.objects.all().values().filter(product_id=pk)
    is_review_exist = is_review(reviews, pk, request)
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid() and is_review_exist is not True:
            post = form.save(commit=False)
            post.product_id = pk
            post.review_user_id = request.session['_auth_user_id']
            post.save()
            return redirect('product_detail', pk=post.product_id)
    else:
        form = form
    context = {
        'form': form,
        'product': product,
        'reviews': reviews,
        'is_review_exist': is_review_exist,
    }
    return render(request, template, context)
