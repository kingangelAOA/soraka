
class TaskTypeError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)

class TasksTypeError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)