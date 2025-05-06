from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProfileUpdateForm

@login_required
def profile_view(request):
    """Handles the profile update view."""
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')  # Redirect to the same profile page after saving
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    return render(request, 'account/profile.html', {'form': form})
