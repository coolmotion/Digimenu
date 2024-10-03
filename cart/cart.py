from main.models import Portion

class Cart:
    def __init__(self, request, app_id):
        # Initialize the session and app-specific session key
        self.session = request.session
        self.request = request
        # Dynamically create a session key for the app (based on app_id)
        self.session_key = f'app_{app_id}_cart'
        cart = self.session.get(self.session_key)

        # If the session key is not found, initialize an empty cart
        if self.session_key not in request.session:
            cart = self.session[self.session_key] = {}

        self.cart = cart

    def db_add(self, portion, quantity):
        portion_id = str(portion)
        portion_qty = str(quantity)

        if portion_id in self.cart:
            pass
        else:
            # Add the item to the cart
            self.cart[portion_id] = int(portion_qty)

        # Mark the session as modified
        self.session.modified = True

    def add(self, portion, quantity, app_id):
        portion_id = str(portion.id)
        portion_qty = int(quantity)

        # Retrieve the specific cart based on app_id
        self.session_key = f'app_{app_id}_cart'
        self.cart = self.session.get(self.session_key, {})

        if portion_id in self.cart:
            pass
        else:
            # Add the item to the cart with its price
            self.cart[portion_id] = int(portion_qty)

        # Save the updated cart in the session for this app
        self.session[self.session_key] = self.cart
        # Mark the session as modified
        self.session.modified = True

    def cart_total(self, app_id):
        # Retrieve the specific cart based on app_id
        self.session_key = f'app_{app_id}_cart'
        self.cart = self.session.get(self.session_key, {})

        # Get portion IDS
        portion_ids = self.cart.keys()
        # lookup those keys in our portions database model
        portions = Portion.objects.filter(id__in=portion_ids)
        # Get quantities
        quantities = self.cart
        # Start counting at 0
        total = 0

        for key, value in quantities.items():
            # Convert key string into into so we can do math
            key = int(key)
            for portion in portions:
                if portion.id == key:
                    total = total + (portion.price * value)

        return total

    def __len__(self):
        # Return the total number of items in the cart
        return len(self.cart)

    def get_prods(self):
        # Get ids from cart
        portion_ids = self.cart.keys()
        # Use ids to lookup portions in database model
        portions = Portion.objects.filter(id__in=portion_ids)

        return portions

    def get_quants(self):
        # Return the quantities of items in the cart
        return self.cart

    def update(self, portion, quantity, app_id):
        portion_id = str(portion)
        portion_qty = int(quantity)

        # Retrieve the specific cart based on app_id
        self.session_key = f'app_{app_id}_cart'
        self.cart = self.session.get(self.session_key, {})

        # Update the quantity of the item in the cart
        self.cart[portion_id] = portion_qty
        # Mark the session as modified
        self.session.modified = True

    def delete(self, portion, app_id):
        portion_id = str(portion)

        self.session_key = f'app_{app_id}_cart'
        self.cart = self.session.get(self.session_key, {})

        if portion_id in self.cart:
            del self.cart[portion_id]

        self.session[self.session_key] = self.cart
        self.session.modified = True
