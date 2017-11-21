from domain import Resource
class Rope(Resource):
    def __init__(self, count):
        Resource.__init__(self, __class__.__name__.lower(),  count)


