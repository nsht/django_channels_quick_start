import csv
import json

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


import channels.layers
from asgiref.sync import async_to_sync

def index(request):
    return render(request, 'chat/index.html')

@csrf_exempt
def room(request, room_name):
    print(room_name)
    print(request.FILES[room_name])
    csv_file = request.FILES[room_name]
    decoded_file = csv_file.read().decode('utf-8').splitlines()
    reader = csv.DictReader(decoded_file)
    channel_layer = channels.layers.get_channel_layer()
    total = len(decoded_file)
    count = 0
    for row in reader:
        count += 1
        if count % 50 == 0:
            async_to_sync(channel_layer.group_send)(f'chat_{room_name}', {'type': 'chat_message','message':f'Procesed {count} of {total} '})
        print(row)

    async_to_sync(channel_layer.group_send)(f'chat_{room_name}', {'type': 'chat_message','message':'end'})

