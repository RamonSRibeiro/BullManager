from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_bois, name='lista_bois'),
    path('novo/', views.criar_boi, name='criar_boi'),
    path('boi/<int:pk>/', views.detalhes_boi, name='detalhes_boi'),
    path('boi/<int:pk>/editar/', views.editar_boi, name='editar_boi'),
    path('boi/<int:pk>/deletar/', views.deletar_boi, name='deletar_boi'),
    path('boi/<int:pk>/coleta/nova/', views.registrar_coleta, name='registrar_coleta'),
    path('boi/<int:pk>/foto/nova/', views.adicionar_foto, name='adicionar_foto'),
    path('boi/<int:pk_boi>/foto/<int:pk_foto>/deletar/', views.deletar_foto, name='deletar_foto'),
    # Adicione junto com as outras rotas do boi
    path('boi/<int:pk>/saida/nova/', views.registrar_saida, name='registrar_saida'),
    path('boi/<int:pk>/relatorio/', views.relatorio_boi, name='relatorio_boi'),
    path('importar/', views.importar_bois, name='importar_bois'),

]