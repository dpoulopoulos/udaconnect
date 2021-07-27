def register_routes(api, root="api"):
    from app.src import register_routes as register_persons

    # Add routes
    register_persons(api, root=root)
