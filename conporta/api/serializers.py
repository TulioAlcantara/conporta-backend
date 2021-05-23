from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from api.models import OrdinanceCitation, Directive, AdminUnitMember, Notification, Profile, Ordinance, OrdinanceMember, \
    AdminUnit


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


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


class AdminUnitMemberCompleteSerializer(ModelSerializer):
    profile = ProfileSerializer(many=False, read_only=True)
    admin_unit = AdminUnitSerializer(many=False, read_only=True)

    class Meta:
        model = AdminUnitMember
        fields = '__all__'


class OrdinanceMemberCompleteSerializer(ModelSerializer):
    member = AdminUnitMemberCompleteSerializer(many=False, read_only=True)

    class Meta:
        model = OrdinanceMember
        fields = '__all__'


