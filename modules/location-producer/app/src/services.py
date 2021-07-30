import os
import json
import logging

from typing import Dict

from kafka import KafkaProducer

from app import db
from app.src.models import Location


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("udaconnect-api")

KAFKA_URL = os.environ["KAFKA_URL"]
KAFKA_TOPIC = os.environ["KAFKA_TOPIC"]

producer = KafkaProducer(bootstrap_servers=KAFKA_URL)


class LocationService:
    @staticmethod
    def retrieve(location_id) -> Location:
        location, coord_text = (
            db.session.query(Location, Location.coordinate.ST_AsText())
            .filter(Location.id == location_id)
            .one()
        )

        # Rely on database to return text form of point to reduce overhead of conversion in app code
        location.wkt_shape = coord_text
        return location

    @staticmethod
    def create(location: Dict) -> Location:
        encoded_data = json.dumps(location, indent=2).encode('utf-8')
        producer.send(KAFKA_TOPIC, encoded_data)
