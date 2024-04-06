"""
Протестируйте классы из модуля homework/models.py
"""
import pytest
from tests.models import Product, Cart


@pytest.fixture
def product():

    # item = Product("book", 100, "This is a book", 1000)
    # return item

    return Product("book", 100, "This is a book", 1000)

@pytest.fixture
def cart():

    return Cart()

class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):
        # TODO напишите проверки на метод check_quantity
        stock = product.quantity

        assert product.check_quantity(stock)
        assert product.check_quantity(0)
        assert product.check_quantity(-1)
        assert product.check_quantity(stock + 1) == False

    def test_product_buy(self, product):
        # TODO напишите проверки на метод buy

        in_cart = 1

        before_buy = product.quantity
        product.buy(in_cart)
        after_buy = product.quantity

        assert after_buy == before_buy - in_cart

        in_cart = after_buy

        before_buy = product.quantity
        product.buy(in_cart)
        after_buy = product.quantity

        assert after_buy == before_buy - in_cart

    def test_product_buyx(self, product):
        # TODO напишите проверки на метод buy
        product.buy(50)

        assert product.check_quantity(700)


    def test_product_buy_more_than_available(self, product):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии

        stock = product.quantity

        with pytest.raises(ValueError):
            product.buy(stock + 1)

class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """

    def test_add_product_to_cart(self, cart, product):
        # TODO написать проверку на метод add_product

        cart.add_product(product, 0)
        assert cart.products[product] == 0

        cart.add_product(product)
        assert cart.products[product] == 1

        cart.add_product(product,1000)
        assert cart.products[product] == 1001
    def test_remove_product_from_cart(self, cart, product):
        # TODO написать проверку на метод remove_product

        cart.add_product(product, 1000)
        cart.remove_product(product, 1)
        assert cart.products[product] == 999

        cart.remove_product(product, 999)
        assert product not in cart.products

        cart.add_product(product, 1000)
        cart.remove_product(product, 0)
        assert cart.products[product] == 1000

        cart.remove_product(product, 1500)
        assert product not in cart.products

        with pytest.raises(KeyError):
            cart.remove_product(product, 1)

        cart.add_product(product, 1000)
        cart.remove_product(product)
        assert product not in cart.products


    def test_cart_clear(self, cart, product):
        cart.add_product(product, 1000)
        cart.clear()
        assert product not in cart.products

    def test_cart_get_total_price(self, product, cart):
        cart.add_product(product, 1)
        assert cart.get_total_price() == 1 * product.price

        cart.add_product(product, 10)
        assert cart.get_total_price() == (10 + 1) * product.price

        cart.remove_product(product, 2)
        assert cart.get_total_price() == (10 + 1 - 2) * product.price

        cart.remove_product(product, 200)
        assert cart.get_total_price() == 0

    def test_cart_buy(self, product, cart):

        stock = product.quantity

        cart.add_product(product, 1)
        cart.buy()
        assert product.quantity == stock - 1
        assert product not in cart.products

        cart.add_product(product, product.quantity + 1)
        with pytest.raises(ValueError):
            cart.buy()
