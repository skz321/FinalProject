from . import orders, order_details
from . import promotion_codes


def load_routes(app):
    app.include_router(orders.router)
    app.include_router(order_details.router)
    app.include_router(promotion_codes.router)
