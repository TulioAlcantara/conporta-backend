import datetime

from django.core import serializers
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from api.serializers import OrdinanceCitationSerializer, DirectiveSerializer, AdminUnitMemberSerializer, \
    NotificationSerializer, ProfileSerializer, OrdinanceSerializer, OrdinanceMemberSerializer, AdminUnitSerializer, \
    AdminUnitMemberCompleteSerializer, OrdinanceMemberCompleteSerializer, AdminUnitCompleteSerializer
from api.models import OrdinanceCitation, Directive, AdminUnitMember, Notification, Profile, Ordinance, \
    OrdinanceMember, AdminUnit


class OrdinanceCitationViewSet(ModelViewSet):
    queryset = OrdinanceCitation.objects.order_by('pk')
    serializer_class = OrdinanceCitationSerializer


class DirectiveViewSet(ModelViewSet):
    queryset = Directive.objects.order_by('pk')
    serializer_class = DirectiveSerializer


class AdminUnitMemberViewSet(ModelViewSet):
    queryset = AdminUnitMember.objects.order_by('pk')

    def get_serializer_class(self):
        if self.action == 'list':
            return AdminUnitMemberCompleteSerializer
        return AdminUnitMemberSerializer

    @action(detail=False, methods=['get'])
    def current_user_admin_unit_memberships(self, request):
        queryset = AdminUnitMember.objects.filter(profile__user=request.user.id)
        serializer = AdminUnitMemberCompleteSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def ordinance_awareness(self, request, pk=None):
        ordinance = request.GET.get('ordinance', None)
        ordinance = int(ordinance)
        ordinance_member = OrdinanceMember.objects.filter(member_id=pk, ordinance_id=ordinance).first()
        ordinance_member.date = datetime.datetime.now()
        ordinance_member.save()
        return Response()


class NotificationViewSet(ModelViewSet):
    queryset = Notification.objects.order_by('pk')
    serializer_class = NotificationSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        ordinance = request.GET.get('ordinance', None)
        member = request.GET.get('member', None)
        queryset = queryset.filter(ordinance__pk=ordinance, admin_unit_member__pk=member, date__isnull=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def awareness(self, request, pk=None):
        notification = Notification.objects.filter(pk=pk).first()
        notification.date = datetime.datetime.now()
        notification.save()
        return Response()


class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.order_by('pk')
    serializer_class = ProfileSerializer

    def list(self, request, *args, **kwargs):
        search = request.GET.get('search', None)
        queryset = self.get_queryset()
        if search:
            queryset = queryset.filter(Q(id__icontains=search) | Q(name__icontains=search) | Q(
                email__icontains=search))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def current_user_profile(self, request):
        queryset = Profile.objects.get(user=request.user.id)
        serializer = self.serializer_class(queryset)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == 'get':
            return AdminUnitMemberCompleteSerializer
        return ProfileSerializer


class OrdinanceViewSet(ModelViewSet):
    queryset = Ordinance.objects.order_by('pk')
    serializer_class = OrdinanceSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        author_ua = AdminUnit.objects.get(initials=serializer.data['admin_unit_initials'])
        author_ua.last_proposed_number = author_ua.last_proposed_number + 1
        author_ua.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        author_ua = AdminUnit.objects.get(initials=instance.admin_unit_initials)
        ordinance_issued = request.GET.get('ordinance-issued', None) == 'true'
        if ordinance_issued:
            author_ua.last_issued_number = author_ua.last_issued_number + 1
            author_ua.last_proposed_number = author_ua.last_proposed_number - 1
            author_ua.save()
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        search = request.GET.get('search', None)
        user_ua_list = AdminUnitMember.objects.filter(profile__user_id=request.user.id).values_list('admin_unit')
        queryset = self.get_queryset()
        queryset = queryset.filter(admin_unit__in=user_ua_list)
        if search:
            queryset = queryset.filter(Q(id__icontains=search) | Q(theme__icontains=search))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def citations(self, request, pk=None):
        queryset = OrdinanceCitation.objects.filter(Q(from_ordinance=pk) | Q(to_ordinance=pk))
        serializer = OrdinanceCitationSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        queryset = OrdinanceMember.objects.filter(ordinance=pk)
        serializer = OrdinanceMemberCompleteSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def directives(self, request, pk=None):
        queryset = Directive.objects.filter(ordinance=pk)
        serializer = DirectiveSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def non_cited_members(self, request, pk=None):
        search = request.GET.get('search', None)
        ordinance = Ordinance.objects.get(pk=pk)
        possible_admin_units = [ordinance.admin_unit.pk]
        child_admin_units = AdminUnit.objects.filter(parent_admin_unit=ordinance.admin_unit)
        for unit in child_admin_units:
            possible_admin_units.append(unit.pk)
        ordinance_members_ids = OrdinanceMember.objects.filter(ordinance=pk,).values_list('member', flat=True)
        queryset = AdminUnitMember.objects.filter(admin_unit__in=possible_admin_units).order_by('pk')
        if search:
            queryset = queryset.filter(
                (Q(admin_unit__name__icontains=search) | Q(profile__name__icontains=search)))
        queryset = queryset.exclude(
            pk__in=ordinance_members_ids)[:10]
        serializer = AdminUnitMemberCompleteSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def non_cited_ordinances(self, request, pk=None):
        search = request.GET.get('search', None)
        cited_ordinances_ids = OrdinanceCitation.objects.filter(from_ordinance=pk).values_list('to_ordinance',
                                                                                               flat=True)
        queryset = self.get_queryset()
        if search:
            queryset = queryset.filter(pk=search)
        queryset = queryset.exclude(pk__in=cited_ordinances_ids)[:10]
        serializer = OrdinanceSerializer(queryset, many=True)
        return Response(serializer.data)


def user_mentioned_ordinances_list(request, pk=None):
    user_memberships = request.GET.get('user_memberships', None)
    user_memberships = user_memberships.split(',')
    user_memberships = [int(item) for item in user_memberships]
    user_mentioned_ordinances = OrdinanceMember.objects.filter(member__pk__in=user_memberships,
                                                               date=None).values_list('ordinance', flat=True)
    queryset = Ordinance.objects.order_by('pk')
    queryset = queryset.filter(pk__in=user_mentioned_ordinances)
    serializer = OrdinanceSerializer(queryset, many=True)
    return JsonResponse(data=serializer.data, status=status.HTTP_200_OK, content_type='application/json', safe=False)


def user_notifications_ordinances_list(request, pk=None):
    user_memberships = request.GET.get('user_memberships', None)
    user_memberships = user_memberships.split(',')
    user_memberships = [int(item) for item in user_memberships]
    user_notifications = Notification.objects.filter(admin_unit_member__pk__in=user_memberships,
                                                     date=None).values_list('ordinance', flat=True)
    queryset = Ordinance.objects.order_by('pk')
    queryset = queryset.filter(pk__in=user_notifications)
    serializer = OrdinanceSerializer(queryset, many=True)
    return JsonResponse(data=serializer.data, status=status.HTTP_200_OK, content_type='application/json', safe=False)


class OrdinanceMemberViewSet(ModelViewSet):
    queryset = OrdinanceMember.objects.order_by('pk')
    serializer_class = OrdinanceMemberSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        member = AdminUnitMember.objects.filter(pk=serializer.data['member']).first()
        ordinance = Ordinance.objects.filter(pk=serializer.data['ordinance']).first()
        if not Notification.objects.filter(admin_unit=member.admin_unit.pk, ordinance=ordinance.pk).exists():
            admin_unit_boss = AdminUnitMember.objects.get(admin_unit=member.admin_unit, is_boss=True)
            new_notification = Notification.objects.create(ordinance=ordinance, admin_unit=member.admin_unit,
                                                           admin_unit_member=admin_unit_boss)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class AdminUnitViewSet(ModelViewSet):
    queryset = AdminUnit.objects.order_by('pk')
    serializer_class = AdminUnitSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AdminUnitCompleteSerializer
        return AdminUnitSerializer

    def list(self, request, *args, **kwargs):
        search = request.GET.get('search', None)
        queryset = self.get_queryset()
        if search:
            queryset = queryset.filter(Q(id__icontains=search) |
                                       Q(name__icontains=search) |
                                       Q(initials__icontains=search))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def parent_admin_unit_options(self, request, pk=None):
        search = request.GET.get('search', None)
        queryset = self.get_queryset()
        queryset = queryset.exclude(pk=pk)
        if search:
            queryset = queryset.filter(Q(id__icontains=search) | Q(name__icontains=search) | Q(
                initials__icontains=search))
        serializer = AdminUnitSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        queryset = AdminUnitMember.objects.filter(admin_unit=pk)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = AdminUnitMemberCompleteSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = AdminUnitMemberCompleteSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        queryset = AdminUnitMember.objects.filter(admin_unit=pk)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = AdminUnitMemberCompleteSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = AdminUnitMemberCompleteSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def non_member_profiles(self, request, pk=None):
        search = request.GET.get('search', None)
        queryset = Profile.objects.all().exclude(admin_unit_member__admin_unit__pk=pk)
        if search:
            queryset = queryset.filter(Q(id__icontains=search) | Q(name__icontains=search))
        queryset = queryset[:10]
        serializer = ProfileSerializer(queryset, many=True)
        return Response(serializer.data)
