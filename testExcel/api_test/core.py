from django.db.models import fields
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import parser_classes 
from .serializers import PostSerializer, TrxCinetpaySerializer,TrxDifferenceSerializer,TrxRightCorrespodentSerializer,TrxOperateurSerializer,TrxreconciledSerializer,TrxRightCorrespodentDdvaVisaSerializer,TrxDifferenceDdvaVisaSerializer
from .models import Post, Tache,TrxDifference,TrxOperateur,TrxRightCorrespodent,TrxFailedCinetpay,TrxCinetpay,TrxSuccessCinetpay,TrxCorrespondent, Trxreconciled,TrxNonereconciled,TrxDifferenceDdvaVisa,TrxNonereconciledDdvaVisa,TrxreconciledDdvaVisa,TrxRightCorrespodentDdvaVisa,TrxRightCorrespodentDdvaVisa,TrxDdvaVisa
from datetime import date, datetime
from rest_framework.response import Response
from rest_framework import status
import time
import requests
import json
from testExcel.settings import EMAIL_HOST_USER
from django.core.mail import EmailMessage
from .config import *
def verify_oneci_moov(file) : 
    empty_trx =[]
    field = [ "RefID","DATE","TYPE","S/D","CR","STATUS" ]
    for  count ,x in enumerate(file) :
        if field == list(x.keys()) :
            pass
        else :
            empty_trx.append(count)
    return empty_trx

def verify_ddva_visa(file) : 
    empty_trx =[]
    field = [ "Date et heure","ID du marchand","Montant","ID de requête","UUID de la transaction","Décision" ]
    for  count ,x in enumerate(file) :
        if field == list(x.keys()) :
            pass
        else :
            empty_trx.append(count)
    return empty_trx

def verify_orange_ci(file) : 
    empty_trx =[]
    field = [ "Date","Heure","Référence","Statut","Crédit" ,"Correspondant","Compte OM" ]
    for  count ,x in enumerate(file) :
        if field == list(x.keys()) :
            pass
        else :
            empty_trx.append(count)
    return empty_trx

def verify_mtn(file) : 
    empty_trx =[]
    field = ["ServiceProviderCode","TransactionId","MSISDN","SiteIDCP","IdTransactionCP","Amount","ResponseMessage","EndDateTime",]
    for  count ,x in enumerate(file) :
        if field == list(x.keys()) :
            pass
        else :
            empty_trx.append(count)
    return empty_trx

def get_field_from_config(config):
    field = []
    for item in list(config["index"].keys()):
        field.append(config["index"][item]["fileIndex"])
    return field

def verify_type_from_config(config):
    required_not_found = []
    for key, value in config["index"].items() :
        try :
            for item in TO_VERIFY[key]['required'] : # TO_VERIFY comes from config
                if item not in list(value.keys()) :
                    required_not_found.append(
                        {
                            "type":key,
                            "field_index":item
                        }
                    )
        except Exception as e :
            raise e

    return required_not_found


def verify_index_from_config(file, field):
    empty_trx = []
    for count,x in enumerate(file):
        for item in field :
            if item not in list(x.keys()) :
                print(list(x.keys()),field)
                empty_trx.append(count)
    for x in empty_trx :
        nbr = empty_trx.count(x)
        while nbr > 1 :
            empty_trx.remove(x)
            nbr = nbr-1
    return empty_trx


def Cinetpay_transaction_success(first,last,all_trx):
    success_trx = []  
    # create a function for this and use task_manager
    for trx in all_trx :
        trx_obj = trx.created_at
        # trx.cpm_payment_date = str(trx.cpm_payment_date).replace('+00:00','')             
        # trx_obj = datetime.strptime(str(trx.cpm_payment_date), '%Y-%m-%d %H:%M:%S')
        # print(trx.cpm_payment_date)
        # trx_obj = trx.cpm_paym    ent_date
        if trx_obj <= last and trx_obj >= first :
            success_trx.append(trx)
    print(len(success_trx))
    return success_trx


def Cinetpay_transaction_failed(first,last,all_trx):
    failed_trx = []  
    # create a function for this and use task_manager
    for trx in all_trx :
        # trx.created_at = str(trx.created_at).replace('+00:00','')          
        # trx_obj = datetime.strptime(str(trx.created_at), '%Y-%m-%d %H:%M:%S')
        trx_obj = trx.created_at
        # print(type(trx_obj))
        if trx_obj in (first,last) :
            failed_trx.append(trx)
    print(len(failed_trx))
    return failed_trx


def consult_trx(first,last,all_trx,operator):
    consult_trx = []     
    for trx in all_trx :
        trx.payment_date = str(trx.payment_date).replace('+00:00','')          
        trx_obj = datetime.strptime(str(trx.payment_date), '%Y-%m-%d %H:%M:%S')
        if trx_obj <= last and trx_obj >= first :
            consult_trx.append(trx)
    print(len(consult_trx))
    return list(consult_trx)



# Insertion of failed transactions from Cinetpay------------------------------------------------------------------------------
def insert_failed_trx(x,compte,agent,tache):
    b =TrxFailedCinetpay(created_at=x.created_at,cpm_payment_date=x.cpm_payment_date,marchand=x.marchand,EmailMarchand=x.EmailMarchand,
    NomDuService=x.NomDuService,cpm_trans_id=x.cpm_trans_id,
    cpm_site_id=x.cpm_site_id,cpm_amount=x.cpm_amount,payment_method=x.payment_method,
    cel_phone_num=x.cel_phone_num,cpm_trans_status=x.cpm_trans_status,cpm_payid=x.cpm_payid,account=compte,agent=agent,tache=tache)
    b.save()
    print('sauvé')
#-----------------------------------------------------------------------------------------------------------------------------


# Insertion of successfully transactions from Cinetpay------------------------------------------------------------------------
def insert_success_trx(x,compte,agent,tache):
    b =TrxSuccessCinetpay(created_at=x.created_at,cpm_payment_date=x.cpm_payment_date,marchand=x.marchand,EmailMarchand=x.EmailMarchand,
    NomDuService=x.NomDuService,cpm_trans_id=x.cpm_trans_id,
    cpm_site_id=x.cpm_site_id,cpm_amount=x.cpm_amount,payment_method=x.payment_method,
    cel_phone_num=x.cel_phone_num,cpm_trans_status=x.cpm_trans_status,cpm_payid=x.cpm_payid,account =compte,agent=agent,tache=tache)
    b.save()
    print('sauvé')
#-----------------------------------------------------------------------------------------------------------------------------

# Insertion of trx correspondent---------------------------------------------------------------------------------------------------------------
def insert_correspondent(x,compte,agent,tache):
    b =TrxCorrespondent(created_at=x.created_at,cpm_payment_date=x.cpm_payment_date,marchand=x.marchand,EmailMarchand=x.EmailMarchand,
    NomDuService=x.NomDuService,cpm_trans_id=x.cpm_trans_id,
    cpm_site_id=x.cpm_site_id,cpm_amount=x.cpm_amount,payment_method=x.payment_method,
    cel_phone_num=x.cel_phone_num,cpm_trans_status=x.cpm_trans_status,cpm_payid=x.cpm_payid,account=compte,agent=agent,tache=tache)
    b.save()
    print('sauvé')
#--------------------------------------------------------------------------------------------------------------------------------------------


# Insertion correspondent of each DDVA VISA transaction------------------------------------------------------------------------------------------------
def insert_finalCorrespondant_ddva_visa(x,t,compte,agent,tache):
    b =TrxRightCorrespodentDdvaVisa(payment_date =x.payment_date,payid=x.payid,status =x.status,phone_num=x.phone_num,amount = x.amount,
    created_atCorrespondent =t.created_at,AmountCorrespodent=t.cpm_amount,payment_methodCorrespondant=t.payment_method,
    cel_phone_numCorrespondant=t.cel_phone_num,StautTransactionCorrespondent=t.cpm_trans_status,cpm_trans_idCorrespondent = t.cpm_trans_id,cpm_customCorrespondent=t.cpm_custom,account =compte,agent=agent,tache=tache)
    b.save()
    print('sauvé')
#---------------------------------------------------------------------------------------------------------------------------------------------


# Insertion correspondent of each transaction------------------------------------------------------------------------------------------------
def insert_finalCorrespondant(x,t,compte,agent,tache):
    b =TrxRightCorrespodent(payment_date =x.payment_date,payid=x.payid,status =x.status,phone_num=x.phone_num,amount = x.amount,
    created_atCorrespondent =t.created_at,AmountCorrespodent=t.cpm_amount,payment_methodCorrespondant=t.payment_method,
    cel_phone_numCorrespondant=t.cel_phone_num,StautTransactionCorrespondent=t.cpm_trans_status,cpm_trans_idCorrespondent = t.cpm_trans_id,account =compte,agent=agent,tache=tache)
    b.save()
    print('sauvé')
#---------------------------------------------------------------------------------------------------------------------------------------------

# Insertion of DDVA VISA reconciled transaction------------------------------------------------------------------------------------------------
def insert_reconciled_trx_ddva_visa(x,tache):
    b =TrxreconciledDdvaVisa(payment_date =x.payment_date,payid=x.payid,status =x.status,trans_id=x.trans_id,amount = x.amount,
    created_atCorrespondent =x.created_atCorrespondent,AmountCorrespodent=x.AmountCorrespodent,payment_methodCorrespondant=x.payment_methodCorrespondant,
    cel_phone_numCorrespondant=x.cel_phone_numCorrespondant,StautTransactionCorrespondent=x.StautTransactionCorrespondent,cpm_trans_idCorrespondent = x.cpm_trans_idCorrespondent,account =x.account,agent=x.agent,tache=tache)
    b.save()
    print('sauvé')
#---------------------------------------------------------------------------------------------------------------------------------------------

# Insertion of  reconciled transaction------------------------------------------------------------------------------------------------
def insert_reconciled_trx(x,tache):
    b =Trxreconciled(payment_date =x.payment_date,payid=x.payid,status =x.status,phone_num=x.phone_num,amount = x.amount,
    created_atCorrespondent =x.created_atCorrespondent,AmountCorrespodent=x.AmountCorrespodent,payment_methodCorrespondant=x.payment_methodCorrespondant,
    cel_phone_numCorrespondant=x.cel_phone_numCorrespondant,StautTransactionCorrespondent=x.StautTransactionCorrespondent,cpm_trans_idCorrespondent = x.cpm_trans_idCorrespondent,account =x.account,agent=x.agent,tache=tache)
    b.save()
    print('sauvé')
#---------------------------------------------------------------------------------------------------------------------------------------------


#Detect each correspondant of Cinetpay failed transaction--------------------------------------------------------------------------------------
def detect_correspondent(compte,agent,tache):
    difference = TrxDifference.objects.all()
    for trx in difference : # select each element from difference
        corresp = TrxFailedCinetpay.objects.filter(cpm_amount=trx.amount,cel_phone_num=trx.phone_num) # select all his correspondent
        right_corresp = TrxFailedCinetpay.objects.filter(cpm_amount=trx.amount,cel_phone_num=trx.phone_num,created_at=trx.payment_date) # select transactions for which payment_date and creation are the same
        if len(right_corresp) != 0 : 
            for t in right_corresp : #insert those transactions in rightCorespondent table 
                print(trx.phone_num,trx.payment_date,trx.amount,"-->",t.cel_phone_num,t.created_at,t.cpm_amount,t.cpm_trans_id,"direct")
                insert_finalCorrespondant(trx,t,compte,agent,tache)
            TrxgetRightCorrenpondent = TrxRightCorrespodent.objects.all() # Select transactions having already their correspondents
            #And  Delete them from difference and TrxFailed table 
            for s in TrxgetRightCorrenpondent : 
                TrxFailedCinetpay.objects.filter(cel_phone_num=s.cel_phone_numCorrespondant,cpm_amount = s.AmountCorrespodent,account=compte,agent= agent).delete()
                TrxDifference.objects.filter(phone_num=s.phone_num,amount = s.amount,account=compte,agent= agent).delete()
        elif len(corresp) != 0 : # check if he has any correspondent
     
            for x in corresp : # if yes ,insert his correspondent 
                insert_correspondent(x,compte,agent,tache)
            final =get_closest_to(TrxCorrespondent, trx.payment_date,trx.amount,trx.phone_num) # select the closest from him through datepaiement and created_at 
            print(trx.phone_num,trx.payment_date,trx.amount,"-->",final.cel_phone_num,final.created_at,final.cpm_amount,final.cpm_trans_id)
            insert_finalCorrespondant(trx, final,compte,agent,tache)
            #And  Delete them from difference and TrxFailed table 
            TrxgetRightCorrenpondent = TrxRightCorrespodent.objects.all() # Select transactions having already their correspondents
            for s in TrxgetRightCorrenpondent : 
                TrxFailedCinetpay.objects.filter(cel_phone_num=s.cel_phone_numCorrespondant,cpm_amount = s.AmountCorrespodent,account= compte,agent=agent).delete()
                TrxDifference.objects.filter(phone_num=s.phone_num,amount = s.amount,account=compte,agent=agent).delete()
                TrxCorrespondent.objects.filter(cel_phone_num=s.cel_phone_numCorrespondant,cpm_amount = s.AmountCorrespodent,account= compte,agent=agent).delete()
        else :
            print(trx.phone_num,"doesn't have any correspondent")

                
#----------------------------------------------------------------------------------------------------------------------------------------------
   

#Detect each correspondant of Cinetpay failed transaction for DDVA VISA precisely--------------------------------------------------------------------------------------
def detect_correspondent_ddva_visa(compte,agent):
    difference = TrxDifferenceDdvaVisa.objects.all()
    for trx in difference : # select each element from difference
        corresp = TrxFailedCinetpay.objects.filter(cpm_amount=trx.amount,cpm_custom=trx.trans_id) # select  his correspondent
        if len(corresp) != 0 : 
            for t in corresp : #insert those transactions in rightCorespondent table 
                print(trx.trans_id,trx.payment_date,trx.amount,"-->",t.cpm_custom,t.created_at,t.cpm_amount,t.cpm_trans_id,"direct")
                insert_finalCorrespondant_ddva_visa(trx,t,compte,agent)
            TrxgetRightCorrenpondent = TrxRightCorrespodentDdvaVisa.objects.all() # Select transactions having already their correspondents
            #And  Delete them from difference and TrxFailed table 
            for s in TrxgetRightCorrenpondent : 
                TrxFailedCinetpay.objects.filter(cpm_custom=s.cpm_customCorrespondant,cpm_amount = s.AmountCorrespodent,account=compte,agent= agent).delete()
                TrxDifference.objects.filter(trans_id=s.trans_id,payid=s.payid,amount = s.amount,account=compte,agent= agent).delete()
        else :
            print(trx.trans_id,"doesn't have any correspondent")

                
#----------------------------------------------------------------------------------------------------------------------------------------------


# Find the closest transaction from the difference---------------------------------------------------------------------------------------------
def get_closest_to(self,target,amount,phone_num):
    closest_greater_qs = self.objects.filter(created_at__gt=target).order_by('created_at')
    closest_less_qs    = self.objects.filter(created_at__lt=target).order_by('-created_at')

    try:
        try:
            closest_greater = closest_greater_qs[0]
        except IndexError:
            return closest_less_qs[0]

        try:
            closest_less = closest_less_qs[0]
        except IndexError:
            return closest_greater_qs[0]
    except IndexError:
        raise self.objects.model.DoesNotExist("There is no closest object"
                                      " because there are no objects.")

    if closest_greater.created_at - target > target - closest_less.created_at:
        return closest_less
    else:
        return closest_greater
#----------------------------------------------------------------------------------------------------------------------------------------------


def file_treatment_orange_ci(file,debut,agent):
    for x in file :
        b = x['Date']
        s=x['Date'].replace(b,debut.split('T')[0])
        x['Date'] =" ".join([s,x['Heure']])
        serializer = TrxOperateurSerializer(data=x)
        insert_operator_trx(x,agent)

def file_treatment_mtnci(file,debut,agent):
    for x in file :
        x['MSISDN'] = str(x['MSISDN']).replace('225','')
        s =x['EndDateTime'].split('.')[0]
        b = s.split(' ')[0]
        x['EndDateTime'] = s.replace(b,debut.split('T')[0]) 
        print(x['EndDateTime'])
        serializer = TrxOperateurSerializer(data=x)
        insert_operator_mtn(x,agent)

def file_treatment_oneci_moov(file,agent):
    for x in file :
        x['DATE'] = x['DATE'].split('.')[0]
        x['S/D'] = str(x['S/D']).replace('225','')
        serializer = TrxOperateurSerializer(data=x)
        insert_oneci_moov_trx(x,agent)

def file_treatment_ddva_visa(file,debut,agent) :
    for x in file :
        b = x['Date et heure'].split(' ')[0]
        x['Date et heure']=x['Date et heure'].replace(b,debut.split('T')[0]).split(' +')[0]
        print(x['Date et heure'])
        serializer = TrxOperateurSerializer(data=x)
        insert_ddva_visa_trx(x,agent)


#transaction from operator and not from Cinetpay------------------------------------------------------------------------------
def match_table(compte,agent):
    difference = TrxOperateur.objects.filter(account = compte,agent=agent).exclude(payid__in=TrxSuccessCinetpay.objects.values_list('cpm_payid', flat=True))
    return difference
#-----------------------------------------------------------------------------------------------------------------------

#transaction from DDVA VISA and not from Cinetpay------------------------------------------------------------------------------
def match_table_ddva_visa():
    difference = TrxDdvaVisa.objects.exclude(payid__in=TrxSuccessCinetpay.objects.values_list('cpm_payid', flat=True))
    return difference
#-----------------------------------------------------------------------------------------------------------------------


# Insertion transaction from operator and not from Cinetpay (difference)------------------------------------------------------
def insert_difference(x,compte,agent,tache):
    b =TrxDifference(payment_date=x.payment_date, payid=x.payid,status=x.status,phone_num=x.phone_num,amount=x.amount,account = compte,agent = agent,tache=tache)
    b.save()
    print('sauvé')
#-----------------------------------------------------------------------------------------------------------------------------

# Insertion transaction from DDVA VISA and not from Cinetpay (difference)------------------------------------------------------
def insert_difference_ddva_visa(x,compte,agent,tache):
    b =TrxDifferenceDdvaVisa(payment_date=x.payment_date, payid=x.payid,status=x.status,trans_id=x.trans_id,amount=x.amount,account = compte,agent = agent,tache=tache)
    b.save()
    print('sauvé')
#-----------------------------------------------------------------------------------------------------------------------------


# Insertion transaction none reconciled------------------------------------------------------
def insert_none_reconciled_trx(x,tache):
    b =TrxNonereconciled(payment_date=x.payment_date, payid=x.payid,status=x.status,phone_num=x.phone_num,amount=x.amount,account = x.account,agent = x.agent,tache=tache)
    b.save()
    print('sauvé')
#-----------------------------------------------------------------------------------------------------------------------------

# Insertion DDVA VISA transaction none reconciled------------------------------------------------------
def insert_none_reconciled_trx_ddva_visa(x,tache):
    b =TrxNonereconciledDdvaVisa(payment_date=x.payment_date, payid=x.payid,status=x.status,trans_id=x.trans_id,amount=x.amount,account = x.compte,agent = x.agent,tache=tache)
    b.save()
    print('sauvé')
#-----------------------------------------------------------------------------------------------------------------------------


# Orange Operator insertion precisely------------------------------------------------------------------------------------------
def insert_operator_trx(x,agent):
    b =TrxOperateur(payment_date=x['Date'] , payid=x['Référence'],status=x['Statut'],phone_num=x['Correspondant'],amount=x['Crédit'],account=x['Compte OM'],agent = agent)
    b.save()
    print('sauvé---------------------')
#------------------------------------------------------------------------------------------------------------------------------

# MTNCI Operator insertion precisely------------------------------------------------------------------------------------------
def insert_operator_mtn(x,agent):
    b =TrxOperateur(payment_date=x['EndDateTime'] , payid=x['TransactionId'],status=x['ResponseMessage'],phone_num=x['MSISDN'],amount=x['Amount'],account=x['ServiceProviderCode'],agent = agent)
    b.save()
    print('sauvé---------------------')
#------------------------------------------------------------------------------------------------------------------------------

# ONECI_MOOV  insertion precisely------------------------------------------------------------------------------------------
def insert_oneci_moov_trx(x,agent):
    b =TrxOperateur(payment_date=x['DATE'] , payid=x['RefID'],status=x['STATUS'],phone_num=x['S/D'],amount=x['CR'],account=x['TYPE'],agent = agent)
    b.save()
    print('sauvé---------------------')
#------------------------------------------------------------------------------------------------------------------------------


# DDVA VISA insertion precisely------------------------------------------------------------------------------------------
def insert_ddva_visa_trx(x,agent):
    b =TrxDdvaVisa(payment_date=x['Date et heure'] , payid=x['ID de requête'],status=x['Décision'],trans_id=x['UUID de la transaction'],amount=x['Montant'],account=x['ID du marchand'],agent = agent)
    b.save()
    print('sauvé---------------------')
#------------------------------------------------------------------------------------------------------------------------------

class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening



""" FONCTIONS DE TRAITEMENT DES FICHIERS """


def treatment_msisdn(file, fileIndex, digit, indicative):
    for x in file :
        if len(str(x[fileIndex])) > digit :
            x[fileIndex] = str(x[fileIndex]).replace(str(indicative),"")


def treatment_date(file, fileIndex, format):
    for x in file :
        if format != "YYYY-mm-DD" :
            YY_indice = format.find("YYYY")
            len_yy = 0
            if YY_indice == -1 :
                YY_indice = format.find("YY")
                len_yy = 2
            else :
                len_yy = 4
            mm_indice = format.find("mm")
            DD_indice = format.find("DD")
            x[fileIndex] = "{}-{}-{}".format(x[fileIndex][YY_indice:YY_indice+len_yy], x[fileIndex][mm_indice:mm_indice+2], x[fileIndex][DD_indice:DD_indice+2])

def treatment_datetime(file, fileIndex, format):
    print(format)
    for x in file :
        if format != "YYYY-mm-DD HH:MM:SS" :
            YY_indice = format.find("YYYY")
            len_yy = 0
            if YY_indice == -1 :
                YY_indice = format.find("YY")
                len_yy = 2
            else :
                len_yy = 4
            mm_indice = format.find("mm")
            DD_indice = format.find("DD")
            HH_indice = format.find("HH")
            MM_indice = format.find("MM")
            SS_indice = format.find("SS")

            x[fileIndex] = "{}-{}-{} {}:{}:{}".format(x[fileIndex][YY_indice:YY_indice+len_yy], x[fileIndex][mm_indice:mm_indice+2], x[fileIndex][DD_indice:DD_indice+2], x[fileIndex][HH_indice:HH_indice+2], x[fileIndex][MM_indice:MM_indice+2], x[fileIndex][SS_indice:SS_indice+2])

def treatment_time(file, fileIndex, format):
    for x in file :
        if format != "HH:MM:SS":
            HH_indice = format.find("HH")
            MM_indice = format.find("MM")
            SS_indice = format.find("SS")

            x[fileIndex] = "{}:{}:{}".format(x[fileIndex][HH_indice:HH_indice+2], x[fileIndex][MM_indice:MM_indice+2], x[fileIndex][SS_indice:SS_indice+2])


def join_date_and_time(file, fileIndexDate, fileIndexTime):
    for x in file :
        x[fileIndexDate] = "{} {}".format(x[fileIndexDate], x[fileIndexTime])


def insert_operator(x, agent, index_, tache):
    try :
        b =TrxOperateur(payment_date=x[index_["index_date"]] , payid=x[index_["index_reference"]],status=x[index_["index_status"]],phone_num=x[index_["index_msisdn"]],amount=x[index_["index_amount"]],account=x[index_["index_account"]],agent = agent, tache=tache)
    except Exception as e:
        print(e)
        b =TrxOperateur(payment_date=x[index_["index_datetime"]] , payid=x[index_["index_reference"]],status=x[index_["index_status"]],phone_num=x[index_["index_msisdn"]],amount=x[index_["index_amount"]],account=x[index_["index_account"]],agent = agent, tache=tache)

    b.save()
    print('sauvé---------------------')



def save_file(file, agent, index_, tache) :
    for x in file :
        serializer = TrxOperateurSerializer(data=x)
        insert_operator(x,agent, index_, tache)
        print("sauvé")


def start_treatment(item,a) :
    a = {}
    try :
        a["payment_method"] = item["paymentMethod"]
    except KeyError :
        pass
    try :
        a["marchand"] = item["merchant"]
    except KeyError :
        pass
    try :
        a["NomDuService"] = item["serviceName"]
    except KeyError :
        pass

def second_treatment(failed_trx,success_trx,compte,agent,tache) :
    # insert failed transactions from Cinetay in DB----------
    for x in failed_trx :
        insert_failed_trx(x,compte,agent,tache)
    #---------------------------------------------------------
    # insert successfuly transactions from Cinetay in DB------
    for x in success_trx :
        insert_success_trx(x,compte,agent,tache)
    #---------------------------------------------------------

def third_treatment(agent,compte,tache) :
    countOperator= TrxOperateur.objects.filter(agent =agent ,account = compte,tache= tache).count()
    countCinetpay = TrxSuccessCinetpay.objects.filter(account= compte, agent=agent,tache= tache).count()
    diffCount = countOperator - countCinetpay
    operatorA = TrxOperateur.objects.filter(agent =agent ,account = compte,tache= tache)
    CinetpayA = TrxSuccessCinetpay.objects.filter(account= compte, agent=agent,tache= tache)
    operatorAmount = 0
    for t in operatorA :
        if t.amount != '-' :
            operatorAmount += int(t.amount.split('.')[0])
    print(operatorAmount)
    CinetpayAmount = 0
    for t in CinetpayA :
        if t.cpm_amount != '-' :
            CinetpayAmount += int(t.cpm_amount)
    print(CinetpayAmount)
    diffAmount = operatorAmount - CinetpayAmount
    TrxOperateur.objects.filter(account= compte,agent=agent,tache= tache ).delete()
    TrxSuccessCinetpay.objects.filter(account= compte,agent=agent,tache= tache).delete()
    TrxFailedCinetpay.objects.filter(account= compte,agent=agent,tache= tache).delete()
    TrxDifference.objects.filter(account= compte,agent=agent,tache= tache).delete()
    TrxCorrespondent.objects.filter(account= compte,agent=agent,tache= tache).delete()
    TrxRightCorrespodent.objects.filter(account= compte,agent=agent,tache= tache).delete()
    information = {
        'difference': 0,
        'montantOperateur':operatorAmount,
        'montantCinetpay':CinetpayAmount,
        'diffMontant':diffAmount,
        'countOperator':countOperator,
        'countCinetpay':countCinetpay,
        'diffCount':diffCount 
    }
    return information

def forth_treament(difference,compte,agent,tache):
    #insert trx in difference table
    for x in difference :
        insert_difference(x,compte,agent,tache)
    # Detect each correspondent of trx in difference
    detect_correspondent(compte,agent,tache)

    diff = TrxDifference.objects.filter(agent=agent,account = compte, tache = tache)
    diffSerialiser = TrxDifferenceSerializer(diff, many=True)
    countOperator= TrxOperateur.objects.filter(agent =agent ,account = compte, tache = tache).count()
    countCinetpay = TrxSuccessCinetpay.objects.filter(account= compte, agent=agent, tache = tache).count()
    diffCount = countOperator - countCinetpay
    operatorA = TrxOperateur.objects.filter(agent =agent ,account = compte, tache = tache)
    CinetpayA = TrxSuccessCinetpay.objects.filter(account= compte, agent=agent, tache = tache)
    operatorAmount = 0
    for t in operatorA :
        if t.amount != '-' :
            operatorAmount += int(t.amount.split('.')[0])
    print(operatorAmount)
    CinetpayAmount = 0
    for t in CinetpayA :
        if t.cpm_amount != '-' :
            CinetpayAmount += int(t.cpm_amount)
    print(CinetpayAmount)
    diffAmount = operatorAmount - CinetpayAmount
    # b = TrxCorrespondentSerializer(qs, many=True)
    
    qs = TrxRightCorrespodent.objects.filter(agent=agent,account = compte, tache = tache)
    serializer = TrxRightCorrespodentSerializer(qs, many=True)
    
    information = {
        'With correspondent': serializer.data, 
        'Not correspondent':diffSerialiser.data,
        'montantOperateur':operatorAmount,
        'montantCinetpay':CinetpayAmount,
        'diffMontant':diffAmount,
        'countOperator':countOperator,
        'countCinetpay':countCinetpay,
        'diffCount':diffCount 
    }
    print(json.dumps(information))
    return information


def send_email(user):
    email = EmailMessage('Le lien des transactions reconciliées', 'http://127.0.0.1:8000/reconciliation/','kouakounoeamani1@gmail.com',  to=['waltertacka@gmail.com'])
    email.send()
    print('ok')
    


def send_sms():
    r = requests.post('http://admin.smspro24.com/api/api_http.php', 
            data={
                'username' :'', 
                'password':'',
                'sender' : 22586446316,
                'text' : 'Recocnciliation termninée',
                'type' : 'text',
                 'to' : "0142662716"
            },
        )
    return Response(r.json)



def notification(user):
    try :
        send_email(user)
    except Exception as e:
        raise(e)
    try:    
        send_sms(user)
    except Exception :
        pass

def execute_reoncile(item,tache):
    headers = {
        'Authorization': 'Bearer JWNYIJmx6mqdkXbsWDhfpW6tulWYro',
        'Content-Type': 'application/json'
    }
    r=requests.post('http://localhost:8000/api_test/catered/',
        json = {
            'item':item,
            'id_tache':tache.pk,
        }, headers=headers
    )
    return Response(r.text)
