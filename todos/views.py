from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Task


def task_list(request):
    filter_by = request.GET.get('filter', 'all')

    tasks = Task.objects.all()
    if filter_by == 'active':
        tasks = tasks.filter(completed=False)
    elif filter_by == 'completed':
        tasks = tasks.filter(completed=True)

    total     = Task.objects.count()
    active    = Task.objects.filter(completed=False).count()
    completed = Task.objects.filter(completed=True).count()

    context = {
        'tasks':     tasks,
        'filter_by': filter_by,
        'total':     total,
        'active':    active,
        'completed': completed,
        'today':     timezone.now().date(),
    }
    return render(request, 'todos/task_list.html', context)


def add_task(request):
    if request.method == 'POST':
        title    = request.POST.get('title', '').strip()
        priority = request.POST.get('priority', 'medium')
        due_date = request.POST.get('due_date') or None
        if title:
            Task.objects.create(title=title, priority=priority, due_date=due_date)
    return redirect('task_list')


def toggle_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.completed = not task.completed
    task.save()
    return redirect(request.META.get('HTTP_REFERER', 'task_list'))


def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return redirect(request.META.get('HTTP_REFERER', 'task_list'))


def clear_completed(request):
    if request.method == 'POST':
        Task.objects.filter(completed=True).delete()
    return redirect('task_list')