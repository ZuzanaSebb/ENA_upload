from ftplib import FTP

# Replace these with your FTP server credentials
ftp_host = 'webin2.ebi.ac.uk'
ftp_user = 'Webin-66822'
ftp_passwd = 'Quaternion07!'

# Connect to the FTP server
ftp = FTP(ftp_host)
ftp.login(ftp_user, ftp_passwd)

# List files in the current directory
ftp.dir()



# Upload a file
with open('/Users/zsebechle/ENA_test/ena_uploader/experiment/mantis_religiosa_R2.fastq.gz', 'rb') as file:
    ftp.storbinary('STOR mantis_religiosa_R2.fastq.gz', file)

# Close the FTP connection
ftp.quit()
