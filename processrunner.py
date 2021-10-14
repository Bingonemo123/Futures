import multiprocessing
import log_protocols
import inspect
logger = log_protocols.Archlog

importer = inspect.getmodulename(inspect.stack()[-1][1])

class Space:
    def __init__(self):
        self.var = 0

logger.info('High level Entry')
def main():
    mainmodule = __import__ (importer)

if __name__ != '__main__':
    while True:
        logger.debug('High level start')

        Process = multiprocessing.Process(target=main)
        Process.start()
        Process.join(timeout= 15 * 60)

