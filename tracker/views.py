import csv
from collections import defaultdict
from datetime import date, timedelta
from decimal import Decimal
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import TxnForm
from .models import Transaction, Budget, ADD, SUB

def month_start(s):
    try:
        y, m = map(int, (s or "").split("-")); return date(y, m, 1)
    except ValueError:
        return date.today().replace(day=1)

def next_month(d):
    return date(d.year + (d.month == 12), d.month % 12 + 1, 1)

def total(qs, *types):
    return qs.filter(type__in=types).aggregate(s=Sum("amount"))["s"] or Decimal(0)

def balance(qs):
    return total(qs, *ADD) - total(qs, *SUB)

@login_required
def dashboard(request):
    start = month_start(request.GET.get("month")); end = next_month(start)
    allq = Transaction.objects.filter(user=request.user)
    mq = allq.filter(date__gte=start, date__lt=end)
    opening = balance(allq.filter(date__lt=start))
    spent = total(mq, "EXPENSE")
    cats = defaultdict(Decimal)
    for t in mq.filter(type="EXPENSE"):
        cats[t.category or "Other"] += t.amount
    cats = sorted(((c, a, int(a * 100 / spent) if spent else 0) for c, a in cats.items()), key=lambda x: -x[1])
    owed = defaultdict(Decimal)
    for t in allq.filter(type__in=["LENT", "REPAID"]):
        owed[t.person or "Unknown"] += t.amount if t.type == "LENT" else -t.amount
    owed = {p: a for p, a in owed.items() if a > 0}
    b = Budget.objects.filter(user=request.user, month=start).first()
    ctx = dict(month=start, prev=(start - timedelta(days=1)).replace(day=1), next=end,
        opening=opening, income=total(mq, *ADD), spent=spent, lent=total(mq, "LENT"),
        saved=total(mq, "SAVING"), closing=opening + balance(mq), total_saved=total(allq, "SAVING"),
        cats=cats, owed=owed, budget=b,
        budget_pct=min(int(spent * 100 / b.amount), 100) if b and b.amount else 0, recent=mq[:10])
    return render(request, "tracker/dashboard.html", ctx)

@login_required
def add(request):
    form = TxnForm(request.POST or None)
    if form.is_valid():
        t = form.save(commit=False); t.user = request.user; t.save()
        return redirect("history")
    return render(request, "tracker/form.html", {"form": form, "title": "Nayi entry"})

@login_required
def edit(request, pk):
    t = get_object_or_404(Transaction, pk=pk, user=request.user)
    form = TxnForm(request.POST or None, instance=t)
    if form.is_valid():
        form.save(); return redirect("history")
    return render(request, "tracker/form.html", {"form": form, "title": "Entry edit karo"})

@login_required
def delete(request, pk):
    t = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == "POST":
        t.delete(); return redirect("history")
    return render(request, "tracker/confirm.html", {"t": t})

def filtered(request):
    qs = Transaction.objects.filter(user=request.user); g = request.GET
    if g.get("type"): qs = qs.filter(type=g["type"])
    if g.get("person"): qs = qs.filter(person__icontains=g["person"])
    if g.get("category"): qs = qs.filter(category__icontains=g["category"])
    if g.get("from"): qs = qs.filter(date__gte=g["from"])
    if g.get("to"): qs = qs.filter(date__lte=g["to"])
    return qs

@login_required
def history(request):
    qs = filtered(request)
    return render(request, "tracker/history.html", {"txns": qs, "net": balance(qs), "q": request.GET,
        "query": request.GET.urlencode()})

@login_required
def export(request):
    r = HttpResponse(content_type="text/csv"); r["Content-Disposition"] = 'attachment; filename="history.csv"'
    w = csv.writer(r); w.writerow(["Date", "Type", "Amount", "Category", "Person", "Note"])
    for t in filtered(request):
        w.writerow([t.date, t.type, t.amount, t.category, t.person, t.note])
    return r

@login_required
def set_budget(request):
    if request.method == "POST":
        m = month_start(request.POST.get("month"))
        Budget.objects.update_or_create(user=request.user, month=m, defaults={"amount": request.POST["amount"]})
        return redirect(f"/?month={m:%Y-%m}")
    return redirect("dashboard")

def register(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        login(request, form.save()); return redirect("dashboard")
    return render(request, "registration/register.html", {"form": form})
