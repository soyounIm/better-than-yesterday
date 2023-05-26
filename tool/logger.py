import logging
import typing
import types

def get_logger(logger_name: typing.Union[types.ModuleType, str], level:int=logging.INFO) -> logging.Logger:

  if isinstance(logger_name, types.ModuleType):
    print(f'{logger_name} / {logger_name.__name__}')
    logger_name = logger_name.__name__

  logger = logging.getLogger(logger_name)
  logger.setLevel(level)

  formatter = logging.Formatter('[%(asctime)s][%(levelname)s] %(message)s', datefmt='%Y/%m/%d %H:%M:%S')

  stream_handler = logging.StreamHandler()
  stream_handler.setFormatter(formatter)
  logger.addHandler(stream_handler)

  return logger  
