from boofuzz import *
from lib.Decrypt import getSessionID
import requests

def check_alive(url):
    flag = False
    try:
        requests.get(url)
        flag = True
    except Exception as e:
        print(e)

    return flag

class Fuzz():
    def __init__(self,ip,username,password,cmd):
        self.ip = ip
        self.cmd = cmd
        self.username = username
        self.password = password

    def cmd_log(self,data):
        print("[+]"+data.decode())
        return data

    def alive(self,target, my_logger, session, *args, **kwargs):
        url = "http://"+self.ip
        flag = check_alive(url)
        if flag:
            my_logger.log_pass('HTTP alive')
        else:
            print('http down')
            my_logger.log_fail('HTTP down')
            exit(1)

    def fuzz_start(self):
        url = "http://"+self.ip
        s_initialize('webfuzz')
        sessionID = getSessionID(url,self.username,self.password)
        s_static("POST /stok="+sessionID+"/ds HTTP/1.1\r\n")
        s_static('Host: ' + self.ip + '\r\n')
        s_static('Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3\r\n')
        s_static('Accept-Encoding: gzip, deflate\r\n')
        s_static('Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n')
        s_static('User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0\r\n')
        s_static('Content-Length: ')
        s_size('length', output_format='ascii', fuzzable=False)
        s_static('\r\n\r\n')

        s_block_start("length")
        s_block_start("data",encoder = self.cmd_log)

        list = cmd.split("<replace>")

        s_static(list[0])
        s_string('*')
        s_static(list[1])
        s_block_end("data")
        s_block_end("length")

        session = Session(
            target=Target(
                connection=SocketConnection(ip, 80, proto='tcp'),

            ),
            # fuzz_loggers=my_logger,
            crash_threshold_element=1,

        )

        session.connect(s_get('webfuzz'), callback= self.alive)
        session.fuzz()

if __name__ == '__main__':
    cmd = '{"system":{"boot_set_date":{"seconds_from_1970":<replace>}},"method":"do"}'
    ip = "192.168.1.38"
    username = "admin"
    password = "admin123"
    fuzz = Fuzz(ip,username,password,cmd)
    fuzz.fuzz_start()


