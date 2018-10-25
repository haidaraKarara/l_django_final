from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    #url(r'^connexion$', views.Login.as_view(), name='connexion'),
    url(r'^$',views.liste,name="url_liste"),
    #url(r'^nouveau',views.nouveau,name="url_nouveau"),
    url(r'^nouveau$', views.URLCreate.as_view(), name='url_nouveau'),
    url(r'^edition/(?P<code>\w{6,})$', views.URLUpdate.as_view(), name='url_update'),
    url(r'^supprimer/(?P<code>\w{6,})$', views.URLDelete.as_view(), name='url_delete'),
    url(r'^(?P<code>\w{6,})/$',views.redirection,name="url_redirection"),
    url(r'^deconnexion',auth_views.logout_then_login,name='deconnexion'),
    url(r'^changer_mdp$',views.ChangeMdp.as_view(),name='changer_mdp'),
    #url(r'^deconnexion$', views.deconnexion, name='deconnexion'),
    url(r'^connexion$', auth_views.login,{'template_name':'mini_url_app/connexion.html'},name="connexion"), 
    # internationalisation
    url(r'^test-i18n$',views.test_i18n,name='i18n')
]

