import boto3

class AwsCommand:

  def __init__(self, profile:str):
    self._session = boto3.Session(profile_name=profile, region_name='ap-northeast-2')
    self._s3_client = None
    self._s3 = None
    self._command = []

  def __enter__(self):
    return self

  def __exit__(self, exec_type, exec_value, traceback):
    if self._s3:
      del self._s3
    if self._session:
      del self._session
  
  def close(self):
    self.__exit__()

  @property
  def s3(self):
    if not self._s3_client:
      self._s3_client = self._session.client('s3')
    if not self._s3:
      self._s3 = self._session.resource('s3')
    return self

  def bucket(self, bucket_name:str, prefix:str):
    self._bucket_name = bucket_name
    self._prefix = prefix
    self._bucket = self._s3.Bucket(bucket_name)
    return self

  def show_buckets(self):
    for bucket in self._s3.buckets.all():
      print(f'- {bucket.name}')

  def show_objects(self, prefix:str, is_files=False):
    prefix = prefix if prefix else self._prefix
    objects = self._bucket.objects.filter(Prefix=prefix)
    print(len(list(objects)))
    for obj in objects:
      print(obj)
      if is_files is False and obj.key.endswith('/') is False:
        continue
      print(f'- {obj.key}')

  def is_empty(self, prefix:str):
    objects = list(self._bucket.objects.filter(Prefix=prefix))
    return True if len(objects) == 0 else False
  
  def get_info(self, prefix:str):
    res = self._s3_client.list_objects_v2(Bucket=self._bucket_name, Prefix=prefix)
    contents = res.get('Contents')
    total_size = 0
    for data in contents:
      total_size += data.get('Size', 0)
    return { 'count' : len(contents), 'total_size' : total_size }

  def upload_files(self, files:str, obj_name:str):
    return self._s3_client.upload_file(files, self._bucket_name, obj_name) if obj_name else False

  def delete_files(self, prefix:str):
    res = self._s3_client.list_objects_v2(Bucket=self._bucket_name, Prefix=prefix)
    for obj in res.get('Contents'):
      print(f'Deleing {obj["Key"]}')
      self._s3_client.delete_object(Bucket=self._bucket_name, Key=obj['Key'])


if __name__ == "__main__":

  with AwsCommand('default') as aws:
    #aws.s3.show_buckets()
    aws.s3.bucket('bucket name','prefix')
    #aws.show_objects()
    #if aws.upload_files('local file', 's3 file') is False:
    #  print('Failed uploading files!!')

    print('is_empty=', aws.is_empty(prefix='prefix'))
    #print(aws.get_info('path'))
    #aws.delete_files('path')
