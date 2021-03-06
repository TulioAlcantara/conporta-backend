# Generated by Django 3.1.7 on 2021-04-04 05:18

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20210403_0033'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordinance',
            name='description',
            field=models.TextField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ordinance',
            name='dou_publication_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='ordinance',
            name='pdf_path',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='ordinance',
            name='sei_process_number',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='ordinance',
            name='summary',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='ordinance',
            name='theme',
            field=models.TextField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='adminunit',
            name='type',
            field=models.IntegerField(choices=[(1, 'Administração Central'), (2, 'Câmpus'), (3, 'Curso'), (4, 'Colegiado'), (5, 'Conselho'), (6, 'Orgão'), (7, 'Regional'), (8, 'Unidade Acadêmica'), (9, 'Unidade Externa')], default=1),
        ),
        migrations.AlterField(
            model_name='adminunitmember',
            name='end_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='adminunitmember',
            name='type',
            field=models.IntegerField(choices=[(1, 'Docente'), (2, 'Estagiário'), (3, 'Estudante'), (4, 'Técnico-Administrativo')], default=1),
        ),
        migrations.AlterField(
            model_name='directive',
            name='previous_directive',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.directive'),
        ),
        migrations.AlterField(
            model_name='directive',
            name='type',
            field=models.IntegerField(choices=[(1, 'Orientação'), (2, 'Regra')], default=1),
        ),
        migrations.AlterField(
            model_name='ordinance',
            name='end_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ordinancecitation',
            name='type',
            field=models.IntegerField(choices=[(1, 'Anulação'), (2, 'Menção'), (3, 'Retificação'), (4, 'Revogação')], default=1),
        ),
        migrations.AlterField(
            model_name='ordinancemember',
            name='date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ordinancemember',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ordinancemember',
            name='occupation_type',
            field=models.IntegerField(blank=True, choices=[(1, 'Presidente'), (2, 'Vice-presidente'), (3, 'Membro'), (4, 'Titular'), (5, 'Membro Suplente'), (6, 'Coordenador'), (7, 'Vice-coordenador'), (8, 'Represetante'), (9, 'Reitor'), (10, 'Vice-reitor'), (11, 'Pro-reitor'), (12, 'Pro-reitor Adjunto'), (13, 'Secretario'), (14, 'Secretario Adjunto'), (15, 'Diretor'), (16, 'Vice-diretor')], default=1, null=True),
        ),
        migrations.AlterField(
            model_name='ordinancemember',
            name='reference_type',
            field=models.IntegerField(choices=[(1, 'Afastamento'), (2, 'Aposentadoria'), (3, 'Cessão'), (4, 'Contratação'), (5, 'Demissão'), (6, 'Designação'), (7, 'Dispensa'), (8, 'Exonereção'), (9, 'Nomeação'), (10, 'Penalidade'), (11, 'Pensão'), (12, 'Prorrogação'), (13, 'Recondução'), (14, 'Redistribuição'), (15, 'Remoção'), (16, 'Rescisão'), (17, 'Vacância')], default=1),
        ),
        migrations.AlterField(
            model_name='ordinancemember',
            name='workload',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
