from . import orders, order_details, user, menu_items


def load_routes(app):
    app.include_router(orders.router)
    app.include_router(order_details.router)
    app.include_router(user.router)
    app.include_router(menu_items.router)
