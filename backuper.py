# Author: Mehrdad Shoja, VTwo.org
import urllib.request
import subprocess
import datetime
import os
import ftplib

# Init
dbs = ['db1', 'db2']
backup_base_dir_name = 'mb_backups'
backup_base_dir_path = '/opt/' + backup_base_dir_name + '/'
ftp_host = 'ftp.example.com'
ftp_username = 'username'
ftp_password = 'password'
backup_files_limit = 5

try:
    # Needed for filename
    now = datetime.datetime.now()
    date_time_postfix = now.strftime("%Y.%m.%d_%H.%M.%S")
    dir_name = date_time_postfix
    zip_file_name = dir_name + '.zip'
    backup_dir = backup_base_dir_path + dir_name + '/'

    # Make backup base dir
    subprocess.run('mkdir -p ' + backup_dir, shell=True)

    # Dump dbs
    for db_name in dbs:
        subprocess.run('mongodump -d {dbname} -o {backupdir}'.format(backupdir=backup_dir, dbname=db_name), shell=True)

    # Zip dump
    subprocess.run(
        'cd {backupbasedir} && zip -r {backupbasedir}{zipfilename} ./{dirname} && cd -'.format(
            backupbasedir=backup_base_dir_path,
            zipfilename=zip_file_name,
            dirname=dir_name), shell=True)

    # Remove unnecessary dir
    subprocess.run('rm -rf {backupdir}'.format(backupdir=backup_dir), shell=True)

    # Remove the oldest zip files by limit
    for filename in sorted(os.listdir(backup_base_dir_path))[:-backup_files_limit]:
        filename_relPath = os.path.join(backup_base_dir_path, filename)
        os.remove(filename_relPath)

    # Connect to ftp
    ftp_session = ftplib.FTP(ftp_host, ftp_username, ftp_password)

    # Make dir if not exists & cd dir
    if not (backup_base_dir_name in ftp_session.nlst()):
        ftp_session.mkd(backup_base_dir_name)
    ftp_session.cwd('/' + backup_base_dir_name)

    # Send file
    file = open(backup_base_dir_path + zip_file_name, 'rb')
    ftp_session.storbinary('STOR /' + backup_base_dir_name + '/' + zip_file_name, file)
    file.close()

    # List of files: session.retrlines('LIST ./gps-tracking-mongo-backup')  # list directory contents

    # Remove the oldest zip files by limit
    dir_list = []
    files = []
    ftp_session.dir(dir_list.append)
    for line in dir_list:
        filename = line.strip().split(' ')[-1]
        if filename != '.' and filename != '..':
            files.append(filename)

    files.sort(reverse=True)
    files = files[backup_files_limit:]
    for filename in files:
        # If file exists! - to ensure
        if filename in ftp_session.nlst():
            ftp_session.delete(filename)

    # Close connection
    ftp_session.quit()
    print('Done.')
except:
    print('Error.')
