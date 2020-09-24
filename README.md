# redis-dump-backup
Remote redis-dump and file backup to either filesystem or google bucket

There is k8 files tested on GKE that run as a cron job at 23:00 (feel free to modify the schedule)

redis-dump-backup is a python script that essentially runs a rrd dump and then saves the file somewhere to a backend provider.

Current providers are
- file
- bucket (Google Bucket)

You can run multiple providers at the same time if you like.

## Installation
pipenv install  
pipenv shell  

### Edit redis-dump-backup.conf
Edit the redis-dump-backup.conf file

Current backup methods are: (you can have multiple, seperated by a comma)  
method=file,bucket

## TODO
By default we look for a config file redis-dump-backup.conf. Implement command line args to specify this file  
File: Implement max amount of files for rotation  
AWS: Yeah  
Write the backup verify function (and veryify) on a backup. (I've verified manually, it seems ok)  

