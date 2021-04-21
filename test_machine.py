import pytest

from ingredients import Ingredient, IngredientStore, InsufficientIngredient
from machine import CoffeeMachine, MachineError, OutletNotFoundError, RecipeNotFoundError
from recipes import Recipe


@pytest.fixture
def water():
    return Ingredient(1, "Hot Water", "ml")


@pytest.fixture
def milk():
    return Ingredient(2, "Hot Milk", "ml")


@pytest.fixture
def tea_leaves_syrup():
    return Ingredient(3, "Tea leaves syrup", "ml")


@pytest.fixture
def ginger_syrup():
    return Ingredient(4, "Ginger Syrup", "ml")


@pytest.fixture
def sugar_syrup():
    return Ingredient(5, "Sugar syrup", "ml")


@pytest.fixture
def elaichi_syrup():
    return Ingredient(6, "Elaichi syrup", "ml")


@pytest.fixture
def ginger_tea(water, milk, tea_leaves_syrup, ginger_syrup, sugar_syrup):
    return Recipe(
        cook_time=1, r_id=1,
        ingredients=(
            (water, 50),
            (milk, 10),
            (tea_leaves_syrup, 10),
            (ginger_syrup, 5),
            (sugar_syrup, 10)
        ))


@pytest.fixture
def hot_milk(milk):
    return Recipe(
        cook_time=1, r_id=2,
        ingredients=(
            (milk, 50),
        ))


@pytest.fixture
def hot_water(water):
    return Recipe(
        cook_time=1, r_id=3,
        ingredients=(
            (water, 50),
        ))


@pytest.fixture
def coffee_machine(milk, water, hot_water, hot_milk):
    ist = IngredientStore({
        water: 100,
        milk: 100,
    })
    recps = [hot_milk, hot_water]
    return CoffeeMachine(3, ist, recps)


def test_coffee_machine(coffee_machine, hot_milk, hot_water):
    cm = coffee_machine
    cm.serve(hot_milk)

    cm.serve(hot_milk)

    with pytest.raises(InsufficientIngredient):
        cm.serve(hot_milk)

    cm.serve(hot_water)

    with pytest.raises(OutletNotFoundError):
        cm.serve(hot_water)


def test_non_existing_recipe(coffee_machine, hot_milk, ginger_tea):
    cm = coffee_machine
    cm.serve(hot_milk)

    with pytest.raises(RecipeNotFoundError):
        cm.serve(ginger_tea)


def test_more_outlet_demand(coffee_machine, hot_milk, hot_water):
    cm = coffee_machine
    cm.serve(hot_milk)
    cm.serve(hot_milk)
    cm.serve(hot_water)

    with pytest.raises(OutletNotFoundError):
        cm.serve(hot_water)
