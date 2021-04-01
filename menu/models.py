from django.db import models


# Create your models here.
class Meal(models.Model):
    name = models.TextField()
    description = models.TextField()


class Ingredient(models.Model):
    name = models.textField()


class FoodPreferences(models.Model):
    food_preference = models.TextField()


class FoodPreferenceRelationship(model.Models):
    meal_name = models.ForeignKey(Meal, on_delete=models.CASCADE)
    food_preference_name = models.ForeignKey(FoodPreferences, on_delete=models.CASCADE)


class IngredientRelationship(model.Models):
    meal_name = models.ForeignKey(Meal, on_delete=models.CASCADE)
    ingredient_name = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
