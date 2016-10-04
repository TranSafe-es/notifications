from django.conf.urls import url
from .views import TransactionDetails, TransactionHistory, CreateTransaction, UpdateTransactionState

urlpatterns = [
               url(r'^email/$', TransactionDetails.as_view(), name="Show details"),
               url(r'^messenger/$', TransactionHistory.as_view(), name="Transactions history"),
               url(r'^sms/$', CreateTransaction.as_view(), name="Create transaction"),
]
