import re

# Textos esperados nas telas da SauceDemo, conferidos no código-fonte oficial
# (github.com/saucelabs/sample-app-web) e na versão publicada em www.saucedemo.com


class Texts:
    BROWSER_TITLE = 'Swag Labs'
    LOGO = 'Swag Labs'

    class Login:
        USERNAME_PLACEHOLDER = 'Username'
        PASSWORD_PLACEHOLDER = 'Password'
        BUTTON = 'Login'
        ACCEPTED_USERNAMES = 'Accepted usernames are:'
        PASSWORD_FOR_ALL_USERS = 'Password for all users:'

    class Inventory:
        TITLE = 'Products'
        TOTAL_PRODUCTS = 6
        DEFAULT_SORT = 'Name (A to Z)'
        SORT_OPTIONS = ['Name (A to Z)', 'Name (Z to A)', 'Price (low to high)', 'Price (high to low)']

    class ProductDetails:
        BACK_BUTTON = 'Back to products'

    class Buttons:
        ADD_TO_CART = 'Add to cart'
        REMOVE = 'Remove'

    MENU_ITEMS = ['All Items', 'Dynamic Catalog', 'About', 'Logout', 'Reset App State']

    class Cart:
        TITLE = 'Your Cart'
        CHECKOUT_BUTTON = 'Checkout'
        CONTINUE_SHOPPING_BUTTON = 'Continue Shopping'

    class Checkout:
        INFORMATION_TITLE = 'Checkout: Your Information'
        OVERVIEW_TITLE = 'Checkout: Overview'
        COMPLETE_TITLE = 'Checkout: Complete!'
        COMPLETE_HEADER = 'Thank you for your order!'
        BACK_HOME_BUTTON = 'Back Home'

    class Footer:
        COPYRIGHT = re.compile(r'© \d{4} Sauce Labs\. All Rights Reserved\.')
        SOCIAL_X = 'https://x.com/saucelabs'
        SOCIAL_FACEBOOK = 'https://www.facebook.com/saucelabs'
        SOCIAL_LINKEDIN = 'https://www.linkedin.com/company/sauce-labs/'

    class Errors:
        USERNAME_REQUIRED = 'Epic sadface: Username is required'
        LOCKED_OUT = 'Epic sadface: Sorry, this user has been locked out.'
        INVALID_CREDENTIALS = 'Epic sadface: Username and password do not match any user in this service'
        FIRST_NAME_REQUIRED = 'Error: First Name is required'

        @staticmethod
        def login_required(route):
            return f"Epic sadface: You can only access '{route}' when you are logged in."


PRICE_PATTERN = re.compile(r'^\$\d+\.\d{2}$')
