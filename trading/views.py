import json
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .finnhub import DEFAULT_WATCHLIST, get_quote, get_quotes, search_symbol
from .models import Holding, Portfolio, PortfolioSnapshot, Transaction


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    error = ''
    if request.method == 'POST':
        action = request.POST.get('action')
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        if action == 'register':
            email = request.POST.get('email', '').strip()
            if User.objects.filter(username=username).exists():
                error = 'Username already taken.'
            elif len(password) < 6:
                error = 'Password must be at least 6 characters.'
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                portfolio = Portfolio.objects.create(user=user)
                PortfolioSnapshot.objects.create(portfolio=portfolio, value=Decimal('1000000.00'), cash=Decimal('1000000.00'))
                login(request, user)
                return redirect('dashboard')

        elif action == 'login':
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                portfolio, created = Portfolio.objects.get_or_create(user=user)
                if created:
                    PortfolioSnapshot.objects.create(portfolio=portfolio, value=Decimal('1000000.00'), cash=Decimal('1000000.00'))
                return redirect('dashboard')
            else:
                error = 'Invalid username or password.'

    return render(request, 'trading/login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    portfolio = get_object_or_404(Portfolio, user=request.user)
    holdings = list(portfolio.holdings.all())
    watchlist = list(DEFAULT_WATCHLIST)

    symbols_needed = list({h.symbol for h in holdings} | set(watchlist))
    prices = get_quotes(symbols_needed)

    for h in holdings:
        price = prices.get(h.symbol, float(h.avg_cost))
        h.set_current_price(price)

    holdings_value = sum(h.current_value for h in holdings)
    total_value = float(portfolio.cash) + holdings_value
    total_pnl = total_value - 1000000.0
    total_return_pct = (total_pnl / 1000000.0) * 100

    last_snap = portfolio.snapshots.last()
    now = timezone.now()
    if not last_snap or (now - last_snap.timestamp).total_seconds() > 300:
        PortfolioSnapshot.objects.create(
            portfolio=portfolio,
            value=Decimal(str(round(total_value, 2))),
            cash=portfolio.cash,
        )

    snapshots = list(portfolio.snapshots.order_by('timestamp')[:100])
    chart_labels = [s.timestamp.strftime('%b %d %H:%M') for s in snapshots]
    chart_values = [float(s.value) for s in snapshots]

    recent_txns = portfolio.transactions.all()[:10]

    watchlist_data = [
        {'symbol': s, 'price': prices.get(s)}
        for s in watchlist
    ]

    context = {
        'portfolio': portfolio,
        'holdings': holdings,
        'holdings_value': holdings_value,
        'total_value': total_value,
        'total_pnl': total_pnl,
        'total_return_pct': total_return_pct,
        'watchlist_data': watchlist_data,
        'recent_txns': recent_txns,
        'chart_labels': json.dumps(chart_labels),
        'chart_values': json.dumps(chart_values),
        'prices': prices,
    }
    return render(request, 'trading/dashboard.html', context)


@login_required
@require_POST
def trade(request):
    portfolio = get_object_or_404(Portfolio, user=request.user)
    symbol = request.POST.get('symbol', '').strip().upper()
    action = request.POST.get('action', '').lower()
    try:
        qty = Decimal(request.POST.get('qty', '0'))
    except Exception:
        messages.error(request, 'Invalid quantity.')
        return redirect('dashboard')

    if not symbol or qty <= 0 or action not in ('buy', 'sell'):
        messages.error(request, 'Invalid trade parameters.')
        return redirect('dashboard')

    quote = get_quote(symbol)
    if not quote:
        messages.error(request, f'Could not fetch price for {symbol}.')
        return redirect('dashboard')

    price = Decimal(str(quote['c']))
    total = price * qty

    if action == 'buy':
        if total > portfolio.cash:
            messages.error(request, f'Insufficient funds. Need ₹{total:.2f}, have ₹{portfolio.cash:.2f}.')
            return redirect('dashboard')
        portfolio.cash -= total
        holding, created = Holding.objects.get_or_create(
            portfolio=portfolio, symbol=symbol,
            defaults={'shares': Decimal('0'), 'avg_cost': price}
        )
        if not created:
            prev_total = holding.shares * holding.avg_cost
            holding.shares += qty
            holding.avg_cost = (prev_total + total) / holding.shares
        else:
            holding.shares = qty
            holding.avg_cost = price
        holding.save()
        portfolio.save()
        Transaction.objects.create(portfolio=portfolio, symbol=symbol, action='buy', shares=qty, price=price, total=total)
        messages.success(request, f'Bought {qty} {symbol} @ ₹{price:.2f}')

    elif action == 'sell':
        try:
            holding = Holding.objects.get(portfolio=portfolio, symbol=symbol)
        except Holding.DoesNotExist:
            messages.error(request, f"You don't hold any {symbol}.")
            return redirect('dashboard')
        if qty > holding.shares:
            messages.error(request, f'You only have {holding.shares} shares of {symbol}.')
            return redirect('dashboard')
        realized_pnl = (price - holding.avg_cost) * qty
        portfolio.cash += total
        holding.shares -= qty
        if holding.shares == 0:
            holding.delete()
        else:
            holding.save()
        portfolio.save()
        Transaction.objects.create(portfolio=portfolio, symbol=symbol, action='sell', shares=qty, price=price, total=total, realized_pnl=realized_pnl)
        messages.success(request, f'Sold {qty} {symbol} @ ₹{price:.2f} · P&L: {"+" if realized_pnl >= 0 else ""}₹{realized_pnl:.2f}')

    return redirect('dashboard')


@login_required
def history(request):
    portfolio = get_object_or_404(Portfolio, user=request.user)
    transactions = portfolio.transactions.all()

    symbol_filter = request.GET.get('symbol', '').strip().upper()
    action_filter = request.GET.get('action', '').strip().lower()
    if symbol_filter:
        transactions = transactions.filter(symbol=symbol_filter)
    if action_filter in ('buy', 'sell'):
        transactions = transactions.filter(action=action_filter)

    total_realized = sum(
        float(t.realized_pnl) for t in portfolio.transactions.filter(action='sell')
        if t.realized_pnl is not None
    )

    context = {
        'transactions': transactions,
        'symbol_filter': symbol_filter,
        'action_filter': action_filter,
        'total_realized': total_realized,
        'portfolio': portfolio,
    }
    return render(request, 'trading/history.html', context)


@login_required
def api_quote(request):
    symbol = request.GET.get('symbol', '').strip().upper()
    if not symbol:
        return JsonResponse({'error': 'No symbol'}, status=400)
    quote = get_quote(symbol)
    if not quote:
        return JsonResponse({'error': f'Symbol {symbol} not found'}, status=404)
    return JsonResponse({'symbol': symbol, 'price': quote['c']})


@login_required
def api_search(request):
    query = request.GET.get('q', '').strip()
    if not query:
        return JsonResponse({'results': []})
    results = search_symbol(query)
    return JsonResponse({'results': results})


@login_required
def api_portfolio_chart(request):
    portfolio = get_object_or_404(Portfolio, user=request.user)
    snapshots = list(portfolio.snapshots.order_by('timestamp'))
    data = {
        'labels': [s.timestamp.strftime('%b %d %H:%M') for s in snapshots],
        'values': [float(s.value) for s in snapshots],
    }
    return JsonResponse(data)
