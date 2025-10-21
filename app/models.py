from django.db import models

class Sponsor(models.Model):
    class SponsorTypeChoice(models.TextChoices):
        INDIVIDUAL = 'individual', 'Jismoniy shaxs'
        LEGAL = 'legal', 'Yuridik shaxs'
    sponsor_type = models.CharField(
        max_length=255,
        choices=SponsorTypeChoice.choices,
        default=SponsorTypeChoice.INDIVIDUAL
    )
    class StatusSponsorChoice(models.TextChoices):
        NEW = 'new', 'Yangi'
        MODERATION = 'modernation', 'Moderinizatsiya'
        APPROVED = 'approved', 'Tasdiqlangan'
        CANCELLED = 'cancelled', 'Bekor qilingan '
    sponsor_status = models.CharField(
        max_length=255,
        choices=StatusSponsorChoice.choices,
        default=StatusSponsorChoice.NEW
    )
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=13)
    payment_amount = models.PositiveBigIntegerField()
    orgination_name = models.CharField(max_length=255,null= True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class University(models.Model):
    university_name = models.CharField(max_length=255)

class Student(models.Model):
    class DegreeStudentChoice(models.TextChoices):
        BACHELOR = 'bachelor', 'Bakalavr'
        MASTER = 'master', 'Magistr'
    degree_student = models.CharField(
        max_length=255,
        choices=DegreeStudentChoice.choices
    )
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=13)
    contract_sum = models.PositiveBigIntegerField()
    university = models.ForeignKey(
        University,
        related_name='students',
        on_delete=models.PROTECT
    )
    created_at = models.DateTimeField(auto_now_add=True)
   
class Sponsor_of_Student(models.Model):
    sponsor = models.ForeignKey(
        Sponsor,
        related_name='payment_amounts',
        on_delete=models.PROTECT
    )

    student = models.ForeignKey(
        Student,
        related_name='allocated_amounts',
        on_delete=models.PROTECT
    )

    allocated_amount = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)