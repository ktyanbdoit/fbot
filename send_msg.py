import requests


def send(phone, msg, intid):

    url = 'http://10.79.4.34:88/'
    sendata = {'phone': phone, 'msg': msg, 'intid': intid, 'sender': 'Facebook'}

    #r = requests.get(url, params={"msg":"tes sdf sdf sdf"})
    #r = requests.get(url)
    r = requests.post(url, json=sendata)
    #r = requests.post('http://92.46.43.50/', json={'test': 'cheers'})
    print("SENDING_!!")
    print(r)