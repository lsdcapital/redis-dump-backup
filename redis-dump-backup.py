import configparser
import datetime
import logging
import os
import subprocess
import sys
import time

from google.cloud import storage
from str2bool import str2bool

def getConfig(conf='redis-dump-backup.conf', section='backup'):
    config = configparser.ConfigParser()
    config.read(conf)
    return {k:v for k, v in config[section].items()}

def dump():
    config = getConfig()

    logger.info("Dumping redis rdb")
    if not str2bool(config['test']):
        subprocess.run(["redis-cli", "-h", config['hostname'], config['port'], "--rdb", "/tmp/redis-dump-backup.rdb"], shell=True, check=True)
        backup()
    else:
        logger.warning('Running in test mode (test=true) and simulating a redis-dump-backup')
        with open('/tmp/redis-dump-backup.rdb', 'w') as file:
            file.write('This is a redis test file')
        backup()

def backup():
    config = getConfig()

    date = datetime.datetime.now()
    datefile = date.strftime("%Y-%m-%d-%X")

    with open("/tmp/redis-dump-backup.rdb", "rb") as file:
        data = file.read()

    for method in config['method'].split(','):
        if method == 'file':
            cfg = getConfig(section='file')
            filename = cfg['filepath'] + '/' + cfg['filename'] + '-' + datefile + '.backup'
            if not os.path.exists(cfg['filepath']):
                logger.error(f'Backup filepath {cfg["filepath"]} does not exist. Attemping to create.')
                os.makedirs(cfg['filepath'])

            with open(filename, "wb") as file:
                file.write(data)
            logger.info(f'Created redis rdb backup to file {filename}')

        elif method == 'bucket':
            cfg = getConfig(section='bucket')

            storage_client = storage.Client.from_service_account_json(cfg['credspath'])
            try:
                bucket = storage_client.get_bucket(cfg['bucket'])
            except:
                logger.error('Failed to find Google Bucket')
                logger.error('Known buckets are:')
                buckets = storage_client.list_buckets()
                for bucket in buckets:
                    logger.error(bucket.name)

            # Create tempory file for upload
            filename = cfg['filename'] + '-' + datefile + '.backup'
            with open(filename, "wb") as file:
                file.write(data)
            
            blob = bucket.blob(filename)
            blob.upload_from_filename(filename)
            logger.info(f'Created redis rdb backup on Google Bucket: ' + blob.public_url)
            os.remove(filename)
        else:
            logger.error('No backup methods specified')

def verifyBackup():
    #TODO
    ''' Function to verify redis backup" '''
    pass

#Global logging defintion
config = getConfig()
logger = logging.getLogger()
loglevel = config['loglevel'].upper()
logfile = config['logfile']

logger.setLevel(loglevel)
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')
fh = logging.FileHandler(logfile)
sh = logging.StreamHandler(sys.stdout)
fh.setFormatter(formatter)
sh.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(sh)

def main():
    logger.info('Application Started')
    dump()

if __name__ == "__main__":
    main()
