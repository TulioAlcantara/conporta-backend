from rest_framework.viewsets import ModelViewSet
from api.serializers import OrdinanceCitationSerializer, DirectiveSerializer, AdminUnitMemberSerializer, NotificationSerializer, ProfileSerializer, OrdinanceSerializer, OrdinanceMemberSerializer, AdminUnitSerializer
from api.models import OrdinanceCitation, Directive, AdminUnitMember, Notification, Profile, Ordinance, OrdinanceMember, AdminUnit


class OrdinanceCitationViewSet(ModelViewSet):
    queryset = OrdinanceCitation.objects.order_by('pk')
    serializer_class = OrdinanceCitationSerializer


class DirectiveViewSet(ModelViewSet):
    queryset = Directive.objects.order_by('pk')
    serializer_class = DirectiveSerializer


class AdminUnitMemberViewSet(ModelViewSet):
    queryset = AdminUnitMember.objects.order_by('pk')
    serializer_class = AdminUnitMemberSerializer


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
