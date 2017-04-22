from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.

class AttemptedManager(models.Manager):
	def get_queryset(self):
		return super(AttemptedManager, self).get_queryset()


class UploadedManager(models.Manager):
	def get_queryset(self):
		return super(UploadedManager, self).get_queryset().filter(uploadSuccessful=True)


class FailedManager(models.Manager):
	def get_queryset(self):
		return super(FailedManager, self).get_queryset().filter(uploadSuccessful=False)


class UploadFile(models.Model):
	userName = models.CharField(max_length=20)
	fullName = models.CharField(max_length=100, blank=True, null=True)
	email = models.EmailField()
	company = models.CharField(max_length=100, blank=True, null=True)
	#fileOrig = models.FileField(upload_to='upload/files/')
	fileOrig = models.CharField(max_length=100)
	uploadSuccessful = models.BooleanField(default=False)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

	objects = models.Manager()
	attempted = AttemptedManager()
	uploaded = UploadedManager()
	failed = FailedManager()

	def __str__(self):
		# Think about how to bring back file details instead.
		return str({
			'userName': self.userName,
			'fileOrig': self.fileOrig,
			'uploadSuccessful': str(self.uploadSuccessful)
			})

	def get_absolute_url(self):
		return reverse('upload:upload_detail_for_user',
			args = [self.userName,
			        self.timestamp.strftime('%Y'),
			        self.timestamp.strftime('%m'),
			        self.timestamp.strftime('%d')
			        ])
