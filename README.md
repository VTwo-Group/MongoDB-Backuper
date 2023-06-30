# MongoDB-Backuper
MongoDB Backuper & upload on FTP.
MongoDB database backuper. First, it is backed up, and after zipping and deleting the zipped directory, it is sent to FTP server. 

In addition, the last 5 new files are kept both in the ftp server and in the saved location, and the rest are deleted. Of course, this number can be edited.
Other names can be edited.
## Restore
You can also use the following command to restore:
```shell
mongorestore -d db1 --dir /opt/backup/db1/
```
