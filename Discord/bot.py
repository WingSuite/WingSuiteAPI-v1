import requests
from channels import ChannelMap

#Webhook of my channel. Click on edit channel --> Webhooks --> Creates webhook
channel_map = ChannelMap.channel_map


def send_discord(kwargs: any):
    id = kwargs['unit']
    mUrl = channel_map[id]

    #send message with the content

    data = kwargs
    response = requests.post(mUrl, json=data)

    print(response.status_code)

    print(response.content)
