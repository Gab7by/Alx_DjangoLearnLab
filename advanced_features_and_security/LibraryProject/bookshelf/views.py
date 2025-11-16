from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from .models import books   # <-- replace Item with your actual model
from .forms import ExampleForm

# ================================
# VIEW ITEMS
# ================================
@permission_required('your_app.can_view', raise_exception=True)
def book_list(request):
    books = Item.objects.all()
    return render(request, 'your_app/item_list.html', {'items': items})


# ================================
# CREATE ITEM
# ================================
@permission_required('your_app.can_create', raise_exception=True)
def item_create(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():  # ensures input validation
            form.save()
            return redirect('item_list')
    else:
        form = ItemForm()
   return render(request, 'your_app/item_form.html', {'form': form})

# ================================
# EDIT ITEM
# ================================
@permission_required('your_app.can_edit', raise_exception=True)
def item_edit(request, pk):
    item = get_object_or_404(Item, pk=pk)

    if request.method == 'POST':
        item.name = request.POST.get('name')
        item.save()
        return redirect('item_list')

    return render(request, 'your_app/item_edit.html', {'item': item})


# ================================
# DELETE ITEM
# ================================
@permission_required('your_app.can_delete', raise_exception=True)
def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk)
    item.delete()
    return redirect('item_list')