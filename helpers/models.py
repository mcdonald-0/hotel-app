# This is the tracking model which is an abstract model and this would be added to other apps to track when they were created or updated
# It orders the items from the last created to the first created

from django.db import models


class TrackingModel(models.Model):
	created_at = models.DateTimeField(auto_now_add=True, null=True)
	updated_at = models.DateTimeField(auto_now=True, null=True)

	class Meta:
		abstract = True
		ordering = ('-created_at',)
		
