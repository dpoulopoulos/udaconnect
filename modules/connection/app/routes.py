def register_routes(api, root="api"):
    from app.src import register_routes as register_connection

    # Add routes
    register_connection(api)
