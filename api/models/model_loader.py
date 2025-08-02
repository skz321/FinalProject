from . import orders, order_details, user, menu_items, reviews, ingredients, menu_item_ingredients


from ..dependencies.database import engine


def index():
    orders.Base.metadata.create_all(engine)
    order_details.Base.metadata.create_all(engine)
    user.Base.metadata.create_all(engine)
    menu_items.Base.metadata.create_all(engine)
    reviews.Base.metadata.create_all(engine)
    ingredients.Base.metadata.create_all(engine)
    menu_item_ingredients.Base.metadata.create_all(engine)


