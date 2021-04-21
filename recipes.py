import time
from typing import Tuple

from ingredients import IngredientStore, Ingredient


class Recipe:
    required_ingredients: Tuple[Tuple[Ingredient, float]] = ()

    def __init__(self, cook_time, r_id, ingredients = None):
        if ingredients:
            self.required_ingredients = ingredients
        self.cook_time = cook_time
        self.r_id = r_id

    def take_ingredients(self, ingredient_store: IngredientStore):
        for required_ing in self.required_ingredients:
            ingredient_store.take(required_ing[0], required_ing[1])

    def make(self):
        time.sleep(self.cook_time)
        print(f"Made {self.__class__.__name__}", flush=True)

    def __hash__(self) -> int:
        return hash(self.r_id)

    def __eq__(self, other):
        return self.r_id == other.r_id

    def __str__(self):
        return self.__class__.__name__
