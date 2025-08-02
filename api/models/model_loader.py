from . import orders, order_details, food_items, user, menu_items, payment


from ..dependencies.database import engine


def index():
    orders.Base.metadata.create_all(engine)
    order_details.Base.metadata.create_all(engine)
    food_items.Base.metadata.create_all(engine)
    user.Base.metadata.create_all(engine)
    menu_items.Base.metadata.create_all(engine)
    payment.Base.metadata.create_all(engine)

