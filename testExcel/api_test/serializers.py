from django.db import models
from django.forms import fields
from rest_framework import serializers

from .models import  Operateur,Profile, Post, Tache,TrxCorrespondent, TrxDifferenceDdvaVisa, TrxRightCorrespodentDdvaVisa,TrxSuccessCinetpay,TrxCinetpay,TrxFailedCinetpay,TrxRightCorrespodent,TrxOperateur,TrxDifference, Trxreconciled,TrxNonereconciled,TrxDdvaVisa



class PostSerializer(serializers.ModelSerializer):
    class Meta :
        model = Post
        fields ='__all__'

class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta :
        model = Profile
        fields ='__all__'
  




class TrxOperateurSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta :
        model = TrxOperateur
        fields =('datepaiment','idpaiment','status','telephone','montant', 'owner')

class TrxDifferenceSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta :
        model = TrxDifference
        fields ='__all__'

class TrxDifferenceDdvaVisaSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta :
        model = TrxDifferenceDdvaVisa
        fields ='__all__'

class TrxDdvaVisaSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta :
        model = TrxDdvaVisa
        fields ='__all__'


class TrxreconciledSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta :
        model = Trxreconciled
        fields ='__all__'


class TrxNonereconciledSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta :
        model = Trxreconciled
        fields ='__all__'



class TrxSuccessCinetpaySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta :
        model = TrxSuccessCinetpay
        fields ='__all__'

class TrxFailedCinetpaySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta :
        model = TrxFailedCinetpay
        fields ='__all__'

class TrxRightCorrespodentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta :
        model = TrxRightCorrespodent
        fields ='__all__'

class TrxRightCorrespodentDdvaVisaSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta :
        model = TrxRightCorrespodentDdvaVisa
        fields ='__all__'

class TrxCorrespondentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta :
        model = TrxCorrespondent
        fields ='__all__'

class TrxCinetpaySerializer(serializers.ModelSerializer):
    class Meta :
        model = TrxCinetpay
        fields = ('created_at','cpm_payment_date','marchand','NomDuService','cpm_trans_id' ,'cpm_site_id','cpm_amount','cpm_currency' ,'payment_method','cel_phone_num',
                 'cpm_trans_status','cpm_payid') 

    # def __str__(self):
    #     return "{} {} {}".format(self.IdPaiment, self.datePaiement, self.marchand)

class OperateurSerializer(serializers.ModelSerializer):
    class Meta:
        model   = Operateur
        fields  = '__all__' 

class TacheSerializer(serializers.ModelSerializer):
    dateCreation = serializers.ReadOnlyField()
    dateUpdate   = serializers.ReadOnlyField()
    etat         = serializers.ReadOnlyField()
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model   = Tache
        fields  = '__all__' 
    