from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import CustomUserCreationForm, MessageForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Message
from .serializers import MessageSerializer
from .encryption_utils import encrypt_message, decrypt_message
from django.http import JsonResponse
from cryptography.fernet import InvalidToken
from django.contrib.auth import get_user_model


User = get_user_model()  # Use the custom user model

def view_user_messages(request, user_id):
    user = get_object_or_404(User, id=user_id)
    messages = Message.objects.filter(sender=user) | Message.objects.filter(receiver=user)

    # Decrypt the message content before displaying it
    for message in messages:
        message.content = message.get_decrypted_content()

    return render(request, 'messaging/view_user_messages.html', {'user': user, 'messages': messages})

def home(request):
    return render(request, 'messaging/home.html') 

def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('admin_dashboard')

# Admin Dashboard View
@login_required
def admin_dashboard(request):
    if not request.user.is_staff:  # Restrict non-admin users
        messages.error(request, "Access denied. Admin privileges are required.")
        return redirect('admin_login')
    
    users = User.objects.all()
    messages = Message.objects.all()

    # Decrypt the message content if needed
    for message in messages:
        message.content = message.get_decrypted_content()

    return render(request, "messaging/dashboard.html", {
        'users': users,
        'messages': messages
    })

# Admin Login View
def admin_login(request):
    if request.user.is_authenticated:  # Redirect if already logged in
        if request.user.is_staff:  # Ensure only admin users can access
            return redirect('admin_dashboard')
        else:
            logout(request)  # Force logout for non-admin users
            messages.error(request, "Invalid username or password.")
            return redirect('admin_login')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_staff:  # Allow only admin users to log in
                login(request, user)
                messages.success(request, "Logged in successfully.")
                return redirect('admin_dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'messaging/login.html', {'form': form})

# Admin Logout View
def admin_logout(request):
    logout(request)
    return redirect('admin_login')

# Send Message View
@login_required
def send_message(request, user_id=None):
    if request.method == 'POST':
        content = request.POST.get('content')

        try:
            receiver = get_object_or_404(User, id=user_id)
        except User.DoesNotExist:
            return render(request, 'messaging/send_message.html', {'error': 'User not found'})

        # Create and save the message (content encrypted automatically by middleware)
        message = Message(sender=request.user, receiver=receiver, content=content)
        message.save()

        return redirect('admin_dashboard')  # Redirect after sending the message

    # Preload the receiver's info if user_id is provided
    receiver = get_object_or_404(User, id=user_id) if user_id else None
    return render(request, 'messaging/send_message.html', {'receiver': receiver})

# Message List View
def message_list(request):
    messages = Message.objects.all()
    return JsonResponse({'messages': [message.to_dict() for message in messages]})

class MessageListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Fetch the latest messages for the current user
        messages = Message.objects.filter(receiver=request.user)
        
        # Decrypt the message content (if needed)
        for message in messages:
            message.content = message.get_decrypted_content()

        # Serialize the messages
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

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

# Secure API Endpoint for Receiving Messages (User)
class ReceiveMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        messages = Message.objects.filter(receiver=request.user)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
