import os
import logging

from typing import Dict, List
from datetime import datetime, timedelta

import grpc

from sqlalchemy.sql import text

import app.src.person_pb2 as person_pb2
import app.src.person_pb2_grpc as person_pb2_grpc

from app import db
from app.src.models import Connection, Location, Person


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("connection-api")


PERSONS_GRPC_URL = os.environ.get("PERSONS_GRPC_URL", "localhost:30003")


class ConnectionService:
    @staticmethod
    def find_contacts(person_id: int, start_date: datetime, end_date: datetime, meters=5
    ) -> List[Connection]:
        """
        Finds all Person who have been within a given distance of a given Person within a date range.

        This will run rather quickly locally, but this is an expensive method and will take a bit of time to run on
        large datasets. This is by design: what are some ways or techniques to help make this data integrate more
        smoothly for a better user experience for API consumers?
        """
        locations: List = db.session.query(Location).filter(
            Location.person_id == person_id
        ).filter(Location.creation_time < end_date).filter(
            Location.creation_time >= start_date
        ).all()

        # Cache all users in memory for quick lookup
        person_map: Dict[str, Person] = {
            person.id: person for person in PersonService.retrieve_all()}

        # Prepare arguments for queries
        data = []
        for location in locations:
            data.append(
                {
                    "person_id": person_id,
                    "longitude": location.longitude,
                    "latitude": location.latitude,
                    "meters": meters,
                    "start_date": start_date.strftime("%Y-%m-%d"),
                    "end_date": (end_date + timedelta(days=1)).strftime("%Y-%m-%d"),
                }
            )

        query = text(
            """
        SELECT  person_id, id, ST_X(coordinate), ST_Y(coordinate), creation_time
        FROM    location
        WHERE   ST_DWithin(coordinate::geography,ST_SetSRID(ST_MakePoint(:latitude,:longitude),4326)::geography, :meters)
        AND     person_id != :person_id
        AND     TO_DATE(:start_date, 'YYYY-MM-DD') <= creation_time
        AND     TO_DATE(:end_date, 'YYYY-MM-DD') > creation_time;
        """
        )
        result: List[Connection] = []
        for line in tuple(data):
            for (
                exposed_person_id,
                location_id,
                exposed_lat,
                exposed_long,
                exposed_time,
            ) in db.engine.execute(query, **line):
                location = Location(
                    id=location_id,
                    person_id=exposed_person_id,
                    creation_time=exposed_time,
                )
                location.set_wkt_with_coords(exposed_lat, exposed_long)

                result.append(
                    Connection(
                        person=person_map[exposed_person_id], location=location,
                    )
                )

        return result

class PersonService:
    @staticmethod
    def retrieve_all() -> List[Person]:
        persons = []

        channel = grpc.insecure_channel(PERSONS_GRPC_URL)
        stub = person_pb2_grpc.PersonServiceStub(channel)

        response = stub.Get(person_pb2.Empty())
        
        for p in response.persons:
            person = Person()
            person.id = p.id
            person.first_name = p.first_name
            person.last_name = p.last_name
            person.company_name = p.company_name
            persons.append(person)

        return persons
