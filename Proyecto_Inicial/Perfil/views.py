
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import ProfileForm

@login_required
def mi_perfil(request):
    return render(request, 'perfil/mi_perfil.html')


@login_required
def edit_profile(request):
    profile = request.user.profile

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("mi_perfil")

    else:
        form = ProfileForm(instance=profile)

    return render(request, "profile/edit_perfil.html", {"form": form})
