def register_routes(api, root="api"):
    from app.src.controllers import api as connection_api

    api.add_namespace(connection_api, path=f"/{root}")
