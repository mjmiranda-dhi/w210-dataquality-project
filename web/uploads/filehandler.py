from django.core.files.storage import FileSystemStorage
from . import models
import os

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


def process_file(f):
    print("process_file:", type(f))
    b = f.file
    print("process_file after open:", type(b))
    #for chunk in f.chunks():
    #    filedest.write(chunk)
    print("file size:",os.path.size(b))


#FROM STACKOVERFLOW PROGRESS INFO incomplete. 
def get_chunks(file_size):
    chunk_start = 0
    chunk_size = 0x20000  # 131072 bytes, default max ssl buffer size
    while chunk_start + chunk_size < file_size:
        yield(chunk_start, chunk_size)
        chunk_start += chunk_size

    final_chunk_size = file_size - chunk_start
    yield(chunk_start, final_chunk_size)


def read_file_chunked(file_path):
    with open(file_path) as file_:
        file_size = os.path.getsize(file_path)

        print('File size: {}'.format(file_size))

        progress = 0

        for chunk_start, chunk_size in get_chunks(file_size):

            file_chunk = file_.read(chunk_size)

            # do something with the chunk, encrypt it, write to another file...

            progress += len(file_chunk)
            print('{0} of {1} bytes read ({2}%)'.format(
                progress, file_size, int(progress / file_size * 100))
            )
#FROM STACKOVERFLOW PROGRESS INFO incomplete. 
