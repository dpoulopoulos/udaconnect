import grpc

import person_event_pb2
import person_event_pb2_grpc


print("Requesting Persons...")

channel = grpc.insecure_channel("127.0.0.1:30001")
stub = person_pb2_grpc.PersonServiceStub(channel)

response = stub.Get(person_pb2.Empty())

print(response)