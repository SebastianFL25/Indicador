from django.db import models

class EconomicIndicator(models.Model):
    indicator=models.CharField( max_length=50)
    date = models.DateField()
    value = models.FloatField()
    
    def __str__(self) -> str:
        return '%s %s %s'%(self.indicator, self.date, self.value)
