from django.db import models

# Create your models here.

class DataSource(models.Model):
    name = models.CharField(max_length=100)
    host = models.CharField(max_length=100)
    port = models.CharField(max_length=10)
    database = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.host}:{self.port})"

class SchemaMapping(models.Model):
    source = models.ForeignKey(DataSource, on_delete=models.CASCADE)
    source_table = models.CharField(max_length=100)
    target_table = models.CharField(max_length=100)
    mapping_definition = models.JSONField()
    
    def __str__(self):
        return f"{self.source.name}: {self.source_table} -> {self.target_table}"
