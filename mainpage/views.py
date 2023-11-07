from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .kafka_producer import send_kafka_message
import socket, random, platform, os

kafka_message_count = 0
pod_name = os.getenv('POD_NAME', socket.gethostname())

def index(request):
    global kafka_message_count, pod_name

    context = {'pod_name': pod_name, 
               'kafka_message_count': kafka_message_count}

    return render(request, 'index.html', context)

def send(request):
    global kafka_message_count, pod_name

    message = f"Hello from Pod: {pod_name}, Message Count: {kafka_message_count}"
    send_kafka_message(message)

    kafka_message_count += 1  # 카운트 증가

    return redirect('index')

def reset(request):
    global kafka_message_count
    kafka_message_count = 0  # 카운트 초기화

    return redirect('index')

def random_menu(request):
    global kafka_message_count, pod_name

    # 무작위 아이템 선택
    sample_list = ['Nike', 'Adidas', 'Newbalance', 'Salomon', 'Jordan', 'Converse']
    random_element = random.choice(sample_list)
    random_number = random.randint(1, 10)

    message = f"Random Element from Pod: {pod_name}, Element: {random_element}, Number: {random_number}, Message Count: {kafka_message_count}"
    send_kafka_message(message)
    kafka_message_count += 1

    return redirect('index')  # 기존 페이지로 리다이렉트

def send_os_info(request):
    global kafka_message_count, pod_name
    # 현재 OS 정보 가져오기
    os_info = platform.system()

    message = f"OS Info from Pod: {pod_name}, OS: {os_info}, Message Count: {kafka_message_count}"
    send_kafka_message(message)
    kafka_message_count += 1

    return redirect('index')  # 기존 페이지로 리다이렉트

def k_menu(request):
    global kafka_message_count, pod_name
    sample_list = ['Nike', 'Adidas', 'Newbalance', 'Salomon', 'Jordan', 'Converse']

    # 무작위 아이템과 수량을 선택하고 메시지 전달
    for _ in range(1000):
        random_element = random.choice(sample_list)
        random_number = random.randint(1, 10)

        message = f"Random Element from Pod: {pod_name}, Element: {random_element}, Number: {random_number}, Message Count: {kafka_message_count}"
        send_kafka_message(message)
        kafka_message_count += 1

    return redirect('index')  # 기존 페이지로 리다이렉트
