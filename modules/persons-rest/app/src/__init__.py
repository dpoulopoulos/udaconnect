def register_routes(api, root="api"):
    from app.src.controllers import api as persons_api

    api.add_namespace(persons_api, path=f"/{root}")
