from django.contrib import auth
from django.db import models


class Dish(models.Model):
    """A dish."""
    name = models.CharField(max_length=70,
                             help_text="The name of the dish.")
    description = models.TextField(help_text="The Description text.")
    receipe = models.TextField(help_text="The Receipe text.")
    publication_date = models.DateField(verbose_name="Date the dish was published.")
    photo = models.ImageField(null=True,
                              blank=True,
                              upload_to="dish_photos/")

    def __str__(self):
        return "{}".format(self.name)

class Review(models.Model):
    content = models.TextField(help_text="The Review text.")
    rating = models.IntegerField(help_text="The the reviewer has given.")
    date_created = models.DateTimeField(auto_now_add=True,
                                        help_text="The date and time the review was created.")
    date_edited = models.DateTimeField(null=True,
                                       help_text="The date and time the review was last edited.")
    creator = models.ForeignKey(auth.get_user_model(), on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, default=None,
                             help_text="The Dish that this review is for.")

    def __str__(self):
        return "{} - {}".format(self.creator.username, self.dish.name)
