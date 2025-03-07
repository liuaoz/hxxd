class JsonRet:
    def __init__(self, code: int = 200, message: str = 'success', data=None):
        self.code = code
        self.message = message
        self.data = data

    def to_dict(self):
        return {
            'code': self.code,
            'message': self.message,
            'data': self.data
        }
