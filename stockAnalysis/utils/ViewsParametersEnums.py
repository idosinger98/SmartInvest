import enum


class SearchStockViewParameters(enum.Enum):
    INTERVAL = 'interval'
    FROM = 'from'
    TO = 'to'
    STOCK_SYMBOL = 'sy'
    STOCK = 'stock'
    STOCK_DATA = 'stock_data'
    INDICATORS = 'indicators'


class IndicatorsViewParameters(enum.Enum):
    INDICATORS = 'indicators'
    STOCK = 'stock'


class SaveStockViewParameters(enum.Enum):
    CHART = 'chart'
    PUBLISH = 'is_public'
    DESCRIPTION = 'description'
    TITLE = 'title'


class ChartDetails(enum.Enum):
    INDICATORS = 'indicators'
    DATA = 'data'
    ANNOTATIONS = 'annotations'
