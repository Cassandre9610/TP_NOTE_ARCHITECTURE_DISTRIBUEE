import grpc
from concurrent import futures
import schedule_pb2
import schedule_pb2_grpc
import json

class ScheduleServicer(schedule_pb2_grpc.ScheduleServicer):

    def __init__(self):
        with open('{}/data/times.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["schedule"]

    def GetSchedule(self, request, context):
        return super().GetSchedule(request, context)

    def GetScheduleByDate(self, request, context):
        return super().GetScheduleByDate(request, context)

    def GetScheduleByMovieId(self, request, context):
        return super().GetScheduleByMovieId(request, context)

    def CreateSchedule(self, request, context):
        return super().CreateSchedule(request, context)

    def DeleteMovieFromDate(self, request, context):
        return super().DeleteMovieFromDate(request, context)

    def DeleteScheduleByDate(self, request, context):
        return super().DeleteScheduleByDate(request, context)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    schedule_pb2_grpc.add_ScheduleServicer_to_server(ScheduleServicer(), server)
    server.add_insecure_port('[::]:3002')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
