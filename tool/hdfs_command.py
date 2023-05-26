import subprocess

class HdfsResult:

  def __init__(self, is_success:bool, stdout:str, stderr:str):
    self._is_success = is_success
    self._stdout = stdout
    self._stderr = stderr

  def __str__(self):
    if self.isSuccess is True:
      return f'{self._stdout}'
    else:
      return f'{self._stderr}'

  @property
  def isSuccess(self):
    return self._is_success

  @property
  def result(self):
    return self._stdout

class HdfsCommand:

  def __init__(self):
    self._command = []
    self._options = []
    self._args = []

  def ls(self, path:str):
    self._command.extend(['hdfs', 'dfs', '-ls'])
    self._args.extend([path])
    return self

  def test(self, path:str):
    self._command.extend(['hdfs', 'dfs', '-test'])
    self._args.extend([path])
    return self

  def count(self, path:str):
    self._command.extend(['hdfs', 'dfs', '-count'])
    self._args.extend([path])
    return self

  def get(self, source:str, target:str):
    self._command.extend(['hdfs', 'dfs', '-get'])
    self._args.extend([source, target])
    return self
 
  def distcp(self, source:str, target:str):
    self._command.extend(['hadoop', 'distcp'])
    self._args.extend([source, target])
    return self

  def options(self, options:list):
    self._options.extend(options)
    return self

  def run(self):
    '''
    '''
    hdfs_command = []
    try:
      if not self._command:
        raise Exception('Invalid hdfs cli')

      hdfs_command = self._command + self._options + self._args
      result = subprocess.run(hdfs_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      if result.returncode != 0:
        raise Exception(f'Failed Command {result.stderr.decode()}')
    except Exception as e:
      return HdfsResult(False, result.stdout.decode(), f'{hdfs_command}, Error Msg:{e}')
    finally:
      self.__init__()
    return HdfsResult(True, result.stdout.decode(), result.stderr.decode())

if __name__ == "__main__":

  import os
  hdfs = HdfsCommand()

  # ls usage
  #print(hdfs.ls('hdfs path').run())

  # distcp
#  print(hdfs.distcp(source='hdfs path', target='hdfs path').options(['-skipcrccheck']).run())

  # get
#  os.makedirs(target_fs_path, exist_ok=True) 
#  print(hdfs.get(source='source path', target=target_fs_path,).run())

  # count
  #print(hdfs.count(path='path').options(['-h']).run())

  #ret = hdfs.count(path='path').run()
  #print(f'{ret.result}')

  ret = hdfs.test(path='path').options(['-s']).run()
  print(f'{ret.isSuccess}')



