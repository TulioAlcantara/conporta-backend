from django.db import models


class OrdinanceCitation(models.Model):
    class OrdinanceType(models.IntegerChoices):
        ANULACAO = 1, 'Anulação'
        MENCAO = 2, 'Menção'
        RETIFICACAO = 3, 'Retificação'
        REVOGACAO = 4, 'Revogação'

    type = models.IntegerField(
        default=OrdinanceType.ANULACAO, choices=OrdinanceType.choices)
    description = models.TextField()
    from_ordinance = models.ForeignKey(
        'Ordinance', on_delete=models.CASCADE, related_name='from_ordinance')
    to_ordinance = models.ForeignKey(
        'Ordinance', on_delete=models.CASCADE, related_name='to_ordinance')


class Directive(models.Model):
    class DirectiveType(models.IntegerChoices):
        ORIENTACAO = 1, 'Orientação'
        REGRA = 2, 'Regra'

    type = models.IntegerField(
        default=DirectiveType.ORIENTACAO, choices=DirectiveType.choices)
    previous_directive = models.ForeignKey(
        'self', on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField()
    ordinance = models.ForeignKey(
        'Ordinance', on_delete=models.CASCADE, related_name='directives')


class AdminUnitMember(models.Model):
    class AdminUnitMemberType(models.IntegerChoices):
        DOCENTE = 1, 'Docente'
        ESTAGIARIO = 2, 'Estagiário'
        ESTUDANTE = 3, 'Estudante'
        TECNICO_ADMINISTRATIVO = 4, 'Técnico-Administrativo'

    is_boss = models.BooleanField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
    type = models.IntegerField(
        default=AdminUnitMemberType.DOCENTE, choices=AdminUnitMemberType.choices)
    description = models.TextField()
    admin_unit = models.ForeignKey(
        'AdminUnit', on_delete=models.CASCADE)
    profile = models.ForeignKey(
        'Profile', on_delete=models.CASCADE)
    ordinances_received = models.ManyToManyField(
        'Ordinance', through='OrdinanceMember')

    def __str__(self):
        return f'{self.profile.name} - {self.admin_unit.name}'


class Notification(models.Model):
    date = models.DateTimeField(blank=True, null=True)
    ordinance = models.ForeignKey('Ordinance', on_delete=models.CASCADE)
    admin_unit = models.ForeignKey(
        'AdminUnit', on_delete=models.CASCADE)
    admin_unit_member = models.ForeignKey(
        'AdminUnitMember', on_delete=models.CASCADE)


class Profile(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    is_active = models.BooleanField()

    def __str__(self):
        return self.name


class Ordinance(models.Model):
    class OrdinanceStatus(models.IntegerChoices):
        PROPOSTA = 1, 'Proposta'
        VIGENTE = 2, 'Vigente'
        EXPIRADA = 3, 'Expirada'
        ANULADA = 4, 'Anulada'
        RETIFICADA = 5, 'Retificada'
        REVOGADA = 6, 'Revogada'

    identifier = models.CharField(max_length=255)
    admin_unit_initials = models.CharField(max_length=255)
    status = models.IntegerField(
        default=OrdinanceStatus.PROPOSTA, choices=OrdinanceStatus.choices)
    expedition_date = models.DateTimeField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
    dou_publication_date = models.DateTimeField(blank=True, null=True)
    sei_process_number = models.IntegerField(blank=True, null=True)
    theme = models.TextField()
    summary = models.TextField(blank=True, null=True)
    description = models.TextField()
    pdf_path = models.CharField(max_length=255, blank=True, null=True)
    citations = models.ManyToManyField(
        'self', through=OrdinanceCitation)
    author = models.ForeignKey(
        AdminUnitMember, on_delete=models.CASCADE, related_name='is_author_of', blank=True, null=True)
    members_refered = models.ManyToManyField(
        AdminUnitMember, through='OrdinanceMember')

    def __str__(self):
        return self.identifier


class OrdinanceMember(models.Model):
    class ReferenceType(models.IntegerChoices):
        AFASTAMENTO = 1, 'Afastamento'
        APOSENTADORIA = 2, 'Aposentadoria'
        CESSAO = 3, 'Cessão'
        CONTRATACAO = 4, 'Contratação'
        DEMISSAO = 5, 'Demissão'
        DESIGNACAO = 6, 'Designação'
        DISPENSA = 7, 'Dispensa'
        EXONERACAO = 8, 'Exonereção'
        NOMEACAO = 9, 'Nomeação'
        PENALIDADE = 10, 'Penalidade'
        PENSAO = 11, 'Pensão'
        PRORROGACAO = 12, 'Prorrogação'
        RECONDUCAO = 13, 'Recondução'
        REDISTRIBUICAO = 14, 'Redistribuição'
        REMOCAO = 15, 'Remoção'
        RESCISAO = 16, 'Rescisão'
        VACANCIA = 17, 'Vacância'

    class FunctionType(models.IntegerChoices):
        PRESIDENTE = 1, 'Presidente'
        VICE_PRESIDENTE = 2, 'Vice-presidente'
        MEMBRO = 3, 'Membro'
        TITULAR = 4, 'Titular'
        MEMBRO_SUPLENTE = 5, 'Membro Suplente'
        COORDENADOR = 6, 'Coordenador'
        VICE_COORDENADOR = 7, 'Vice-coordenador'
        REPRESETANTE = 8, 'Represetante'
        REITOR = 9, 'Reitor'
        VICE_REITOR = 10, 'Vice-reitor'
        PRO_REITOR = 11, 'Pro-reitor'
        PRO_REITOR_ADJUNTO = 12, 'Pro-reitor Adjunto'
        SECRETARIO = 13, 'Secretario'
        SECRETARIO_ADJUNTO = 14, 'Secretario Adjunto'
        DIRETOR = 15, 'Diretor'
        VICE_DIRETOR = 16, 'Vice-diretor'

    date = models.DateTimeField(blank=True, null=True)
    reference_type = models.IntegerField(
        default=ReferenceType.AFASTAMENTO, choices=ReferenceType.choices)
    occupation_type = models.IntegerField(
        blank=True, null=True, default=FunctionType.PRESIDENTE, choices=FunctionType.choices)
    description = models.TextField(blank=True, null=True)
    workload = models.IntegerField(blank=True, null=True)
    ordinance = models.ForeignKey(Ordinance, on_delete=models.CASCADE)
    member = models.ForeignKey(AdminUnitMember, on_delete=models.CASCADE)


class AdminUnit(models.Model):
    class AdminUnitType(models.IntegerChoices):
        ADMINISTRACAO_CENTRAL = 1, 'Administração Central'
        CAMPUS = 2, 'Câmpus'
        CURSO = 3, 'Curso'
        COLEGIADO = 4, 'Colegiado'
        CONSELHO = 5, 'Conselho'
        ORGAO = 6, 'Orgão'
        REGIONAL = 7, 'Regional'
        UNIDADE_ACADEMICA = 8, 'Unidade Acadêmica'
        UNIDADE_EXTERNA = 9, 'Unidade Externa'

    name = models.CharField(max_length=255)
    initials = models.CharField(max_length=255)
    type = models.IntegerField(
        default=AdminUnitType.ADMINISTRACAO_CENTRAL, choices=AdminUnitType.choices)
    year = models.IntegerField()
    last_ordinance = models.ForeignKey(
        Ordinance, on_delete=models.CASCADE, related_name='last_admin_unit', blank=True, null=True)
    ordinances = models.ManyToManyField(
        Ordinance, through='Notification')
    members = models.ManyToManyField(
        Profile, through='AdminUnitMember')

    def __str__(self):
        return self.name
