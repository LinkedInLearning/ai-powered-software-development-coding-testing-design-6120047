class PaymentProcessor:
    def pay(self, method: str, amount: float):
        if method == "credit_card":
            print(f"Processing credit card payment of ${amount}")
        elif method == "paypal":
            print(f"Processing PayPal payment of ${amount}")
        elif method == "crypto":
            print(f"Processing crypto payment of ${amount}")
        else:
            raise ValueError("Unknown payment method")