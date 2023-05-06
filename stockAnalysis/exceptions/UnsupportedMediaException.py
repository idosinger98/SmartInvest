
class UnsupportedMediaException(Exception):

    def __init__(self, message=""):
        self.message = 'Unsupported media, your content should be json ' + message
        super().__init__(self.message)
