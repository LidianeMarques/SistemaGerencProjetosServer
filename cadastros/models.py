from django.db import models


class Telefone(models.Model):
    tipo = models.CharField(max_length=200)
    ddd = models.CharField(max_length=200)
    numero = models.CharField(max_length=200)
    pessoa = models.ForeignKey("cadastros.Pessoa", related_name="telefones", on_delete=models.CASCADE,
                               null=True)

    def __str__(self):
        return "() {}".format(self.ddd, self.numero)


class Pessoa(models.Model):
    nome = models.CharField(max_length=200)
    endereco = models.CharField(max_length=200)
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.nome



class Projeto(models.Model):
    titulo = models.CharField(max_length=200)
    data_envio = models.DateField(null=True, blank=True)
    autor = models.OneToOneField(to='cadastros.Autor', related_name="projetos", on_delete=models.CASCADE, null=True)
    area = models.TextField()
    resumo = models.TextField()

    def listar_projetos(self):
        return Projeto.objects.all()

    def projetos_enviados(self):
        return Projeto.objects.filter(data_envio__isnull=False)

    def listar_projetos_avaliados(self):
        return Projeto.objects.filter(avaliacoes__nota__isnull=False)

    def listar_projetos_nao_avaliados(self):
        return Projeto.objects.filter(avaliacoes__nota__isnull=True)

    def __str__(self):
        return self.titulo


class Autor(Pessoa):

    def __str__(self):
        return self.nome



class Avaliador(Pessoa):
    numero_registro = models.IntegerField()

    def __str__(self):
        return "()-{}".format(self.nome, self.numero_registro)


class Avaliacao(models.Model):
    avaliador = models.ForeignKey(to='cadastros.Avaliador', on_delete=models.CASCADE, related_name="avaliacoes", null=True)
    projeto = models.OneToOneField(to="cadastros.Projeto", on_delete=models.CASCADE, related_name="avaliacoes", null=True)
    parecer = models.TextField(null=True, blank=True)
    nota = models.FloatField(null=True, blank=True)
    data = models.DateField(null=True, blank=True)

    def __str__(self):
        return '%s-%s' % (self.nota, self.data)


class Cronograma(models.Model):
    descricao = models.TextField()
    data_inicio = models.DateField()
    data_fim = models.DateField()
    premio = models.OneToOneField(to='cadastros.Premio', related_name='cronograma', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return '%s' % self.descricao


class Premio(models.Model):
    projeto = models.OneToOneField(to="cadastros.Projeto", related_name="premios", on_delete=models.CASCADE, null=True)
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    ano = models.IntegerField()

    def listar_premios(self):
        return Premio.objects.all()

    def __str__(self):
        return '%s' % self.nome
