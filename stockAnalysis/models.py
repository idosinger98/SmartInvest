from django.db import models
from users.models import Profile


class AnalyzedStocksManager(models.Manager):

    def get_user_stocks(self, analyst_id):
        return self.filter(analyst_id__user_id=analyst_id)

    def get_community_stocks(self):
        return self.filter(is_public=True)


class AnalyzedStock(models.Model):
    analyst_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    stock_image = models.JSONField()    # for now as json. maybe will change.
    description = models.TextField(blank=True)
    is_public = models.BooleanField(default=False)
    objects = AnalyzedStocksManager()


class StockSymbol(models.Model):
    symbol = models.CharField(max_length=7, primary_key=True)