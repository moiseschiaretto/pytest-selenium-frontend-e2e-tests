class Routes:
    LOGIN = '/'
    INVENTORY = '/inventory.html'
    INVENTORY_ITEM = '/inventory-item.html'
    CART = '/cart.html'
    CHECKOUT_STEP_ONE = '/checkout-step-one.html'
    CHECKOUT_STEP_TWO = '/checkout-step-two.html'
    CHECKOUT_COMPLETE = '/checkout-complete.html'


# Slugs de produto usados pela SauceDemo nos atributos data-test
# (ex.: [data-test="add-to-cart-sauce-labs-backpack"])
class ProductSlugs:
    BACKPACK = 'sauce-labs-backpack'
    BIKE_LIGHT = 'sauce-labs-bike-light'
    BOLT_T_SHIRT = 'sauce-labs-bolt-t-shirt'
    FLEECE_JACKET = 'sauce-labs-fleece-jacket'
    ONESIE = 'sauce-labs-onesie'
    RED_T_SHIRT = 'test.allthethings()-t-shirt-(red)'


class ProductNames:
    BACKPACK = 'Sauce Labs Backpack'
    BIKE_LIGHT = 'Sauce Labs Bike Light'
    BOLT_T_SHIRT = 'Sauce Labs Bolt T-Shirt'


# Ids dos produtos na SauceDemo: usados na URL do detalhe
# (/inventory-item.html?id=4) e no carrinho salvo no localStorage
class ProductIds:
    BACKPACK = 4
    BIKE_LIGHT = 0
    BOLT_T_SHIRT = 1
