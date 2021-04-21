import threading

from ingredients import Ingredient


class MachineError(Exception):
    pass


class OutletNotFoundError(MachineError):
    pass


class RecipeNotFoundError(MachineError):
    pass


class MachineThread(threading.Thread):

    def __init__(self, machine=None, group=None, target=None, name=None,
                 args=(), kwargs=None, *, daemon=None) -> None:
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self.machine = machine

    def run(self) -> None:
        super().run()
        if self.machine:
            self.machine.release_outlet()


class CoffeeMachine:

    def __init__(self, outlets, ingredient_store, recipes):
        self._outlets = outlets
        self._ingredient_store = ingredient_store
        self._lock = threading.Lock()
        self._recipes = recipes

    def refill_ingredient(self, ingredient: Ingredient, quantity: float):
        self._ingredient_store.refill(ingredient, quantity)

    def release_outlet(self):
        with self._lock:
            self._outlets += 1

    def serve(self, recipe):
        if recipe not in self._recipes:
            raise RecipeNotFoundError("Recipe not found in machine.")
        with self._lock:
            if self._outlets == 0:
                raise OutletNotFoundError("No outlet available to serve")
            recipe.take_ingredients(self._ingredient_store)
            self._outlets -= 1
            print(f"Making: {recipe}", flush=True)
            t = MachineThread(target=recipe.make, args=(), machine=self)
            t.start()
