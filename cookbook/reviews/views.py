from io import BytesIO

from PIL import Image
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.files.images import ImageFile
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .forms import SearchForm, ReviewForm, DishMediaForm
from .models import Dish, Review
from .utils import average_rating


def index(request):
    return render(request, "base.html")


#def dish_search(request):
#    search_text = request.GET.get("search", "")
#    search_history = request.session.get('search_history', [])
#    form = SearchForm(request.GET)
#    dishes = set()
#    if form.is_valid() and form.cleaned_data["search"]:
#        search = form.cleaned_data["search"]
#        search_in = form.cleaned_data.get("search_in") or "name"
#        if search_in == "name":
#            dishes = Dish.objects.filter(name__icontains=search)
#
#        if request.user.is_authenticated:
#            search_history.append([search_in, search])
#            request.session['search_history'] = search_history
#    elif search_history:
#        initial = dict(search=search_text,
#                       search_in=search_history[-1][0])
#        form = SearchForm(initial=initial)
#
#    return render(request, "reviews/search-results.html", {"form": form, "search_text": search_text, "dishes": dishes})


def dish_search(request):
    search_text = request.GET.get("search", "")
    search_history = request.session.get('search_history', [])
    form = SearchForm(request.GET)
    dishes = set()
    if form.is_valid() and form.cleaned_data["search"]:
        search = form.cleaned_data["search"]
        search_in = form.cleaned_data.get("search_in") or "name"
        if search_in == "name":
            dishes = Dish.objects.filter(name__icontains=search)
#        else:
#            fname_contributors = \
#                Dish.objects.filter(description__icontains=search)
#
#            for contributor in fname_contributors:
#                for book in contributor.book_set.all():
#                    books.add(book)

        if request.user.is_authenticated:
            search_history.append([search_in, search])
            request.session['search_history'] = search_history
    elif search_history:
        initial = dict(search=search_text,
                       search_in=search_history[-1][0])
        form = SearchForm(initial=initial)

    return render(request, "reviews/search-results.html", {"form": form, "search_text": search_text, "dishes": dishes})




































def dish_list(request):
    dishes = Dish.objects.all()
    dishes_with_reviews = []
    for dish in dishes:
        reviews = dish.review_set.all()
        if reviews:
            dish_rating = average_rating([review.rating for review in reviews])
            number_of_reviews = len(reviews)
        else:
            dish_rating = None
            number_of_reviews = 0
        dishes_with_reviews.append({"dish": dish, "dish_rating": dish_rating, "number_of_reviews": number_of_reviews})

    context = {
        "dish_list": dishes_with_reviews
    }
    return render(request, "reviews/dish_list.html", context)


def dish_detail(request, pk):
    dish = get_object_or_404(Dish, pk=pk)
    reviews = dish.review_set.all()
    if reviews:
        dish_rating = average_rating([review.rating for review in reviews])
        context = {
            "dish": dish,
            "dish_rating": dish_rating,
            "reviews": reviews
        }
    else:
        context = {
            "dish": dish,
            "dish_rating": None,
            "reviews": None
        }
    if request.user.is_authenticated:
        max_viewed_dishes_length = 10
        viewed_dishes = request.session.get('viewed_dishes', [])
        viewed_dish = [dish.id, dish.name]
        if viewed_dish in viewed_dishes:
            viewed_dishes.pop(viewed_dishes.index(viewed_dish))
        viewed_dishes.insert(0, viewed_dish)
        viewed_dishes = viewed_dishes[:max_viewed_dishes_length]
        request.session['viewed_dishes'] = viewed_dishes
    return render(request, "reviews/dish_detail.html", context)


def is_staff_user(user):
    return user.is_staff

@login_required
def review_edit(request, dish_pk, review_pk=None):
    dish = get_object_or_404(Dish, pk=dish_pk)

    if review_pk is not None:
        review = get_object_or_404(Review, dish_id=dish_pk, pk=review_pk)
        user = request.user
        if not user.is_staff and review.creator.id != user.id:
            raise PermissionDenied
    else:
        review = None

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)

        if form.is_valid():
            updated_review = form.save(False)
            updated_review.dish = dish

            if review is None:
                messages.success(request, "Review for \"{}\" created.".format(dish))
            else:
                updated_review.date_edited = timezone.now()
                messages.success(request, "Review for \"{}\" updated.".format(dish))

            updated_review.save()
            return redirect("dish_detail", dish.pk)
    else:
        form = ReviewForm(instance=review)

    return render(request, "reviews/instance-form.html",
                  {"form": form,
                   "instance": review,
                   "model_type": "Review",
                   "related_instance": dish,
                   "related_model_type": "Dish"
                   })

@login_required
def dish_media(request, pk):
    dish = get_object_or_404(Dish, pk=pk)

    if request.method == "POST":
        form = DishMediaForm(request.POST, request.FILES, instance=dish)

        if form.is_valid():
            dish = form.save(False)

            photo = form.cleaned_data.get("photo")

            if photo:
                image = Image.open(photo)
                image.thumbnail((300, 300))
                image_data = BytesIO()
                image.save(fp=image_data, format=photo.image.format)
                image_file = ImageFile(image_data)
                dish.photo.save(photo.name, image_file)
            dish.save()
            messages.success(request, "Dish \"{}\" was successfully updated.".format(dish))
            return redirect("dish_detail", dish.pk)
    else:
        form = DishMediaForm(instance=dish)

    return render(request, "reviews/instance-form.html",
                  {"instance": dish, "form": form, "model_type": "Dish", "is_file_upload": True})
