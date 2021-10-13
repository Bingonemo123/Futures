import multiprocessing
import log_protocols

logger = log_protocols.Archlog

def main():
    import demo

if __name__ == '__main__':
    while True:
        logger.info('High level start')

        Process = multiprocessing.Process(target=main)
        Process.start()
        Process.join(timeout= 15 * 60)

