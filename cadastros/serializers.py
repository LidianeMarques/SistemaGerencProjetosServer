from django.db import transaction
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from cadastros.models import Autor
from cadastros.models import Avaliador
from cadastros.models import Projeto
from cadastros.models import Avaliacao
from cadastros.models import Telefone
from cadastros.models import Cronograma
from cadastros.models import Premio


class TelefoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Telefone
        fields = '__all__'


class ProjetoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projeto
        fields = '__all__'  # ['id', 'titulo', 'data_envio', 'area', 'resumo']


class AutorSerializer(serializers.ModelSerializer):
    telefones = TelefoneSerializer(many=True, required=False)
    projetos = ProjetoSerializer()

    class Meta:
        ordering = ['-id']
        model = Autor
        fields = '__all__'

    @transaction.atomic
    def create(self, validated_data):
        lista_telefones = validated_data.pop('telefones')
        projeto = validated_data.pop('projetos')

        autor = Autor.objects.update_or_create(**validated_data)[0]
        for telefone in lista_telefones:
            telefone['pessoa'] = autor
            Telefone.objects.create(**telefone)
        if projeto is not None and len(projeto) > 0:
            projeto.pop('autor')
            Projeto.objects.create(autor=autor, **projeto)
        return autor

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.nome = validated_data.get('nome', instance.nome)
        instance.endereco = validated_data.get('endereco', instance.endereco)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        projeto = validated_data.get('projetos')
        projeto.pop('autor')
        if hasattr(instance, 'projetos') and getattr(instance, 'projetos') is not None:
            Projeto.objects.filter(id=instance.projetos.id).update(**projeto)
        else:
            Projeto.objects.create(autor=instance, **projeto)

        telefones_ids = []
        for tel in validated_data.get('telefones'):
            tel['pessoa'] = instance
            id_tel = Telefone.objects.update_or_create(**tel)[0].id
            telefones_ids.append(id_tel)
        Telefone.objects.filter(pessoa=instance).exclude(id__in=telefones_ids).delete()

        return instance


class AvaliadorSerializer(serializers.ModelSerializer):
    telefones = TelefoneSerializer(many=True, required=False)

    class Meta:
        ordering = ['-id']
        model = Avaliador
        fields = '__all__'

    @transaction.atomic
    def create(self, validated_data):
        lista_telefones = validated_data.pop('telefones')
        avaliador = Avaliador.objects.update_or_create(**validated_data)[0]
        for telefone in lista_telefones:
            telefone['pessoa'] = avaliador
            Telefone.objects.create(**telefone)
        return avaliador

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.nome = validated_data.get('nome', instance.nome)
        instance.endereco = validated_data.get('endereco', instance.endereco)
        instance.email = validated_data.get('email', instance.email)
        instance.numero_registro = validated_data.get('numero_registro', instance.numero_registro)
        instance.save()
        telefones_ids = []
        for tel in validated_data.get('telefones'):
            tel['pessoa'] = instance
            id_tel = Telefone.objects.update_or_create(**tel)[0].id
            telefones_ids.append(id_tel)

        Telefone.objects.filter(pessoa=instance).exclude(id__in=telefones_ids).delete()

        return instance


class AvaliacaoSerializer(serializers.ModelSerializer):
    avaliador = serializers.PrimaryKeyRelatedField(queryset=Avaliador.objects.all())
    projeto = serializers.PrimaryKeyRelatedField(queryset=Projeto.objects.all())

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.parecer = validated_data.get('parecer', instance.parecer)
        instance.nota = validated_data.get('nota', instance.nota)
        instance.data = validated_data.get('data', instance.data)
        instance.avaliador = validated_data.get('avaliador', instance.avaliador)
        instance.projeto = validated_data.get('projeto', instance.projeto)
        instance.save()
        return instance

    class Meta:
        model = Avaliacao
        fields = '__all__'


class CronogramaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cronograma
        fields = '__all__'


class PremioSerializer(serializers.ModelSerializer):
    cronograma = CronogramaSerializer()
    projeto = serializers.PrimaryKeyRelatedField(queryset=Projeto.objects.all())

    class Meta:
        ordering = ['-id']
        model = Premio
        fields = '__all__'

    def create(self, validated_data):
        cronograma = validated_data.pop('cronograma')
        premio = Premio.objects.update_or_create(**validated_data)[0]

        if cronograma is not None and len(cronograma) > 0:
            cronograma['premio'] = premio
            Cronograma.objects.create(**cronograma)
        return premio

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.nome = validated_data.get('nome', instance.nome)
        instance.descricao = validated_data.get('descricao', instance.descricao)
        instance.ano = validated_data.get('ano', instance.ano)
        instance.save()

        cronograma = self.initial_data.get('cronograma').copy()
        cronograma.pop('id')
        cronograma.pop('premio')
        if hasattr(instance, 'cronograma') and getattr(instance, 'cronograma') is not None:
            Cronograma.objects.filter(id=instance.cronograma.id).update(**cronograma)
        else:
            Cronograma.objects.create(premio=instance, **cronograma)
        return instance


class TelefoneListingField(serializers.RelatedField):
    def to_representation(self, value):
        return '%s: (%s) %s' % (value.tipo, value.ddd, value.numero)


# Consulta Solicitadas
class AutoresEProjetosConsultasSerializer(serializers.ModelSerializer):
    projetos = ProjetoSerializer(many=False, read_only=True)
    telefones = TelefoneListingField(many=True, read_only=True)

    class Meta:
        model = Autor
        fields = ["id", "projetos", "nome", "telefones", "endereco", "email"]


class AvaliacaoConsultasSerializer(serializers.ModelSerializer):
    avaliador = serializers.SlugRelatedField(read_only=True, slug_field="nome")
    projeto = ProjetoSerializer(many=False, read_only=True)

    class Meta:
        model = Avaliacao
        fields = '__all__'


class ProjetosConsultasSerializer(serializers.ModelSerializer):
    avaliacoes = AvaliacaoConsultasSerializer(read_only=True)
    autor = serializers.SlugRelatedField(read_only=True, slug_field="nome")

    class Meta:
        model = Projeto
        fields = '__all__'



