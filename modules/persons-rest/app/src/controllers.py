from typing import List

from flask import request
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource

from app.src.models import Person
from app.src.schemas import PersonSchema
from app.src.services import PersonService


api = Namespace("UdaConnect", description="Connections via geolocation.")


@api.route("/persons")
class PersonsResource(Resource):
    @accepts(schema=PersonSchema)
    @responds(schema=PersonSchema)
    def post(self) -> Person:
        payload = request.get_json()
        new_person: Person = PersonService.create(payload)
        return new_person

    @responds(schema=PersonSchema, many=True)
    def get(self) -> List[Person]:
        persons: List[Person] = PersonService.retrieve_all()
        return persons
