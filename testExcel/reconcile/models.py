from django.db import models


class TrxOperateur(models.Model):
    datepaiment = models.DateTimeField(max_length=200)
    idpaiment = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    telephone = models.CharField(max_length=200)
    montant = models.CharField(max_length=200)
    idtransaction = models.CharField(max_length=200)

class TrxDifference(models.Model):
    datepaiment = models.DateTimeField(max_length=200)
    idpaiment = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    telephone = models.CharField(max_length=200)
    montant = models.CharField(max_length=200)
    idtransaction = models.CharField(max_length=200)

class TrxSuccessCinetpay(models.Model):
    creation = models.DateTimeField(max_length=200)
    datePaiement = models.CharField(max_length=200)
    marchand = models.CharField(max_length=200)
    EmailMarchand = models.CharField(max_length=200)
    NomDuService = models.CharField(max_length=200)
    IdTransaction = models.CharField(max_length=200)
    SiteId = models.CharField(max_length=200)
    Montant = models.CharField(max_length=200)
    Devise = models.CharField(max_length=200)
    methodePaiment = models.CharField(max_length=200)
    Telephone = models.CharField(max_length=200)
    EtatTransaction = models.CharField(max_length=200)
    IdPaiment = models.CharField(max_length=200)


class TrxFailedCinetpay(models.Model):
    creation = models.DateTimeField(max_length=200)
    datePaiement = models.CharField(max_length=200)
    marchand = models.CharField(max_length=200)
    EmailMarchand = models.CharField(max_length=200)
    NomDuService = models.CharField(max_length=200)
    IdTransaction = models.CharField(max_length=200)
    SiteId = models.CharField(max_length=200)
    Montant = models.CharField(max_length=200)
    Devise = models.CharField(max_length=200)
    methodePaiment = models.CharField(max_length=200)
    Telephone = models.CharField(max_length=200)
    EtatTransaction = models.CharField(max_length=200)
    IdPaiment = models.CharField(max_length=200)

class TrxRightCorrespodent(models.Model):
    datePaiement = models.CharField(max_length=200)
    idpaiment = models.CharField(max_length=200)
    telephone= models.CharField(max_length=200)
    montant = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    creationCorrespondent = models.CharField(max_length=200)
    TelephoneCorrespondant = models.CharField(max_length=200)
    AmountCorrespodent = models.CharField(max_length=200)
    methodePaimentCorrespondant = models.CharField(max_length=200)
    StautTransactionCorrespondent = models.CharField(max_length=200)
    IdTransactionCorrespondent = models.CharField(max_length=200)


class TrxCorrespondent(models.Model):
    creation = models.DateTimeField(max_length=200)
    datePaiement = models.CharField(max_length=200)
    marchand = models.CharField(max_length=200)
    EmailMarchand = models.CharField(max_length=200)
    NomDuService = models.CharField(max_length=200)
    IdTransaction = models.CharField(max_length=200)
    SiteId = models.CharField(max_length=200)
    Montant = models.CharField(max_length=200)
    Devise = models.CharField(max_length=200)
    methodePaiment = models.CharField(max_length=200)
    Telephone = models.CharField(max_length=200)
    EtatTransaction = models.CharField(max_length=200)
    IdPaiment = models.CharField(max_length=200)

class TrxCinetpay(models.Model):
    creation = models.DateTimeField(max_length=200)
    datePaiement = models.CharField(max_length=200)
    marchand = models.CharField(max_length=200)
    EmailMarchand = models.CharField(max_length=200)
    NomDuService = models.CharField(max_length=200)
    IdTransaction = models.CharField(max_length=200)
    SiteId = models.CharField(max_length=200)
    Montant = models.CharField(max_length=200)
    Devise = models.CharField(max_length=200)
    methodePaiment = models.CharField(max_length=200)
    Telephone = models.CharField(max_length=200)
    EtatTransaction = models.CharField(max_length=200)
    IdPaiment = models.CharField(max_length=200)

    # def __str__(self):
    #     return "{} {} {}".format(self.IdPaiment, self.datePaiement, self.marchand)

