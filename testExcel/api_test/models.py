from api_test.constantes import ETAT_TACHE
from datetime import date
from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class Post(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def  __str__(self):
        return self.title



class Operateur(models.Model):
    nom         = models.CharField(max_length=100)
    description = models.CharField(max_length=512)
    account     = models.CharField(max_length=50)
    code        = models.CharField(max_length=50, null=True, unique=True)

    class Meta:
        ordering = ['nom']

    def __str__(self) -> str:
        return self.nom

class Tache(models.Model):
    libelle     = models.CharField(max_length=50)
    description = models.CharField(max_length=512)
    dateDebut   = models.DateTimeField(verbose_name='Date de début')
    dateFin     = models.DateTimeField(verbose_name='Date de fin')
    owner       = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    operateur   = models.ForeignKey(Operateur, on_delete=models.SET_NULL, null=True, blank=True)
    etat        = models.CharField(choices=ETAT_TACHE, max_length=50, default='CREATION')

    dateCreation = models.DateTimeField(auto_now_add=True)
    dateUpdate   = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.libelle


class TrxOperateur(models.Model):
    payment_date = models.DateTimeField(max_length=200)
    payid = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    phone_num = models.CharField(max_length=200)
    amount = models.CharField(max_length=200)
    trans_id = models.CharField(max_length=200)
    account = models.CharField(max_length=200) # Operateur
    agent = models.CharField(max_length=200) # user
    # operateur   = models.ForeignKey(Operateur, on_delete=models.SET_NULL, null=True)
    # owner       = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tache       = models.ForeignKey(Tache, on_delete=models.SET_NULL, null=True)


class TrxDdvaVisa(models.Model):
    payment_date = models.DateTimeField(max_length=200)
    payid = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    amount = models.CharField(max_length=200)
    trans_id = models.CharField(max_length=200)
    account = models.CharField(max_length=200)
    agent = models.CharField(max_length=200)
    # owner       = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tache       = models.ForeignKey(Tache, on_delete=models.SET_NULL, null=True)

class TrxDifferenceDdvaVisa(models.Model):
    payment_date = models.DateTimeField(max_length=200)
    payid = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    amount = models.CharField(max_length=200)
    trans_id = models.CharField(max_length=200)
    account = models.CharField(max_length=200)
    agent = models.CharField(max_length=200)
    # owner       = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tache       = models.ForeignKey(Tache, on_delete=models.SET_NULL, null=True)

class TrxDifference(models.Model):
    payment_date = models.DateTimeField(max_length=200)
    payid = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    phone_num = models.CharField(max_length=200)
    amount = models.CharField(max_length=200)
    trans_id = models.CharField(max_length=200)
    account = models.CharField(max_length=200)
    agent = models.CharField(max_length=200)
    # operateur   = models.ForeignKey(Operateur, on_delete=models.SET_NULL, null=True)
    # owner       = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tache       = models.ForeignKey(Tache, on_delete=models.SET_NULL, null=True)



class TrxSuccessCinetpay(models.Model):
    created_at = models.DateTimeField(max_length=200)
    cpm_payment_date = models.CharField(max_length=200)
    marchand = models.CharField(max_length=200)
    EmailMarchand = models.CharField(max_length=200)
    NomDuService = models.CharField(max_length=200)
    cpm_trans_id = models.CharField(max_length=200)
    cpm_site_id = models.CharField(max_length=200)
    cpm_amount = models.CharField(max_length=200)
    cpm_currency = models.CharField(max_length=200)
    payment_method = models.CharField(max_length=200)
    cel_phone_num = models.CharField(max_length=200)
    cpm_trans_status = models.CharField(max_length=200)
    cpm_payid= models.CharField(max_length=200)
    account = models.CharField(max_length=200)
    agent = models.CharField(max_length=200)
    cpm_custom = models.CharField(max_length=200)
    # operateur   = models.ForeignKey(Operateur, on_delete=models.SET_NULL, null=True)
    # owner       = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tache       = models.ForeignKey(Tache, on_delete=models.SET_NULL, null=True)
    

class TrxFailedCinetpay(models.Model):
    created_at = models.DateTimeField(max_length=200)
    cpm_payment_date = models.CharField(max_length=200)
    marchand = models.CharField(max_length=200)
    EmailMarchand = models.CharField(max_length=200)
    NomDuService = models.CharField(max_length=200)
    cpm_trans_id = models.CharField(max_length=200)
    cpm_site_id = models.CharField(max_length=200)
    cpm_amount = models.CharField(max_length=200)
    cpm_currency = models.CharField(max_length=200)
    payment_method = models.CharField(max_length=200)
    cel_phone_num = models.CharField(max_length=200)
    cpm_trans_status = models.CharField(max_length=200)
    cpm_payid= models.CharField(max_length=200)
    account = models.CharField(max_length=200)
    agent = models.CharField(max_length=200)
    cpm_custom = models.CharField(max_length=200)
    # operateur   = models.ForeignKey(Operateur, on_delete=models.SET_NULL, null=True)
    # owner       = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tache       = models.ForeignKey(Tache, on_delete=models.SET_NULL, null=True)



class TrxRightCorrespodent(models.Model):
    payment_date = models.CharField(max_length=200)
    payid = models.CharField(max_length=200)
    phone_num= models.CharField(max_length=200)
    amount = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    account = models.CharField(max_length=200)
    agent = models.CharField(max_length=200)
    created_atCorrespondent = models.CharField(max_length=200)
    cel_phone_numCorrespondant = models.CharField(max_length=200)
    AmountCorrespodent = models.CharField(max_length=200)
    payment_methodCorrespondant = models.CharField(max_length=200)
    StautTransactionCorrespondent = models.CharField(max_length=200)
    cpm_trans_idCorrespondent = models.CharField(max_length=200)
    # operateur   = models.ForeignKey(Operateur, on_delete=models.SET_NULL, null=True)
    # owner       = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tache       = models.ForeignKey(Tache, on_delete=models.SET_NULL, null=True)


class TrxRightCorrespodentDdvaVisa(models.Model):
    payment_date = models.CharField(max_length=200)
    payid = models.CharField(max_length=200)
    trans_id= models.CharField(max_length=200)
    amount = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    account = models.CharField(max_length=200)
    agent = models.CharField(max_length=200)
    created_atCorrespondent = models.CharField(max_length=200)
    cel_phone_numCorrespondant = models.CharField(max_length=200)
    AmountCorrespodent = models.CharField(max_length=200)
    payment_methodCorrespondant = models.CharField(max_length=200)
    StautTransactionCorrespondent = models.CharField(max_length=200)
    cpm_trans_idCorrespondent = models.CharField(max_length=200)
    cpm_customCorrespondent = models.CharField(max_length=200)
    # owner       = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tache       = models.ForeignKey(Tache, on_delete=models.SET_NULL, null=True)

class Trxreconciled(models.Model):
    payment_date = models.CharField(max_length=200)
    payid = models.CharField(max_length=200)
    phone_num= models.CharField(max_length=200)
    amount = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    account = models.CharField(max_length=200)
    agent = models.CharField(max_length=200)
    created_atCorrespondent = models.CharField(max_length=200)
    cel_phone_numCorrespondant = models.CharField(max_length=200)
    AmountCorrespodent = models.CharField(max_length=200)
    payment_methodCorrespondant = models.CharField(max_length=200)
    StautTransactionCorrespondent = models.CharField(max_length=200)
    cpm_trans_idCorrespondent = models.CharField(max_length=200)
    Time = models.DateTimeField(auto_now_add=True, null=False)
    cpm_custom = models.CharField(max_length=200)
    # operateur   = models.ForeignKey(Operateur, on_delete=models.SET_NULL, null=True)
    # owner       = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tache       = models.ForeignKey(Tache, on_delete=models.SET_NULL, null=True)


class TrxreconciledDdvaVisa(models.Model):
    payment_date = models.DateTimeField(max_length=200)
    payid = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    amount = models.CharField(max_length=200)
    trans_id = models.CharField(max_length=200)
    account = models.CharField(max_length=200)
    agent = models.CharField(max_length=200)
    created_atCorrespondent = models.CharField(max_length=200)
    cel_phone_numCorrespondant = models.CharField(max_length=200)
    AmountCorrespodent = models.CharField(max_length=200)
    payment_methodCorrespondant = models.CharField(max_length=200)
    StautTransactionCorrespondent = models.CharField(max_length=200)
    cpm_trans_idCorrespondent = models.CharField(max_length=200)
    Time = models.DateTimeField(auto_now_add=True, null=False)
    cpm_custom = models.CharField(max_length=200)
    # owner       = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tache       = models.ForeignKey(Tache, on_delete=models.SET_NULL, null=True)

class TrxNonereconciled(models.Model):
    payment_date = models.CharField(max_length=200)
    payid = models.CharField(max_length=200)
    phone_num= models.CharField(max_length=200)
    amount = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    account = models.CharField(max_length=200)
    agent = models.CharField(max_length=200)
    cpm_custom = models.CharField(max_length=200)
    Time = models.DateTimeField(auto_now_add=True, null=False)
    # operateur   = models.ForeignKey(Operateur, on_delete=models.SET_NULL, null=True)
    # owner       = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tache       = models.ForeignKey(Tache, on_delete=models.SET_NULL, null=True)



class TrxNonereconciledDdvaVisa(models.Model):
    payment_date = models.DateTimeField(max_length=200)
    payid = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    amount = models.CharField(max_length=200)
    trans_id = models.CharField(max_length=200)
    account = models.CharField(max_length=200)
    agent = models.CharField(max_length=200)
    Time = models.DateTimeField(auto_now_add=True, null=False)
    # owner       = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tache       = models.ForeignKey(Tache, on_delete=models.SET_NULL, null=True)


class TrxCorrespondent(models.Model):
    created_at = models.DateTimeField(max_length=200)
    cpm_payment_date = models.CharField(max_length=200)
    marchand = models.CharField(max_length=200)
    EmailMarchand = models.CharField(max_length=200)
    NomDuService = models.CharField(max_length=200)
    cpm_trans_id = models.CharField(max_length=200)
    cpm_site_id = models.CharField(max_length=200)
    cpm_amount = models.CharField(max_length=200)
    cpm_currency = models.CharField(max_length=200)
    payment_method = models.CharField(max_length=200)
    cel_phone_num = models.CharField(max_length=200)
    cpm_trans_status = models.CharField(max_length=200)
    cpm_payid= models.CharField(max_length=200)
    account = models.CharField(max_length=200)
    agent = models.CharField(max_length=200)
    cpm_custom = models.CharField(max_length=200)
    # operateur   = models.ForeignKey(Operateur, on_delete=models.SET_NULL, null=True)
    # owner       = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tache       = models.ForeignKey(Tache, on_delete=models.SET_NULL, null=True)



class TrxCinetpay(models.Model):
    created_at = models.DateTimeField(max_length=200)
    cpm_payment_date = models.CharField(max_length=200)
    marchand = models.CharField(max_length=200)
    EmailMarchand = models.CharField(max_length=200)
    NomDuService = models.CharField(max_length=200)
    cpm_trans_id = models.CharField(max_length=200)
    cpm_site_id = models.CharField(max_length=200)
    cpm_amount = models.CharField(max_length=200)
    cpm_currency = models.CharField(max_length=200)
    payment_method = models.CharField(max_length=200)
    cel_phone_num = models.CharField(max_length=200)
    cpm_trans_status = models.CharField(max_length=200)
    cpm_payid= models.CharField(max_length=200)
    cpm_custom = models.CharField(max_length=200)
    # operateur   = models.ForeignKey(Operateur, on_delete=models.SET_NULL, null=True)
    # owner       = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    # def __str__(self):
    #     return "{} {} {}".format(self.payid, self.cpm_payment_date, self.marchand)

