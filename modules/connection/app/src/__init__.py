def register_routes(api, root="api"):
    from app.src.controllers import api

    api.add_namespace(api, path=f"/{root}")
