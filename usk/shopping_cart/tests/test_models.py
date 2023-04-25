import pytest
from django.contrib.auth.models import User
from shopping_cart.models import Department, Location, Product, ShoppingCart, ShoppingCartItem, Order, OrderItem
from decimal import Decimal


@pytest.mark.django_db
def test_create_department():
    department = Department.objects.create(name="Electronics", taxable=True)
    assert department.name == "Electronics"
    assert department.taxable is True


@pytest.mark.django_db
def test_create_location():
    location = Location.objects.create(
        name="Warehouse", address="123 Warehouse St", place="New York",
        description="Main Warehouse")
    assert location.name == "Warehouse"
    assert location.address == "123 Warehouse St"
    assert location.place == "New York"
    assert location.description == "Main Warehouse"

# Add test cases for other models like Product, ShoppingCart, ShoppingCartItem, Order, and OrderItem


@pytest.fixture
def create_user():
    user = User.objects.create_user(
        username='testuser', password='testpassword')
    return user


@pytest.fixture
def create_department():
    department = Department.objects.create(name="Electronics", taxable=True)
    return department


@pytest.fixture
def create_department_non_taxable():
    department = Department.objects.create(name="Electronics", taxable=False)
    return department


@pytest.fixture
def create_location():
    location = Location.objects.create(
        name="Warehouse", address="123 Warehouse St", place="New York",
        description="Main Warehouse")
    return location


@pytest.fixture
def create_product(create_department, create_location):
    location = create_location
    location.name = "Store A"
    location.save()
    department = create_department
    product = Product.objects.create(
        name="Laptop",
        description="A great laptop",
        price=1000,
        cost=800,
        department=department,
        location=location,
    )
    return product


@pytest.mark.django_db
def test_create_product(create_product):
    product = create_product
    print(product)  # Add this line to print the product object
    assert product.name == "Laptop"
    assert product.description == "A great laptop"
    assert product.price == Decimal(1000)
    assert product.cost == Decimal(800)
    assert product.department.name == "Electronics"
    assert product.location.name == "Store A"


@pytest.mark.django_db
def test_create_shopping_cart(create_user):
    shopping_cart = ShoppingCart.objects.create(user=create_user)
    assert shopping_cart.user == create_user


@pytest.mark.django_db
def test_create_shopping_cart_item(create_user, create_product):
    shopping_cart = ShoppingCart.objects.create(user=create_user)
    shopping_cart_item = ShoppingCartItem.objects.create(
        product=create_product, cart=shopping_cart, quantity=2,
        price=create_product.price)
    assert shopping_cart_item.product == create_product
    assert shopping_cart_item.cart == shopping_cart
    assert shopping_cart_item.quantity == 2
    assert shopping_cart_item.price == create_product.price


@pytest.mark.django_db
def test_create_order(create_user):
    order = Order.objects.create(user=create_user)
    assert order.user == create_user


@pytest.mark.django_db
def test_create_order_item(create_user, create_product):
    order = Order.objects.create(user=create_user)
    order_item = OrderItem.objects.create(
        order=order, product=create_product, quantity=3,
        price=create_product.price)
    assert order_item.order == order
    assert order_item.product == create_product
    assert order_item.quantity == 3
    assert order_item.price == create_product.price

# Test the get_sales_tax method for ShoppingCart:

# Test when no items are taxable.
# Test when all items are taxable.
# Test when some items are taxable and some are not.
# Test adding multiple products to a shopping cart and updating the quantity.

# Test the deletion of items from the shopping cart and the effect on the shopping cart's total price.

# Test creating an order and its associated order items.

# Test updating an order and its associated order items.

# Test the deletion of an order and its associated order items.

# Test the string representation methods (str) for each model.

# Test the get_total_price method for Order.

# Test the get_total_price method for OrderItem.


@pytest.mark.django_db
def test_get_sales_tax_no_items_taxable(create_user, create_product):
    shopping_cart = ShoppingCart.objects.create(user=create_user)
    shopping_cart_item = ShoppingCartItem.objects.create(
        product=create_product, cart=shopping_cart, quantity=2,
        price=create_product.price)
    assert shopping_cart.get_sales_tax() == Decimal(0)
    assert shopping_cart.get_total_price() == Decimal(2000)
    assert shopping_cart.get_total_price_with_tax() == Decimal(2000)
    assert shopping_cart.get_total_tax() == Decimal(0)
    assert shopping_cart.get_total_price_with_tax() == Decimal(2000)
    
    
@pytest.mark.django_db
def test_get_sales_tax_all_items_taxable(create_user, create_product):
    shopping_cart = ShoppingCart.objects.create(user=create_user)
    shopping_cart_item = ShoppingCartItem.objects.create(
        product=create_product, cart=shopping_cart, quantity=2,
        price=create_product.price)
    create_product.department.taxable = True
    create_product.department.save()
    assert shopping_cart.get_sales_tax() == Decimal(200)
    assert shopping_cart.get_total_price() == Decimal(2000)
    assert shopping_cart.get_total_price_with_tax() == Decimal(2200)
    assert shopping_cart.get_total_tax() == Decimal(200)
    assert shopping_cart.get_total_price_with_tax() == Decimal(2200)
    

@pytest.mark.django_db
def test_get_sales_tax_some_items_taxable(create_user, create_product, create_department_non_taxable):
    shopping_cart = ShoppingCart.objects.create(user=create_user)
    shopping_cart_item = ShoppingCartItem.objects.create(
        product=create_product, cart=shopping_cart, quantity=2,
        price=create_product.price)
    create_product.department.taxable = True
    create_product.department.save()
    create_department_non_taxable.taxable = False
    create_department_non_taxable.save()
    assert shopping_cart.get_sales_tax() == Decimal(200)
    assert shopping_cart.get_total_price() == Decimal(2000)
    assert shopping_cart.get_total_price_with_tax() == Decimal(2200)
    assert shopping_cart.get_total_tax() == Decimal(200)
    assert shopping_cart.get_total_price_with_tax() == Decimal(2200)