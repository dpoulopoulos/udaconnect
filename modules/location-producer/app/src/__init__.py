from app.src.models import Location, Person  # noqa
from app.src.schemas import LocationSchema  # noqa


def register_routes(api, root="api"):
    from app.src.controllers import api as location_api

    api.add_namespace(location_api, path=f"/{root}")
