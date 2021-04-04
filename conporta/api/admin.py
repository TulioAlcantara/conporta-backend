from django.contrib import admin
from .models import OrdinanceCitation, Directive, AdminUnitMember, Notification, Profile, Ordinance, OrdinanceMember, AdminUnit


@admin.register(OrdinanceCitation)
class OrdinanceCitationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'type',
        'description',
        'from_ordinance',
        'to_ordinance',
    )
    list_filter = ('from_ordinance', 'to_ordinance')


@admin.register(Directive)
class DirectiveAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'type',
        'previous_directive',
        'description',
        'ordinance',
    )
    list_filter = ('previous_directive', 'ordinance')


@admin.register(AdminUnitMember)
class AdminUnitMemberAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'is_boss',
        'start_date',
        'end_date',
        'type',
        'description',
        'admin_unit',
        'profile',
    )
    list_filter = (
        'is_boss',
        'start_date',
        'end_date',
        'admin_unit',
        'profile',
    )
    raw_id_fields = ('ordinances_received',)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'date',
        'ordinance',
        'admin_unit',
        'admin_unit_member',
    )
    list_filter = ('date', 'ordinance', 'admin_unit', 'admin_unit_member')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)


@admin.register(Ordinance)
class OrdinanceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'identifier',
        'admin_unit_initials',
        'year',
        'expedition_date',
        'start_date',
        'end_date',
        'dou_publication_date',
        'sei_process_number',
        'theme',
        'summary',
        'description',
        'pdf_path',
        'author',
    )
    list_filter = (
        'expedition_date',
        'start_date',
        'end_date',
        'dou_publication_date',
        'author',
    )
    raw_id_fields = ('citations', 'members_refered')


@admin.register(OrdinanceMember)
class OrdinanceMemberAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'date',
        'reference_type',
        'occupation_type',
        'description',
        'workload',
        'ordinance',
        'member',
    )
    list_filter = ('date', 'ordinance', 'member')


@admin.register(AdminUnit)
class AdminUnitAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'intials',
        'type',
        'year',
        'last_expedition_number',
        'last_ordinance',
    )
    list_filter = ('last_ordinance',)
    raw_id_fields = ('ordinances', 'members')
    search_fields = ('name',)
