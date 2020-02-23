import io
import logging
import os
from ftplib import FTP


class FtpClient:
    """
        Class for FTP Client
    """

    def download_file_from_ftp_server(self, file_name):
        """ Download file from ftp server to local system

        Parameters
        ----------
        file_name : str
            json file name
        """

        try:
            ftp = FTP(os.getenv("FTP_SERVER"))
            ftp.login(user=os.getenv("FTP_SERVER_USER_NAME"), passwd=os.getenv("FTP_SERVER_PASSWORD"))
            tempFile = open(file_name, "wb")
            ftp.retrbinary("RETR " + file_name, tempFile.write, io.DEFAULT_BUFFER_SIZE)
            ftp.quit()
            tempFile.close()
        except Exception as e:
            logging.error(f"Error While downloading file from ftp server {os.getenv('FTP_SERVER')}{file_name}:{e}")
            raise e
