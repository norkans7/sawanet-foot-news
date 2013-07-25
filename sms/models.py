from django.db import models
from smartmin.models import SmartModel


class SMS(SmartModel):
    text = models.TextField(max_length=160, 
                            help_text="The message/information sent to customers in SMS")
    
    tags = models.ManyToManyField('Tag', related_name="messages",
                                  help_text="The keyword associated with this message")

class Tag(SmartModel):
    name = models.CharField(max_length=64,
                            help_text="the keyword")
