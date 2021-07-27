import time

from concurrent import futures

import grpc

from sqlalchemy.sql import text
from sqlalchemy import create_engine

import person_pb2
import person_pb2_grpc


# DB_USERNAME = os.environ["DB_USERNAME"]
# DB_PASSWORD = os.environ["DB_PASSWORD"]
# DB_HOST = os.environ["DB_HOST"]
# DB_PORT = os.environ["DB_PORT"]
# DB_NAME = os.environ["DB_NAME"]

DB_USER = "ct_admin"
DB_NAME = "geoconnections"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_PASS = "wowimsosecure"


class PersonServicer(person_pb2_grpc.PersonServiceServicer):
    def Get(self, request, context):
        response = person_pb2.PersonMessageList()

        engine = create_engine(
            f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
            echo=True
        )
        conn = engine.connect()

        query = text("SELECT * FROM Person")

        result = conn.execute(query)

        for row in result:
            person = person_pb2.PersonMessage(
                id=row.id,
                first_name = row.first_name,
                last_name = row.last_name,
                company_name = row.company_name
            )
            response.persons.append(person)
        
        print(response)
        return response


# Initialize gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
person_pb2_grpc.add_PersonServiceServicer_to_server(PersonServicer(), server)


print("Server starting on port 5005...")
server.add_insecure_port("[::]:5005")
server.start()
# Keep thread alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)