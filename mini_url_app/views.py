
from django.shortcuts import redirect,get_object_or_404,render

from .models import MiniURL
from .forms import MiniURLForm,ConnexionForm
from django.urls import reverse_lazy

from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.cache import cache_page
from django.utils.translation import ugettext as _
from django.utils.translation import ungettext

CRITICAL = 50


# Create your views here.
#@login_required
#@cache_page(3 * 60)
def liste(request):
    """Affichage de la
        liste de redirections"""
    minis = MiniURL.objects.order_by('-nb_acces')
    return render(request,'mini_url_app/liste.html',locals())
    

# def nouveau(request):
#     """Ajout d'une redirection"""
#     if request.method == "POST":
#         form = MiniURLForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect(liste)
#     else:
#         form = MiniURLForm()
#     return render(request,'mini_url_app/nouveau.html',{'form':form})
# substitution 
class URLCreate(LoginRequiredMixin,CreateView):
    login_url = 'connexion'  # if user is not authenticated, he is redirect here
    model = MiniURL
    template_name = 'mini_url_app/nouveau.html'
    form_class = MiniURLForm
    success_url = reverse_lazy('url_liste')

    def form_valid(self, form):
        self.object = form.save()
        # Envoi d'un message à l'utilisateur
        messages.add_message(self.request, messages.SUCCESS, 'Url créér avec succès !')
        return redirect(self.get_success_url())

class URLUpdate(UpdateView):
    model = MiniURL
    template_name = 'mini_url_app/update.html'
    form_class = MiniURLForm
    success_url = reverse_lazy('url_liste')

    def get_object(self, queryset=None):
        code = self.kwargs.get('code', None)
        return get_object_or_404(MiniURL, code=code)

    def form_valid(self, form):
        self.object = form.save()
        # Envoi d'un message à l'utilisateur
        messages.success(self.request,"L'URL  {} a été mise à jour avecc succès !".format(self.object))
        #messages.add_message(self.request, messages.SUCCESS, 'Url mis à jour.')
        return redirect(self.get_success_url())

class URLDelete(DeleteView):
    model = MiniURL
    context_object_name = "mini_url"
    template_name = 'mini_url_app/supprimer.html'
    success_url = reverse_lazy('url_liste')

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        global CRITICAL
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(self.request,"L'URL {} a été bien supprimée".format(self.object))
        messages.add_message(self.request, CRITICAL, 'Vous venez de faire une erreur monumentale.', extra_tags="fail")
        return redirect(success_url)

    def get_object(self, queryset=None):
        code = self.kwargs.get('code', None)
        return get_object_or_404(MiniURL, code=code)

def redirection(request,code):
    """Redirection vers l'url enregistrée """
    mini = get_object_or_404(MiniURL,code=code)
    mini.nb_acces +=1
    mini.save()
    return redirect(mini.url,permanent=True)

class ChangeMdp(PasswordChangeView):
    template_name = 'mini_url_app/changer_mdp.html'
    form_class = MiniURLForm


def connexion(request):
    error = False

    if request.method == "POST":
        form = ConnexionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)  # Nous vérifions si les données sont correctes
            if user:  # Si l'objet renvoyé n'est pas None
                login(request, user)  # nous connectons l'utilisateur
                return redirect('url_liste')
            else: # sinon une erreur sera affichée
                error = True
    else:
        form = ConnexionForm()

    return render(request, 'mini_url_app/connexion.html', locals())

def deconnexion(request):
    logout(request)
    return redirect('connexion')

class Login(LoginView):
    form_class = 'ConnexionForm'
    template_name = 'mini_url_app/connexion.html'

# internationalisation
def test_i18n(request):
    nb_chats = 1
    couleur = "blanc"
    chaine = _("J'ai un %(animal)s %(col)s.") % {'animal': 'chat', 'col':couleur}
    ip = _("Votre IP est %s") % request.META['REMOTE_ADDR']
    infos = ungettext(
        "… et selon mes informations, vous avez %(nb)s chat %(col)s !",
        "… et selon mes informations, vous avez %(nb)s chats %(col)ss !",
        nb_chats) % {'nb':nb_chats, 'col':couleur}

    return render(request, 'mini_url_app/test_i18n.html', locals())


# def liste(request,page=1):
#     """Affichage de la
#         liste de redirections"""
#     minis_list = MiniURL.objects.order_by('-nb_acces')
#     paginator = Paginator(minis_list,5) # 5 liens par page
    
#     try:
#         # La définition de nos URL autorise comme argument « page » uniquement 
#         # des entiers, nous n'avons pas à nous soucier de PageNotAnInteger
#         minis = paginator.page(page)
#     except EmptyPage:
#          # Nous vérifions toutefois que nous ne dépassons pas la limite de page
#         # Par convention, nous renvoyons la dernière page dans ce cas
#         minis = paginator.page(paginator.num_pages)
#     return render(request,'mini_url_app/liste.html',locals())
