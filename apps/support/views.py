from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import SupportTicket

@login_required
def ticket_list(request):
    tickets = SupportTicket.objects.select_related('user').order_by('-created_at')
    return render(request, 'support/list.html', {'tickets': tickets})

@login_required
def ticket_detail(request, pk):
    ticket = get_object_or_404(SupportTicket, pk=pk)
    
    if request.method == 'POST':
        admin_response = request.POST.get('admin_response')
        status = request.POST.get('status')
        
        if admin_response:
            ticket.admin_response = admin_response
        if status:
            ticket.status = status
        
        ticket.save()
        messages.success(request, 'Murojaat yangilandi')
        return redirect('support:detail', pk=pk)
    
    return render(request, 'support/detail.html', {'ticket': ticket})

@login_required
def ticket_delete(request, pk):
    ticket = get_object_or_404(SupportTicket, pk=pk)
    ticket.delete()
    messages.success(request, 'Murojaat o\'chirildi')
    return redirect('support:list')
