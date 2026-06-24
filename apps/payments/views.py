from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Payment

@login_required
def payment_list(request):
    payments = Payment.objects.select_related('user', 'subscription').order_by('-created_at')
    return render(request, 'payments/list.html', {'payments': payments})

@csrf_exempt
def click_prepare(request):
    from .click import ClickService
    data = request.POST.dict() if request.method == 'POST' else request.GET.dict()
    result = ClickService.prepare_payment(data)
    return JsonResponse(result)

@csrf_exempt
def click_complete(request):
    from .click import ClickService
    data = request.POST.dict() if request.method == 'POST' else request.GET.dict()
    result = ClickService.complete_payment(data)
    return JsonResponse(result)
