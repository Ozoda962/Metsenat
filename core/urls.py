from django.contrib import admin
from django.urls import path
from app.views import SponsorRegisterAapivIEW
from app.views import StudentListAPIView, StudentDetailAPIView
from app.views import SponsorListAPIView, SponsorDetailAPIView
from app.views import AddStudentSponsorAPIView
from app.views import DashboardSummaryAPIView, DashboardChartAPIView
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('students/',StudentListAPIView.as_view()),
    path('students/<int:pk>/', StudentDetailAPIView.as_view()),
    path('sponsors/', SponsorListAPIView.as_view()),
    path('sponsors/<int:pk>/',SponsorDetailAPIView.as_view() ),    
    path('sponsor-register/', SponsorRegisterAapivIEW.as_view()),
    path('add-sponsor/', AddStudentSponsorAPIView.as_view()),
    path("summary/", DashboardSummaryAPIView.as_view()),
    path('chart/',DashboardChartAPIView.as_view()),
    path('api/token/', TokenObtainPairView.as_view())   
]
