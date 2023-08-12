"""Strategy pattern, where multiple methods are available 
to perform a task
"""
from fastapi import FastAPI


app = FastAPI()


class PaymentStrategy:
    def pay(self, amount):
        pass


class CreditCardPayment(PaymentStrategy):
    def pay(self, amount):
        return f"Paid {amount} using Credit Card"


class PayPalPayment(PaymentStrategy):
    def pay(self, amount):
        return f"Paid {amount} using PayPal"


class PaymentContext:
    def __init__(self, strategy):
        self._strategy = strategy

    def process_payment(self, amount):
        return self._strategy.pay(amount)


@app.get("/")
async def make_payment(payment_method: str, amount: int):
    if payment_method == "credit_card":
        strategy = CreditCardPayment()
    elif payment_method == "paypal":
        strategy = PayPalPayment()
    else:
        return {"message": "Invalid payment method"}

    context = PaymentContext(strategy)
    result = context.process_payment(amount)
    return {"message": result}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)