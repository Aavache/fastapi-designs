from fastapi import FastAPI

app = FastAPI()

class Coffee:
    def cost(self):
        return 5

class MilkDecorator:
    def __init__(self, coffee):
        self._coffee = coffee

    def cost(self):
        return self._coffee.cost() + 2

class SugarDecorator:
    def __init__(self, coffee):
        self._coffee = coffee

    def cost(self):
        return self._coffee.cost() + 1

@app.get("/")
async def order_coffee():
    coffee = Coffee()
    coffee_with_milk = MilkDecorator(coffee)
    coffee_with_milk_and_sugar = SugarDecorator(coffee_with_milk)

    cost = coffee_with_milk_and_sugar.cost()
    return {"message": "Enjoy your coffee!", "total_cost": cost}
