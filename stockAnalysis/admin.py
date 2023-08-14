from django.contrib import admin
from stockAnalysis.models import AnalyzedStock
from stockAnalysis.models import StockSymbol


admin.site.register(AnalyzedStock)
admin.site.register(StockSymbol)
