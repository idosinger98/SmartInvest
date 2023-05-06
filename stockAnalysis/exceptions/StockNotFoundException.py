
class StockNotFoundException(Exception):

    def __init__(self, message=""):
        self.message = 'Symbol not found / no trading in that period - ' + message
        super().__init__(self.message)
