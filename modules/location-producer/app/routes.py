def register_routes(api, root="api"):
    from app.src import register_routes as register_location

    # Add routes
    register_location(api, root=root)
