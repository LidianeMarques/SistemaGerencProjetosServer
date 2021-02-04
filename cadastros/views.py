from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import generics

from cadastros.models import Autor
from cadastros.models import Avaliacao
from cadastros.models import Avaliador
from cadastros.models import Cronograma
from cadastros.models import Premio
from cadastros.models import Projeto
from cadastros.models import Telefone
from cadastros.serializers import AutorSerializer, TelefoneSerializer, AvaliadorSerializer, AvaliacaoSerializer, \
    ProjetoSerializer, CronogramaSerializer, PremioSerializer, \
      ProjetosConsultasSerializer, AutoresEProjetosConsultasSerializer


# Create your views here.
# CRUD Telefone
class TelefoneList(generics.ListCreateAPIView):
    queryset = Telefone.objects.all()
    serializer_class = TelefoneSerializer


class TelefoneDelete(generics.DestroyAPIView):
    queryset = Telefone.objects.all()
    serializer_class = TelefoneSerializer


class TelefoneUpdate(generics.UpdateAPIView):
    queryset = Telefone.objects.all()
    serializer_class = TelefoneSerializer


class TelefoneListarId(generics.RetrieveAPIView):
    queryset = Telefone.objects.all()
    serializer_class = TelefoneSerializer


# CRUD AUTOR
class AutorList(generics.ListCreateAPIView):

    queryset = Autor.objects.all()
    serializer_class = AutorSerializer

    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]

    search_fields = ['nome', 'endereco', 'email']
    ordering_fields = '__all__'
    filterset_fields = '__all__'



class AutorDelete(generics.DestroyAPIView):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer


class AutorUpdate(generics.UpdateAPIView):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer


class AutorListarId(generics.RetrieveAPIView):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer


# CRUD AVALIADOR
class AvaliadorList(generics.ListCreateAPIView):
    queryset = Avaliador.objects.all()
    serializer_class = AvaliadorSerializer

    filter_backends = [filters.SearchFilter,DjangoFilterBackend,filters.OrderingFilter]
    search_fields = ["id", 'nome', 'endereco', 'email', "numero_registro"]
    ordering_fields = ["id", 'nome', 'endereco', 'email', "numero_registro"]
    filterset_fields = ["id", 'nome', 'endereco', 'email', "numero_registro"]


class AvaliadorDelete(generics.DestroyAPIView):
    queryset = Avaliador.objects.all()
    serializer_class = AvaliadorSerializer


class AvaliadorUpdate(generics.UpdateAPIView):
    queryset = Avaliador.objects.all()
    serializer_class = AvaliadorSerializer


class AvaliadorListarId(generics.RetrieveAPIView):
    queryset = Avaliador.objects.all()
    serializer_class = AvaliadorSerializer


# CRUD Avaliacao
class AvaliacaoList(generics.ListCreateAPIView):
    queryset = Avaliacao.objects.all()
    serializer_class = AvaliacaoSerializer

    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['parecer', 'nota', 'data']
    ordering_fields = ['id', 'parecer', 'nota', 'data', 'projeto', 'avaliador' ]
    filterset_fields = ['id', 'parecer', 'nota', 'data', 'projeto', 'avaliador' ]


class AvaliacaoDelete(generics.DestroyAPIView):
    queryset = Avaliacao.objects.all()
    serializer_class = AvaliacaoSerializer


class AvaliacaoUpdate(generics.UpdateAPIView):
    queryset = Avaliacao.objects.all()
    serializer_class = AvaliacaoSerializer


class AvaliacaoListarId(generics.RetrieveAPIView):
    queryset = Avaliacao.objects.all()
    serializer_class = AvaliacaoSerializer


# CRUD Projeto
class ProjetoList(generics.ListCreateAPIView):
    queryset = Projeto.objects.all()
    serializer_class = ProjetoSerializer

    filter_backends = (filters.SearchFilter,)
    filterset_fields = ['nome']


class ProjetoDelete(generics.DestroyAPIView):
    queryset = Projeto.objects.all()
    serializer_class = ProjetoSerializer


class ProjetoUpdate(generics.UpdateAPIView):
    queryset = Projeto.objects.all()
    serializer_class = ProjetoSerializer


class ProjetoListarId(generics.RetrieveAPIView):
    queryset = Projeto.objects.all()
    serializer_class = ProjetoSerializer


# CRUD Cronograma
class CronogramaList(generics.ListCreateAPIView):
    queryset = Cronograma.objects.all()
    serializer_class = CronogramaSerializer


class CronogramaDelete(generics.DestroyAPIView):
    queryset = Cronograma.objects.all()
    serializer_class = CronogramaSerializer


class CronogramaUpdate(generics.UpdateAPIView):
    queryset = Cronograma.objects.all()
    serializer_class = CronogramaSerializer


class CronogramaListarId(generics.RetrieveAPIView):
    queryset = Cronograma.objects.all()
    serializer_class = CronogramaSerializer


# CRUD Premio
class PremioList(generics.ListCreateAPIView):
    queryset = Premio.objects.all()
    serializer_class = PremioSerializer


class PremioDelete(generics.DestroyAPIView):
    queryset = Premio.objects.all()
    serializer_class = PremioSerializer


class PremioUpdate(generics.UpdateAPIView):
    queryset = Premio.objects.all()
    serializer_class = PremioSerializer


class PremioListarId(generics.RetrieveAPIView):
    queryset = Premio.objects.all()
    serializer_class = PremioSerializer


# Consulta Solicitadas
class listarProjetosEAutores(generics.ListAPIView):
    serializer_class = AutoresEProjetosConsultasSerializer
    queryset = Autor.objects.all()


class AutorProjetosEnviadosNaoAvaliados(generics.ListAPIView):
    serializer_class = AutoresEProjetosConsultasSerializer

    def get_queryset(self):
        return Autor.objects.filter(projetos__data_envio__isnull=False).filter(Q(
                Q(projetos__avaliacoes__isnull=True) or Q(projetos__avaliacoes__nota__isnull=True)
        ))
# -----------------------


class ProjetosAvaliados(generics.ListAPIView):
    serializer_class = ProjetosConsultasSerializer

    def get_queryset(self):
        ids_projeto = Avaliacao.objects.filter(nota__isnull=False).values("projeto_id")
        return Projeto.objects.filter(data_envio__isnull=False).filter(id__in=ids_projeto)


class ProjetosVencedoresComMaiorNota(generics.ListAPIView):
    serializer_class = ProjetosConsultasSerializer

    def get_queryset(self):
        ids_projeto = Premio.objects.filter(projeto__avaliacoes__nota__isnull=False).values("projeto_id")
        return Projeto.objects.filter(data_envio__isnull=False).filter(id__in=ids_projeto).order_by("-avaliacoes__nota")


# lista para os select
class ProjetosNaoPremiados(generics.ListAPIView):
    serializer_class = ProjetosConsultasSerializer

    def get_queryset(self):
        return Projeto.objects.filter(premios__isnull=True)


class ProjetosEnviadosNaoAvaliados(generics.ListAPIView):
    serializer_class = ProjetoSerializer

    def get_queryset(self):
        return Projeto.objects.filter(data_envio__isnull=False).filter(Q(
                Q(avaliacoes__isnull=True) or Q(avaliacoes__nota__isnull=True)
        ))