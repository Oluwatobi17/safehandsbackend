from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics
from rest_framework.views import APIView
from django.views.generic.detail import DetailView
from .serializers import UserSerializer, UserAccountSerializer, ReferedListSerializer, ConnectAccountSerializer,ConnectedAccountSerializer;
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import User, TradeAccounts;
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins, viewsets
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from datetime import datetime, date, timedelta
from django.utils import timezone
import decimal
import random;
from .email_utils import send_custom_email
from django.views.generic import View
from rest_framework.decorators import api_view;
from rest_framework.response import Response;

def fetchUserByToken(token):
    tokens = Token.objects.filter(key=token);
    if tokens: return tokens[0].user;
    else: return [];

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

@api_view(['GET'])
def UserDetails(request, pk):
    user = User.objects.get(pk=pk) #fetchUserByToken(request.GET['token']);
    if user:
        serializer = UserAccountSerializer(user);
        return Response(serializer.data);
        
    return Response({'message': 'User does not exist'}, status=400);

@api_view(['PUT'])
def ChangePassword(request, pk):
    user = User.objects.get(pk=pk);
    if user:
        old_password = request.data['password'];
        new_password = request.data['new_password'];
        if user.check_password(old_password):
            user.set_password(new_password);
            user.save();
            return Response({'message': 'Password Changed Successfully'}, status=201);
        return Response({'message': 'Wrong Password'}, status=403);
        
    return Response({'message': 'Invalid Account'}, status=400);

@api_view(['POST'])
def ConnectAccount(request):
    serialized = ConnectAccountSerializer(data=request.data)
    if serialized.is_valid():
        owner = User.objects.get(pk=request.data['user']);
        sub = request.data['subscription'];
        if(owner.wallet<sub):
            return Response({'message': 'Insufficient Balance. Kindly fund your wallet'}, status=status.HTTP_400_BAD_REQUEST)
        
        owner.wallet -= sub;
        owner.save();
        account = TradeAccounts.objects.create(
            user=owner,
            account_id=request.data['account_id'],
            account_name=request.data['account_name'],
            account_password=request.data['account_password'],
            broker=request.data['broker'],
            brokerNo=request.data['brokerNo'],
            broker_server=request.data['broker_server'],
            broker_server_id=request.data['broker_server_id'],
            expiration=datetime.now()-timedelta(days=30),
            subscription=sub
        )
        return Response(serialized.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def ConnectedAccounts(request, pk):
    user = User.objects.get(pk=pk);
    accounts = TradeAccounts.objects.filter(user=user);
    serializer = ConnectedAccountSerializer(accounts, many=True);
    return Response(serializer.data);

@api_view(['GET'])
def GetReferalList(request, pk):
    refered = User.objects.filter(refID=pk);
    serializer = ReferedListSerializer(refered, many=True);
    return Response(serializer.data);

@api_view(['GET'])
def RenewSubscription(request, pk):
    account = get_object_or_404(TradeAccounts, pk=pk);
    user = User.objects.get(pk=account.user.pk);
    
    if(account.subscription>user.wallet):
        return Response({'message': 'Insufficient Balance. Kindly fund your wallet'}, status=status.HTTP_400_BAD_REQUEST)

    user.wallet -= account.subscription;
    now = datetime.now().timestamp();

    if(account.expiration.timestamp()>now):
        account.expiration += timedelta(days=30);
    else:
        account.expiration = datetime.now()+timedelta(days=30);

    user.save();
    account.save();
    return Response({'message': 'Subscription Renewed'}, status=200);

class SendFormEmail(View):
    def get(self, request):
        first_name = request.GET.get('first_name', None)
        last_name = request.GET.get('last_name', None)
        email = request.GET.get('email', None)
        address = request.GET.get('address', None)
        phone = request.GET.get('phone', None)

        data = " First Name: "+first_name+"\n Last Name: "+last_name+"\n Email: "+email+"\n Address: "+address+"\n Phone: "+phone;
        # """.format(first_name,last_name,email,address,phone);

        # print(data);
        subject = 'New Application'
        message = data;
        recipient_list = ['ganiuibrahim3000@gmail.com']  # Replace with the recipient's email addresses

        send_custom_email(subject, message, recipient_list)

    def get_queryset(self):
        user = self.request.user
        user = get_object_or_404(User,pk=self.kwargs["pk"])
        if(user.interest>0):
            user.capital = user.capital + user.interest;
            user.interest = 0;
            user.last_investment_trigger_date = timezone.now()
            user.save();
        return User.objects.all()
    
class GenerateOTP(APIView):
    # serializer_class = UserDetailsSerializer
    # permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        # user = self.request.user
        user = User.objects.get(pk=pk);
        otp = random.randint(99999,999999);
        user.temp_OTP = otp;
        user.save();
        
        data = "Your OTP is "+str(otp)+"\nKindly ignore if you didn't request for this";
        # print(data);
        subject = 'OTP From Safecapital'
        message = data; #
        recipient_list = [user.email]  # Replace with the recipient's email addresses

        send_custom_email(subject, message, recipient_list);

        return Response({'success': 'OTP Generated and sent'}, status=200)
        # return HttpResponse("OTP Generated and sent");

class WalletUpdate(generics.GenericAPIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        otp = int(request.data['otp']);
        wallet = request.data['wallet'];

        obj = get_object_or_404(User, pk=pk)
        if obj.temp_OTP!=otp and otp!=0:
            return Response({'error': 'Invalid OTP'}, status=400)

        
        obj.walletAddress = wallet;
        obj.temp_OTP = 0;
        obj.save();
        return Response({'success': 'Wallet Updated Successfully'}, status=200)

# def my_email_view(request):
#     # ... Your view logic ...
#     print("Job application received ", request.POST['email']);
#     return HttpResponse("Normal Email Send Successfully!")

    # subject = 'New Application'
    # message = 'This is a test email sent from Django.'
    # recipient_list = ['ganiuibrahim3000@gmail.com']  # Replace with the recipient's email addresses

    # send_custom_email(subject, message, recipient_list)

    # # ... Rest of your view logic ...
    # return HttpResponse("Normal Email Send Successfully!")