import uuid
from django.db import models


def certificate_file_path(instance, filename):
    # Upload the PDF file to a "certificates" folder with a unique filename
    return f'certificates/{uuid.uuid4()}.pdf'


class Certificate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    date = models.DateField()
    signature = models.CharField(max_length=100)
    details = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    pdf_file = models.FileField(upload_to=certificate_file_path, null=True, blank=True)

    def __str__(self):
        return self.title
