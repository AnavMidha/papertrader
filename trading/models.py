from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Portfolio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='portfolio')
    cash = models.DecimalField(max_digits=15, decimal_places=2, default=1000000.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Portfolio"

    @property
    def holdings_value(self):
        return sum(h.current_value for h in self.holdings.all())

    @property
    def total_value(self):
        return float(self.cash) + self.holdings_value

    @property
    def total_pnl(self):
        return self.total_value - 1000000.00

    @property
    def total_return_pct(self):
        return (self.total_pnl / 1000000.00) * 100


class Holding(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='holdings')
    symbol = models.CharField(max_length=10)
    shares = models.DecimalField(max_digits=12, decimal_places=4)
    avg_cost = models.DecimalField(max_digits=12, decimal_places=4)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('portfolio', 'symbol')

    def __str__(self):
        return f"{self.portfolio.user.username} - {self.symbol} x{self.shares}"

    @property
    def cost_basis(self):
        return float(self.shares) * float(self.avg_cost)

    # current_price is set dynamically (not stored)
    @property
    def current_value(self):
        return getattr(self, '_current_value', self.cost_basis)

    def set_current_price(self, price):
        self._current_price = price
        self._current_value = float(self.shares) * price

    @property
    def unrealized_pnl(self):
        price = getattr(self, '_current_price', float(self.avg_cost))
        return (price - float(self.avg_cost)) * float(self.shares)

    @property
    def unrealized_pnl_pct(self):
        if float(self.avg_cost) == 0:
            return 0
        price = getattr(self, '_current_price', float(self.avg_cost))
        return ((price - float(self.avg_cost)) / float(self.avg_cost)) * 100


class Transaction(models.Model):
    BUY = 'buy'
    SELL = 'sell'
    ACTION_CHOICES = [(BUY, 'Buy'), (SELL, 'Sell')]

    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='transactions')
    symbol = models.CharField(max_length=10)
    action = models.CharField(max_length=4, choices=ACTION_CHOICES)
    shares = models.DecimalField(max_digits=12, decimal_places=4)
    price = models.DecimalField(max_digits=12, decimal_places=4)
    total = models.DecimalField(max_digits=15, decimal_places=2)
    realized_pnl = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.action.upper()} {self.shares} {self.symbol} @ {self.price}"


class PortfolioSnapshot(models.Model):
    """Daily portfolio value snapshots for the growth chart."""
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='snapshots')
    value = models.DecimalField(max_digits=15, decimal_places=2)
    cash = models.DecimalField(max_digits=15, decimal_places=2)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.portfolio.user.username} snapshot @ {self.timestamp}: ${self.value}"
