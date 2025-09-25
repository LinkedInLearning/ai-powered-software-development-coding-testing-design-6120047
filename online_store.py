from datetime import datetime
from typing import List, Dict, Optional
import uuid

class Product:
    """Represents a product in the online store."""
    
    def __init__(self, product_id: str, name: str, price: float, description: str = "", category: str = ""):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.description = description
        self.category = category
        self.created_at = datetime.now()
    
    def __str__(self):
        return f"{self.name} - ${self.price:.2f}"
    
    def __repr__(self):
        return f"Product(id='{self.product_id}', name='{self.name}', price={self.price})"
    
    def update_price(self, new_price: float):
        """Update the product price."""
        if new_price < 0:
            raise ValueError("Price cannot be negative")
        self.price = new_price
    
    def get_info(self) -> Dict:
        """Get product information as dictionary."""
        return {
            'product_id': self.product_id,
            'name': self.name,
            'price': self.price,
            'description': self.description,
            'category': self.category,
            'created_at': self.created_at.isoformat()
        }

class ShoppingCart:
    """Manages shopping cart functionality."""
    
    def __init__(self):
        self.items: Dict[str, int] = {}  # product_id -> quantity
        self.products: Dict[str, Product] = {}  # product_id -> Product object
    
    def add_item(self, product: Product, quantity: int = 1):
        """Add item to cart."""
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        
        if product.product_id in self.items:
            self.items[product.product_id] += quantity
        else:
            self.items[product.product_id] = quantity
            self.products[product.product_id] = product
    
    def remove_item(self, product_id: str, quantity: int = None):
        """Remove item from cart."""
        if product_id not in self.items:
            raise ValueError("Product not in cart")
        
        if quantity is None or quantity >= self.items[product_id]:
            del self.items[product_id]
            del self.products[product_id]
        else:
            self.items[product_id] -= quantity
    
    def update_quantity(self, product_id: str, quantity: int):
        """Update item quantity in cart."""
        if product_id not in self.items:
            raise ValueError("Product not in cart")
        
        if quantity <= 0:
            self.remove_item(product_id)
        else:
            self.items[product_id] = quantity
    
    def get_total(self) -> float:
        """Calculate total cart value."""
        total = 0
        for product_id, quantity in self.items.items():
            total += self.products[product_id].price * quantity
        return total
    
    def get_item_count(self) -> int:
        """Get total number of items in cart."""
        return sum(self.items.values())
    
    def clear(self):
        """Clear all items from cart."""
        self.items.clear()
        self.products.clear()
    
    def get_cart_summary(self) -> List[Dict]:
        """Get detailed cart summary."""
        summary = []
        for product_id, quantity in self.items.items():
            product = self.products[product_id]
            summary.append({
                'product_id': product_id,
                'name': product.name,
                'price': product.price,
                'quantity': quantity,
                'subtotal': product.price * quantity
            })
        return summary

class Customer:
    """Represents a customer in the online store."""
    
    def __init__(self, customer_id: str, name: str, email: str, phone: str = ""):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.phone = phone
        self.address = None
        self.created_at = datetime.now()
        self.orders: List['Order'] = []
    
    def __str__(self):
        return f"Customer: {self.name} ({self.email})"
    
    def set_address(self, street: str, city: str, state: str, zip_code: str, country: str = "USA"):
        """Set customer address."""
        self.address = {
            'street': street,
            'city': city,
            'state': state,
            'zip_code': zip_code,
            'country': country
        }
    
    def get_profile(self) -> Dict:
        """Get customer profile information."""
        return {
            'customer_id': self.customer_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'created_at': self.created_at.isoformat(),
            'total_orders': len(self.orders)
        }
    
    def add_order(self, order: 'Order'):
        """Add order to customer's order history."""
        self.orders.append(order)

class Order:
    """Represents an order in the online store."""
    
    def __init__(self, order_id: str, customer: Customer, cart: ShoppingCart):
        self.order_id = order_id
        self.customer = customer
        self.items = cart.get_cart_summary()
        self.total_amount = cart.get_total()
        self.status = "pending"
        self.created_at = datetime.now()
        self.shipping_address = customer.address
        self.payment = None
    
    def __str__(self):
        return f"Order {self.order_id} - ${self.total_amount:.2f} - {self.status}"
    
    def update_status(self, new_status: str):
        """Update order status."""
        valid_statuses = ["pending", "confirmed", "processing", "shipped", "delivered", "cancelled"]
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of: {valid_statuses}")
        self.status = new_status
    
    def add_payment(self, payment: 'Payment'):
        """Add payment to order."""
        self.payment = payment
        if payment.is_successful():
            self.update_status("confirmed")
    
    def get_order_summary(self) -> Dict:
        """Get detailed order summary."""
        return {
            'order_id': self.order_id,
            'customer': self.customer.get_profile(),
            'items': self.items,
            'total_amount': self.total_amount,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'shipping_address': self.shipping_address,
            'payment_status': self.payment.status if self.payment else "not_paid"
        }

class Payment:
    """Handles payment processing."""
    
    def __init__(self, payment_id: str, amount: float, payment_method: str):
        self.payment_id = payment_id
        self.amount = amount
        self.payment_method = payment_method
        self.status = "pending"
        self.processed_at = None
        self.transaction_id = None
    
    def __str__(self):
        return f"Payment {self.payment_id} - ${self.amount:.2f} - {self.status}"
    
    def process_payment(self, card_number: str = None, cvv: str = None) -> bool:
        """Process the payment (simplified simulation)."""
        # In a real application, this would integrate with payment gateways
        # For simulation, we'll just validate basic requirements
        
        if self.payment_method == "credit_card":
            if not card_number or not cvv:
                self.status = "failed"
                return False
            
            # Simulate payment processing
            if len(card_number) >= 13 and len(cvv) >= 3:
                self.status = "successful"
                self.transaction_id = f"TXN_{uuid.uuid4().hex[:8].upper()}"
                self.processed_at = datetime.now()
                return True
            else:
                self.status = "failed"
                return False
        
        elif self.payment_method == "paypal":
            # Simulate PayPal processing
            self.status = "successful"
            self.transaction_id = f"PP_{uuid.uuid4().hex[:8].upper()}"
            self.processed_at = datetime.now()
            return True
        
        else:
            self.status = "failed"
            return False
    
    def is_successful(self) -> bool:
        """Check if payment was successful."""
        return self.status == "successful"
    
    def get_payment_info(self) -> Dict:
        """Get payment information."""
        return {
            'payment_id': self.payment_id,
            'amount': self.amount,
            'payment_method': self.payment_method,
            'status': self.status,
            'transaction_id': self.transaction_id,
            'processed_at': self.processed_at.isoformat() if self.processed_at else None
        }

class Inventory:
    """Manages product inventory."""
    
    def __init__(self):
        self.products: Dict[str, Product] = {}
        self.stock: Dict[str, int] = {}  # product_id -> quantity
    
    def add_product(self, product: Product, initial_stock: int = 0):
        """Add product to inventory."""
        self.products[product.product_id] = product
        self.stock[product.product_id] = initial_stock
    
    def update_stock(self, product_id: str, quantity: int):
        """Update product stock quantity."""
        if product_id not in self.products:
            raise ValueError("Product not found in inventory")
        
        if self.stock[product_id] + quantity < 0:
            raise ValueError("Insufficient stock")
        
        self.stock[product_id] += quantity
    
    def get_stock(self, product_id: str) -> int:
        """Get current stock for a product."""
        return self.stock.get(product_id, 0)
    
    def is_in_stock(self, product_id: str, quantity: int = 1) -> bool:
        """Check if product is in stock."""
        return self.get_stock(product_id) >= quantity
    
    def reserve_stock(self, product_id: str, quantity: int) -> bool:
        """Reserve stock for an order."""
        if self.is_in_stock(product_id, quantity):
            self.update_stock(product_id, -quantity)
            return True
        return False
    
    def get_low_stock_products(self, threshold: int = 10) -> List[Dict]:
        """Get products with low stock."""
        low_stock = []
        for product_id, stock in self.stock.items():
            if stock <= threshold:
                product = self.products[product_id]
                low_stock.append({
                    'product': product.get_info(),
                    'current_stock': stock
                })
        return low_stock
    
    def get_inventory_summary(self) -> Dict:
        """Get complete inventory summary."""
        total_products = len(self.products)
        total_stock_value = sum(
            self.products[pid].price * stock 
            for pid, stock in self.stock.items()
        )
        
        return {
            'total_products': total_products,
            'total_stock_value': total_stock_value,
            'low_stock_products': len(self.get_low_stock_products()),
            'products': [
                {
                    'product': self.products[pid].get_info(),
                    'stock': stock
                }
                for pid, stock in self.stock.items()
            ]
        }

# Example usage and testing
if __name__ == "__main__":
    print("E-Commerce Store System Demo")
    print("=" * 40)
    
    # Create inventory
    inventory = Inventory()
    
    # Add products to inventory
    laptop = Product("P001", "Gaming Laptop", 1299.99, "High-performance gaming laptop", "Electronics")
    mouse = Product("P002", "Wireless Mouse", 29.99, "Ergonomic wireless mouse", "Electronics")
    keyboard = Product("P003", "Mechanical Keyboard", 89.99, "RGB mechanical keyboard", "Electronics")
    
    inventory.add_product(laptop, 50)
    inventory.add_product(mouse, 100)
    inventory.add_product(keyboard, 75)
    
    print("✓ Products added to inventory")
    
    # Create customer
    customer = Customer("C001", "John Doe", "john@example.com", "555-1234")
    customer.set_address("123 Main St", "Anytown", "CA", "12345")
    print(f"✓ Customer created: {customer}")
    
    # Create shopping cart
    cart = ShoppingCart()
    cart.add_item(laptop, 1)
    cart.add_item(mouse, 2)
    cart.add_item(keyboard, 1)
    
    print(f"✓ Cart created with {cart.get_item_count()} items")
    print(f"  Total: ${cart.get_total():.2f}")
    
    # Create order
    order = Order("O001", customer, cart)
    print(f"✓ Order created: {order}")
    
    # Process payment
    payment = Payment("PAY001", order.total_amount, "credit_card")
    if payment.process_payment("1234567890123456", "123"):
        print("✓ Payment processed successfully")
        order.add_payment(payment)
    else:
        print("✗ Payment failed")
    
    # Update inventory
    for item in order.items:
        inventory.reserve_stock(item['product_id'], item['quantity'])
    
    print("✓ Stock reserved for order")
    
    # Display final status
    print("\nFinal Status:")
    print(f"Order Status: {order.status}")
    print(f"Payment Status: {payment.status}")
    print(f"Remaining Laptop Stock: {inventory.get_stock('P001')}")
    print(f"Remaining Mouse Stock: {inventory.get_stock('P002')}")
    print(f"Remaining Keyboard Stock: {inventory.get_stock('P003')}")