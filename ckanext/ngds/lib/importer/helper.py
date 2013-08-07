import datetime as datetime
from ckan.lib.base import config
import ckan.controllers.storage as storage

log = __import__("logging").getLogger(__name__)

BUCKET = config.get('ckan.storage.bucket', 'default')

def upload_file_return_path(file_name=None,file_path=None):
    print "file_name %s " % file_name
    print "file_path %s " % file_path
    if file_name is None or file_path is None:
        print "Either file_name or file_path is None"
        return None
    utc_time = datetime.datetime.utcnow()

    generated_dir = str(utc_time.year) +'-'+ str((utc_time.month)).zfill(2) +'-'+ str((utc_time.day)).zfill(2) +'T'+ str((utc_time.hour)).zfill(2) +':'+ str((utc_time.minute)).zfill(2)+':'+ str((utc_time.second)).zfill(2)

    log.debug("Generated directory %s" % generated_dir)

    label = generated_dir+'/'+file_name

    bucket_id = BUCKET

    params = {'filename-original': file_name, 'uploaded-by': u'admin', 'key': label}

    f = open(file_path+file_name, "rb") # notice the b for binary mode
    data = f.read()
    #storage.get_ofs().put_stream(bucket_id, label, stream.file, params)
    ofs = storage.get_ofs()
    ofs.put_stream(bucket_id, label, data, params)
    f.close()

    log.debug("%s File Uploaded successfully." % file_name)

    #uploaded_file_url = h.url_for('storage_file',label=label,qualified=True)
    uploaded_file_url = ofs.get_url(bucket_id,label)

    print "uploaded_file_url: ",uploaded_file_url

    log.info("uploaded_file_url: %s" % uploaded_file_url)

    return uploaded_file_url

def validate_bulkupload_datafile(file_name):
    print "validate the data file..."

def delete_files(file_path,files_to_delete=None,ignore_files=None):

    import os
    os.chdir(file_path)    

    if files_to_delete:
        files_to_iterate = files_to_delete
    else:
        files_to_iterate = os.listdir(".")

    for filename in files_to_iterate:
        isIgnore = False
        if ignore_files :
            if filename in ignore_files:
                isIgnore = True
        if not isIgnore:
            os.unlink(filename)