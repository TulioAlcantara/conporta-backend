from rest_framework.serializers import ModelSerializer
from api.models import OrdinanceCitation, Directive, AdminUnitMember, Notification, Profile, Ordinance, OrdinanceMember, AdminUnit


class OrdinanceCitationSerializer(ModelSerializer):

    class Meta:
        model = OrdinanceCitation
        fields = '__all__'


class DirectiveSerializer(ModelSerializer):

    class Meta:
        model = Directive
        fields = '__all__'


class AdminUnitMemberSerializer(ModelSerializer):

    class Meta:
        model = AdminUnitMember
        fields = '__all__'


class NotificationSerializer(ModelSerializer):

    class Meta:
        model = Notification
        fields = '__all__'


class ProfileSerializer(ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'


class OrdinanceSerializer(ModelSerializer):

    class Meta:
        model = Ordinance
        fields = '__all__'


class OrdinanceMemberSerializer(ModelSerializer):

    class Meta:
        model = OrdinanceMember
        fields = '__all__'


class AdminUnitSerializer(ModelSerializer):

    class Meta:
        model = AdminUnit
        fields = '__all__'
