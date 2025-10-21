from rest_framework import serializers
from app.models import Student, Sponsor, Sponsor_of_Student, University
from django.db import models
from django.db.models import Sum


class UniversityModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = ("university_name",)

class SponsorSerializer(serializers.ModelSerializer):
    allocated_total = serializers.SerializerMethodField()

    def get_allocated_total(self, obj):
       total = obj.payment_amounts.aggregate(total=Sum('allocated_amount'))['total']
       return total or 0

    class Meta:
        model = Sponsor
        exclude = ('orgination_name', 'sponsor_type')


class SponsorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = "__all__"


class StudentSerializer(serializers.ModelSerializer):
    payment_amounts = serializers.SerializerMethodField()

    def get_payment_amounts(self, obj):
        return obj.allocated_amounts.aggregate(total=Sum('allocated_amount'))['total'] or 0
    class Meta:
        model = Student
        exclude = ('phone_number',)

class StudentDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = "__all__"

class AddSponsorshipSerializer(serializers.Serializer):
    student_id = serializers.IntegerField()
    sponsor_id = serializers.IntegerField()
    allocated_amount = serializers.DecimalField(max_digits=12, decimal_places=2)

class SponsorCountSerializer(serializers.Serializer):
    month = serializers.CharField()
    students = serializers.IntegerField()
    sponsors = serializers.IntegerField()


    
