from django.urls import path

from . import views

urlpatterns = [
    path('telefone/', views.TelefoneList.as_view()),
    path('telefone/delete/<int:pk>', views.TelefoneDelete.as_view()),
    path('telefone/update/<int:pk>', views.TelefoneUpdate.as_view()),
    path('telefone/list/<int:pk>', views.TelefoneListarId.as_view()),

    path('autor/', views.AutorList.as_view()),
    path('autor/delete/<int:pk>', views.AutorDelete.as_view()),
    path('autor/update/<int:pk>', views.AutorUpdate.as_view()),
    path('autor/list/<int:pk>', views.AutorListarId.as_view()),

    path('avaliador/', views.AvaliadorList.as_view()),
    path('avaliador/delete/<int:pk>', views.AvaliadorDelete.as_view()),
    path('avaliador/update/<int:pk>', views.AvaliadorUpdate.as_view()),
    path('avaliador/list/<int:pk>', views.AvaliadorListarId.as_view()),

    path('avaliacao/', views.AvaliacaoList.as_view()),
    path('avaliacao/delete/<int:pk>', views.AvaliacaoDelete.as_view()),
    path('avaliacao/update/<int:pk>', views.AvaliacaoUpdate.as_view()),
    path('avaliacao/list/<int:pk>', views.AvaliacaoListarId.as_view()),

    path('projeto/', views.ProjetoList.as_view()),
    path('projeto/delete/<int:pk>', views.ProjetoDelete.as_view()),
    path('projeto/update/<int:pk>', views.ProjetoUpdate.as_view()),
    path('projeto/list/<int:pk>', views.ProjetoListarId.as_view()),

    path('cronograma/', views.CronogramaList.as_view()),
    path('cronograma/delete/<int:pk>', views.CronogramaDelete.as_view()),
    path('cronograma/update/<int:pk>', views.CronogramaUpdate.as_view()),
    path('cronograma/list/<int:pk>', views.CronogramaListarId.as_view()),

    path('premio/', views.PremioList.as_view()),
    path('premio/delete/<int:pk>', views.PremioDelete.as_view()),
    path('premio/update/<int:pk>', views.PremioUpdate.as_view()),
    path('premio/list/<int:pk>', views.PremioListarId.as_view()),

    # Consulta Solicitadas
    path('listar_autores_projetos/', views.listarProjetosEAutores.as_view()),
    path('autor_projetos_enviados_nao_avaliados/', views.AutorProjetosEnviadosNaoAvaliados.as_view()),

    path('projetos_avaliados/', views.ProjetosAvaliados.as_view()),
    path('projetos_vencedores_maior_nota/', views.ProjetosVencedoresComMaiorNota.as_view()),

    # lista para um select no premio
    path('ProjetosNaoPremiados/', views.ProjetosNaoPremiados.as_view()),
    path('projetos_enviados_nao_avaliados/', views.ProjetosEnviadosNaoAvaliados.as_view()),

]
