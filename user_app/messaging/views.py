from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import Message
from .forms import MessageForm, CustomUserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import MessageSerializer

User = get_user_model()  # Use the custom user model

# Home View
def home(request):
    return render(request, 'messaging/home.html')

# User Registration View
def user_register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)  # Use CustomUserCreationForm here
        if form.is_valid():
            form.save()
            return redirect('user_login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'messaging/register.html', {'form': form})

# User Login View
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('user_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'messaging/login.html', {'form': form})

# User Logout View
def user_logout(request):
    logout(request)
    return redirect('user_login')

# User Dashboard View
@login_required
def user_dashboard(request):
    sent_messages = Message.objects.filter(sender=request.user).values('receiver')
    received_messages = Message.objects.filter(receiver=request.user).values('sender')

    sent_user_ids = {message['receiver'] for message in sent_messages}
    received_user_ids = {message['sender'] for message in received_messages}

    communicated_user_ids = sent_user_ids | received_user_ids
    communicated_users = User.objects.filter(id__in=communicated_user_ids)

    messages = Message.objects.filter(sender=request.user) | Message.objects.filter(receiver=request.user)
    for message in messages:
        message.content = message.get_decrypted_content()

    return render(request, "messaging/dashboard.html", {
        "users": communicated_users,
        "messages": messages
    })

# Send Message View
@login_required
def send_message(request, user_id=None):
    if user_id:
        receiver = get_object_or_404(User, id=user_id)
        messages = Message.objects.filter(sender=request.user, receiver=receiver) | Message.objects.filter(sender=receiver, receiver=request.user)
        messages = messages.order_by('-timestamp')

        for message in messages:
            message.content = message.get_decrypted_content()

        if request.method == 'POST':
            content = request.POST.get('content')
            if content:
                Message.objects.create(sender=request.user, receiver=receiver, content=content)
                return redirect('send_message_with_user', user_id=user_id)

        return render(request, 'messaging/send_message_with_user.html', {'receiver': receiver, 'messages': messages})

    if request.method == 'POST':
        receiver_username = request.POST.get('receiver')
        content = request.POST.get('content')
        try:
            receiver = User.objects.get(username=receiver_username)
            Message.objects.create(sender=request.user, receiver=receiver, content=content)
            return redirect('user_dashboard')
        except User.DoesNotExist:
            return render(request, 'messaging/send_message.html', {'error': 'User not found'})

    return render(request, 'messaging/send_message.html')

# Send Letter to Santa View
@login_required
def send_message_to_santa(request):
    try:
        receiver = User.objects.get(username="admin")  # Ensure 'admin' exists
        if request.method == 'POST':
            content = request.POST.get('content')
            if content:
                Message.objects.create(sender=request.user, receiver=receiver, content=content)
                messages.success(request, 'Your letter to Santa has been sent!')
                return redirect('send_message_to_santa')  # Redirect to prevent duplicate submissions
    except User.DoesNotExist:
        messages.error(request, "Santa (admin) does not exist.")
        return redirect('user_dashboard')

    return render(request, 'messaging/send_message.html')


# Secure API Endpoint for Sending Messages
class SendMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save(sender=request.user)
            return Response({'message': 'Message sent securely'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Secure API Endpoint for Receiving Messages
class ReceiveMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        messages = Message.objects.filter(receiver=request.user)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
