from dataclasses import dataclass
from typing import Dict


@dataclass(unsafe_hash=True)
class Ingredient:
    i_id: int  # unique identifier of ingredient
    name: str
    unit: str

    def __eq__(self, other):
        return self.i_id == other.i_id


class IngredientStoreError(Exception):
    pass


class IngredientAlreadyExist(IngredientStoreError):
    pass


class IngredientNotExists(IngredientStoreError):
    pass


class InsufficientIngredient(IngredientStoreError):
    pass


class IngredientStore:

    def __init__(self, ingredients: Dict[Ingredient, float] = None, dynamic=False):
        """
        Store and manage ingredients.
        :param ingredients:
        :param dynamic: Is dynamic adding of slots enabled.
        """
        self._ingredients_slots = ingredients or {}
        self._dynamic = dynamic

    def add_slot(self, ingredient: Ingredient, quantity: float):
        if not self._dynamic:
            raise IngredientStoreError("Can not add slots after build.")

        if ingredient in self._ingredients_slots:
            raise IngredientAlreadyExist("Ingredient slot already exists in store."
                                         " You can only refill.")
        self._ingredients_slots[ingredient] = quantity

    def refill(self, ingredient: Ingredient, quantity: float):
        if ingredient not in self._ingredients_slots:
            raise IngredientNotExists("Can not refill because ingredient not present in store.")
        self._ingredients_slots[ingredient] += quantity

    def take(self, ingredient: Ingredient, quantity: float):
        if ingredient not in self._ingredients_slots:
            raise IngredientNotExists(f"Ingredient {ingredient} not available.")
        store_quantity = self._ingredients_slots[ingredient]
        if store_quantity < quantity:
            raise InsufficientIngredient(f"Not enough ingredients available of {ingredient}."
                                         f"Required is: {quantity}, Available is {store_quantity}")
        self._ingredients_slots[ingredient] -= quantity
        return ingredient
