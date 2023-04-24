from django.db import models

# Create your models here.
class Vehicle(models.Model):
    choices = (
        ('Electric', 0),
        ('Hybrid', 1)
    )

    name = models.CharField(max_length=30, unique=True)
    type = models.CharField(max_length=20, choices=choices, default=0)
    nominal_energy = models.FloatField()
    nominal_autonomy = models.FloatField()
    charging_power = models.FloatField()
    charging_time = models.FloatField()
    fuel_autonomy = models.FloatField(null=True, blank=True)
    tank_capacity = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = 'Vehicle'
    
    def __str__(self):
        return f'{self.name} - {self.type} - {self.nominal_energy} - {self.nominal_autonomy} - {self.charging_power} - {self.charging_time} - {self.fuel_autonomy} - {self.tank_capacity}'