from django.contrib import admin
from .models import Portfolio, Holding, Transaction, PortfolioSnapshot

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ['user', 'cash', 'created_at']

@admin.register(Holding)
class HoldingAdmin(admin.ModelAdmin):
    list_display = ['portfolio', 'symbol', 'shares', 'avg_cost']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['portfolio', 'symbol', 'action', 'shares', 'price', 'total', 'realized_pnl', 'timestamp']
    list_filter  = ['action', 'symbol']

@admin.register(PortfolioSnapshot)
class SnapshotAdmin(admin.ModelAdmin):
    list_display = ['portfolio', 'value', 'cash', 'timestamp']
