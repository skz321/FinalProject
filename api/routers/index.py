from . import orders, order_details, user, menu_items, reviews, ingredients, menu_item_ingredients


def load_routes(app):
    app.include_router(orders.router)
    app.include_router(order_details.router)
    app.include_router(user.router)
    app.include_router(menu_items.router)
    app.include_router(reviews.router)
    app.include_router(ingredients.router)
    app.include_router(menu_item_ingredients.router)
