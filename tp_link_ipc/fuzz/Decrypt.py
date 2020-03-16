from Crypto import Random
from Crypto.Hash import SHA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
from Crypto.PublicKey import RSA
import base64

import requests
import json




random_generator = Random.new().read
def encrypt(message, pub_rsa_path):

    with open(pub_rsa_path) as f:
        key = f.read()
        rsakey = RSA.importKey(key)
        cipher = Cipher_pkcs1_v1_5.new(rsakey)
        cipher_text = base64.b64encode(cipher.encrypt(message.encode()))
        return cipher_text

def securityEncode(password,en_str1,en_str2):
    pass_len = len(password)
    str1_len = len(en_str1)
    str2_len = len(en_str2)

    if pass_len > str1_len:

        length = pass_len
    else:
        length = str1_len
    e = ""
    for p in range(0,length):
        n = l = 187
        if p >=  pass_len:
            n = ord(en_str1[p])
        else:
            if p >= str1_len:
                l = ord(password[p])
            else:
                l = ord(password[p])
                n = ord(en_str1[p])
        e += en_str2[(l ^ n) % str2_len]
    return e

def dynEncryptPwd(en_password,nonce):
    import os
    en_password = en_password + ':'+ nonce

    with open("pub_key") as f:
        key = f.read()

    rsakey = RSA.importKey(key)
    cipher = Cipher_pkcs1_v1_5.new(rsakey)
    cipher_text = base64.b64encode(cipher.encrypt(en_password.encode()))
    return cipher_text

def password_encry(password,nonce):
    en_password = securityEncode(password, 'RDpbLfCPsJZ7fiv',
                                 'yLwVl0zKqws7LgKPRQ84Mdt708T1qQ3Ha7xv3H7NyU84p21BriUWBU43odz3iP4rBL3cD02KZciXTysVXiV8ngg6vL48rPJyAUw0HurW20xqxv9aYb4M9wK1Ae0wlro510qXeU07kV57fQMc8L6aLgMLwygtc0F10a0Dg70TOoouyFhdysuRMO51yY5ZlOZZLEal1h0t9YQW0Ko7oBwmCAHoic4HYbUyVeU3sfQ1xtXcPcf1aT303wAQhv66qzW')
    enpass = dynEncryptPwd(en_password, nonce)

    return enpass.decode()


def getSessionID(url,username,password):
    data = '{"method":"do","login":{"username":"<user_replace>","password":"<pass_replace>","encrypt_type":"2"}}'
    re = requests.post(url, data)

    authRltObj = json.loads(re.text)

    nonce = authRltObj["data"]["nonce"]
    enpass = password_encry(password, nonce)
    data = data.replace("<user_replace>", username)
    data = data.replace("<pass_replace>", enpass)
    print(data)
    re = requests.post(url, data)

    result = json.loads(re.text)
    print(result)
    if result["error_code"] == 0:
        return result["stok"]
    else:
        return 'NULL';

url = "http://192.168.1.38/"

password = "admin123"

if __name__ == '__main__':
    url = "http://192.168.1.38/"
    username = "admin"
    password = "admin123"
    session = getSessionID(url,username,password)
    if session == "NULL":
        print("Login error")
    else:
        print(session)

