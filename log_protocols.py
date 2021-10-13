import os
import pathlib
import logging
import logging.handlers

class Archivarius ():
    def __init__(self):
        if os.name == 'posix':
            self.path = pathlib.PurePosixPath(os.path.abspath(__file__)).parent
        else:
            self.path = pathlib.PureWindowsPath(os.path.abspath(__file__)).parent

        '''----------------------------------------------------------------------------------------------'''
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        """StreamHandler"""
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)
        """FileHandler"""
        rotatingfile_handler = logging.handlers.RotatingFileHandler(self.path/'demomain.log', backupCount=5, maxBytes=1073741824)
        rotatingfile_handler.setLevel(logging.INFO)
        rotatingfile_handler.setFormatter(formatter)
        self.logger.addHandler(rotatingfile_handler)


Arch = Archivarius()
Archlog = Arch.logger
Archpath = Arch.path