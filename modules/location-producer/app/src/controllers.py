from flask import request, Response
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource

from app.src.models import Location
from app.src.schemas import LocationSchema
from app.src.services import LocationService


DATE_FORMAT = "%Y-%m-%d"

api = Namespace("UdaConnect", description="Connections via geolocation.")  # noqa


@api.route("/locations")
@api.route("/locations/<location_id>")
@api.param("location_id", "Unique ID for a given Location", _in="query")
class LocationResource(Resource):
    @accepts(schema=LocationSchema)
    def post(self) -> Location:
        request.get_json()
        LocationService.create(request.get_json())
        return Response(status=202)

    @responds(schema=LocationSchema)
    def get(self, location_id) -> Location:
        location: Location = LocationService.retrieve(location_id)
        return location
