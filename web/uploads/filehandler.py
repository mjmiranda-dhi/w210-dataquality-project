from django.core.files.storage import FileSystemStorage
from . import models

def write_file_to_disk(f, destination):
    with open(destination, 'wb+') as filedest:
        for chunk in f.chunks():
            filedest.write(chunk) 
    #why use this?
    #fs = FileSystemStorage()
    #filename = fs.save(myfile.name, myfile)
    #uploaded_file_url = fs.url(filename)

def save_file(f):
    filename = f.name
    docfile = Document(file=something, filename=filename, creation_date=datetime.datetime.now())           
    print(docfile.creation_date)
    print(docfile.filename)




