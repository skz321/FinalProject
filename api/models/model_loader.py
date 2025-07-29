from . import orders, order_details, recipes, food_items, resources, user, menu_items, restaurants, payment


from ..dependencies.database import engine


def index():
    orders.Base.metadata.create_all(engine)
    order_details.Base.metadata.create_all(engine)
    recipes.Base.metadata.create_all(engine)
    food_items.Base.metadata.create_all(engine)
    resources.Base.metadata.create_all(engine)
    restaurants.Base.metadata.create_all(engine)
    user.Base.metadata.create_all(engine)
    menu_items.Base.metadata.create_all(engine)
    payment.Base.metadata.create_all(engine)

