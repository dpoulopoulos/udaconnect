from app.src.models import Person  # noqa
from app.src.schemas import PersonSchema  # noqa


def register_routes(api, root="api"):
    from app.src.controllers import api

    api.add_namespace(api, path=f"/{root}")
