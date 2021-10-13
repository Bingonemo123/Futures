import multiprocessing
import log_protocols

logger = log_protocols.Archlog

logger.info('High level Entry')
def main():
    import demo

if __name__ == '__main__':
    while True:
        logger.debug('High level start')

        Process = multiprocessing.Process(target=main)
        Process.start()
        Process.join(timeout= 15 * 60)

