from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from api.serializers import OrdinanceCitationSerializer, DirectiveSerializer, AdminUnitMemberSerializer, \
    NotificationSerializer, ProfileSerializer, OrdinanceSerializer, OrdinanceMemberSerializer, AdminUnitSerializer, \
    AdminUnitMemberReadSerializer
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
            return AdminUnitMemberReadSerializer
        return AdminUnitMemberSerializer


class NotificationViewSet(ModelViewSet):
    queryset = Notification.objects.order_by('pk')
    serializer_class = NotificationSerializer


class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.order_by('pk')
    serializer_class = ProfileSerializer


class OrdinanceViewSet(ModelViewSet):
    queryset = Ordinance.objects.order_by('pk')
    serializer_class = OrdinanceSerializer


class OrdinanceMemberViewSet(ModelViewSet):
    queryset = OrdinanceMember.objects.order_by('pk')
    serializer_class = OrdinanceMemberSerializer


class AdminUnitViewSet(ModelViewSet):
    queryset = AdminUnit.objects.order_by('pk')
    serializer_class = AdminUnitSerializer

    def list(self, request, *args, **kwargs):
        search = request.GET.get('search', None)
        queryset = self.get_queryset()
        if search:
            queryset = queryset.filter(Q(id__icontains=search) | Q(name__icontains=search) | Q(
                initials__icontains=search))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        queryset = AdminUnitMember.objects.filter(admin_unit=pk)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = AdminUnitMemberReadSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = AdminUnitMemberReadSerializer(queryset, many=True)
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
