from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
	email = models.EmailField(unique=True);
	phoneno = models.TextField(default="0000");
	wallet = models.DecimalField(default=0, decimal_places=2, max_digits=20);
	fullName = models.TextField(default="");
	refID = models.IntegerField(default=1);
	walletAddress = models.TextField(default="");
	temp_OTP = models.IntegerField(default=0);

	# pin = models.TextField(default="0000");
	# capital = models.DecimalField(default=0, decimal_places=2, max_digits=20);
	# interest = models.DecimalField(default=0, decimal_places=2, max_digits=20);
	# interest_status = models.BooleanField(default=False); # True for making profit, False for pausing
	# last_investment_trigger_date = models.DateTimeField(auto_now_add=True);

	def __str__(self):
		return self.fullName;

class TradeAccounts(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE);
	account_id = models.IntegerField();
	account_name = models.CharField();
	account_password = models.TextField(default="0000");
	broker = models.CharField();
	brokerNo = models.IntegerField();
	broker_server = models.CharField();
	broker_server_id = models.IntegerField();
	expiration = models.DateTimeField(default=timezone.now);
	subscription = models.DecimalField(default=0,decimal_places=2,max_digits=20);
	
	def __str__(self):
		return self.account_name;

class Withdraws(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE);
	date = models.DateTimeField(auto_now_add=True);

	def __str__(self):
		return self.user.email;