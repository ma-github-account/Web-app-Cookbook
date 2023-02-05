from django import forms

from .models import Dish, Review


class SearchForm(forms.Form):
    search = forms.CharField(required=False, min_length=3)
    search_in = forms.ChoiceField(required=False,
                                  choices=(
                                      ("name", "Name"),
                                      ("description", "Description")
                                  ))

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ["date_edited", "dish"]

    rating = forms.IntegerField(min_value=0, max_value=5)


class DishMediaForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ["photo"]
