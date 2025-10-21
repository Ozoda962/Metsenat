from django.shortcuts import render, HttpResponse
from .models import Student, Sponsor,Sponsor_of_Student, University
from rest_framework.decorators import api_view
from rest_framework.response import Response
from app.serializers import AddSponsorshipSerializer
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import Sum
from rest_framework import serializers
from django.db.models.functions import TruncMonth
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework import filters
from django.db.models import F, Count
from .serializers import SponsorSerializer, SponsorDetailSerializer, StudentDetailSerializer, StudentSerializer

class SponsorRegisterAapivIEW(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        full_name = request.data.get('full_name')
        phone_number = request.data.get('phone_number')
        sponsor_type = request.data.get('sponsor_type')
        payment_amount = request.data.get('payment_amount')
        orgination_name = request.data.get('orgination_name')

        if sponsor_type == 'individual':
            Sponsor.objects.create(
                full_name=full_name,
                phone_number=phone_number,
                sponsor_type= sponsor_type,
                payment_amount=payment_amount
            )
        else:
            Sponsor.objects.create(
                full_name=full_name,
                phone_number=phone_number,
                sponsor_type= sponsor_type,
                payment_amount=payment_amount,
                orgination_name=orgination_name
            )

        return Response(status=201)
    

class AddStudentSponsorAPIView(APIView):
   
    def post(self, request):
        data = request.data
        sponsor = data.get("sponsor")
        student = data.get("student")
        allocated_amount = int(data.get("allocated_amount"))

        sponsor = Sponsor.objects.get(id=sponsor)
        student = Student.objects.get(id=student)

        Sponsor_of_Student.objects.create(
            sponsor=sponsor,
            student=student,
            allocated_amount=allocated_amount
            )
                
        sponsor_allocated_amounts = Sponsor_of_Student.objects.filter(
            sponsor=sponsor).aggregate(
                total_amount=Sum('allocated_amount'))['total_amount'] or 0
        active_balance = sponsor.payment_amount - sponsor_allocated_amounts

        if active_balance < allocated_amount:
            raise serializers.ValidationError(
                {"error": f"Homiyda mablag' yetarli emas ({active_balance})"}
            )
        
        student_recived_amount = Sponsor_of_Student.objects.filter(
            student=student).aggregate(total_recived_amount=Sum('allocated_amount'))['total_recived_amount'] or 0
        student_needed_balance = student.contract_sum - student_recived_amount

        if student_needed_balance < allocated_amount:
            raise serializers.ValidationError(
                {"error": f"Talaba buncha mablag'ga muhtoj emas ({student_needed_balance})"}
            )

        Sponsor_of_Student.objects.create(
            sponsor=sponsor,
            student=student,
            allocated_amount=allocated_amount
        )
        return Response(status=201)
    

class DashboardSummaryAPIView(APIView):
    def get(self, request):
        total_contract_sum = Student.objects.aggregate(total=Sum('contract_sum'))['total'] or 0
        total_paid_sum = Sponsor_of_Student.objects.aggregate(
            total=Sum('allocated_amount'))['total'] or 0

        remaining_sum = total_contract_sum - total_paid_sum

        data = {
            "total_contract_sum": total_contract_sum,
            "total_paid_sum": total_paid_sum,
            "remaining_sum": remaining_sum if remaining_sum > 0 else 0
        }
        return Response(data, status=status.HTTP_200_OK)
    

class DashboardChartAPIView(APIView):
    def get(self, request):
        
        sponsor_data = (
            Sponsor.objects.annotate(month=TruncMonth('created_at'))
            .values('month')
            .annotate(count=Sum(1))
            .order_by('month')
        )

        student_data = (
            Student.objects.annotate(month=TruncMonth('created_at'))
            .values('month')
            .annotate(count=Sum(1))
            .order_by('month')
        )

       
        months = sorted(set([s['month'] for s in sponsor_data] + [s['month'] for s in student_data]))

        chart_data = []
        for month in months:
            chart_data.append({
                "month": month.strftime("%B %Y"),
                "sponsors": next((s['count'] for s in sponsor_data if s['month'] == month), 0),
                "students": next((s['count'] for s in student_data if s['month'] == month), 0),
            })

        return Response(chart_data, status=status.HTTP_200_OK)
       

class SponsorListAPIView(generics.ListAPIView):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filter_fields = ('status',)

class SponsorDetailAPIView(generics.RetrieveAPIView):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorDetailSerializer
    lookup_field = "pk"

class StudentListAPIView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filter_fields = ('full_name',)

class StudentDetailAPIView(generics.RetrieveAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentDetailSerializer
    lookup_field = "pk"


