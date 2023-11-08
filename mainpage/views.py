from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .kafka_producer import send_kafka_message
import socket, random, os, uuid

pod_name = os.getenv('POD_NAME', socket.gethostname())
pod_ip = os.getenv('POD_IP',socket.gethostbyname(pod_name))

info_topic = os.getenv('INFO_TOPIC', 'quickstart-events')
shop_topic = os.getenv('SHOP_TOPIC', 'quickstart-events')

item_list = ['Nike', 'Adidas', 'Newbalance', 'Salomon', 'Jordan', 'Converse']
name_list = ['Kim', 'Lee', 'Park', 'Jo', 'Hong']

def index(request):
    global pod_name
    
    context = {'pod_name': pod_name}

    return render(request, 'index.html', context)

def send_info(request):
    global pod_name, pod_ip

    message = f"Pod Name: {pod_name}, Pod IP: {pod_ip}"

    send_kafka_message(message, info_topic)

    return redirect('index')

def random_menu(request):
    global pod_name

    random_item = random.choice(item_list)
    random_name = random.choice(name_list)
    random_number = random.randint(1, 10)
    userid = uuid.uuid4()

    message = f"Pod Name: {pod_name}, Name: {random_name}, Item: {random_item}, Number: {random_number}, UUID: {userid}"
    
    send_kafka_message(message, shop_topic)

    return redirect('index')  # 기존 페이지로 리다이렉트

def k_menu(request):
    global pod_name

    # 무작위 아이템과 수량을 선택하고 메시지 전달
    for _ in range(1000):
        random_item = random.choice(item_list)
        random_name = random.choice(name_list)
        random_number = random.randint(1, 10)
        userid = uuid.uuid4()

        message = f"Pod Name: {pod_name}, Name: {random_name}, Item: {random_item}, Number: {random_number}, UUID: {userid}"
        
        send_kafka_message(message, shop_topic)

    return redirect('index')  # 기존 페이지로 리다이렉트