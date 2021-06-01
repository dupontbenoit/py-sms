#!/usr/bin/env python3

import socket
import sys

class SmsService():

    """
    Service to send SMS using AT commands.
    Based on EDGE router ER75i v2.
    """

    RETURN = chr(13)
    CTRL_Z = chr(26)

    def __init__(self, host: str='192.168.90.103', port: int=8081):
        self.host = host
        self.port = port

    def send_sms(self, phone_number:str, message:str) -> str:
        """
        Send SMS message.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(self.str_to_bytes('AT+CMGF=1' + self.RETURN))
            s.sendall(self.str_to_bytes('AT+CMGS='+ phone_number + self.RETURN))
            s.sendall(self.str_to_bytes(message + self.CTRL_Z))
            data = s.recv(1024)
            return data.decode('utf_8')

    def str_to_bytes(self, string:str):
        """
        Convert string to bytes for the AT command.
        """
        return bytes(string, 'latin_1')


"""
Send a message in command line.
Parameter 1 : phone number.
Parameter 2 : message .

python3 .\send-sms.py 04700000 'sample test'
"""

if __name__ == "__main__":
    smsService: SmsService = SmsService()
    print(smsService.send_sms(sys.argv[1], sys.argv[2]))