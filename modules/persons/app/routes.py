def register_routes(api, app, root="api"):
    from app.src import register_routes

    # Add routes
    register_routes(api, app)
