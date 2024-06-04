import requests
import random

def notify(msg):
    token = 'BlPiiCU5EMuvoxd6EnbEtFjSxwUfywHxIblwnCYMavu'
    url = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization' : 'Bearer ' + token}
    sticker = ['1988', '1989', '1991', '1992', '1994', '1998', '2001', '2003', '1993', '1996', '1997']
    data = {
            'message': msg,
            'stickerPackageId' : '446',
            'stickerId' : random.choice(sticker)}
    requests.post(url, headers=headers, data=data)



    






