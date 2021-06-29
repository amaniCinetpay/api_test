from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from . import models
from .models import TrxOperateur, TrxCinetpay,TrxFailedCinetpay,TrxDifference,TrxCorrespondent,TrxRightCorrespodent
from django.core import serializers
import json
import time
from queue import Queue
from threading import Thread
import concurrent.futures
from datetime import datetime
from django.shortcuts import get_object_or_404
# # Operateur insertion------------------------------------------------------------------------------------------------------------------
# def insert_data(x):
#     b =TrxOperateur(datepaiment=x['Datepaiment'], idpaiment=x['idpaiment'],status=x['Statut'],telephone=x['telephone'],montant=x['Montant'])
#     b.save()
#     print('sauvé')
#------------------------------------------------------------------------------------------------------------------------------

# Orange Operator insertion precisely------------------------------------------------------------------------------------------
# def insert_data(x):
#     b =TrxOperateur(datepaiment=x['date'] +" "+ x['heure'], idpaiment=x['idpaiment'],status=x['status'],telephone=x['telephone'],montant=x['montant'])
#     b.save()
#     print('sauvé')
#------------------------------------------------------------------------------------------------------------------------------

# # Cinetpay--------------------------------------------------------------------------------------------------------------
# def insert_data(x):
#     b =TrxCinetpay(creation=x['CREATION'],datePaiement=x['DATE PAIEMENT'],marchand=x['MARCHAND'],EmailMarchand=x['EMAIL MARCHAND'],
#     NomDuService=x['NOM DU SERVICE'],IdTransaction=x['ID TRANSACTION'],
#     SiteId=x['SITE_ID'],Montant=x['MONTANT'],methodePaiment=x['METHODE PAIEMENT'],
#     Telephone=x['TELEPHONE'],EtatTransaction=x['ETAT TRANSACTION'],IdPaiment=x['ID PAIEMENT'])
#     b.save()
#     print('sauvé')
#--------------------------------------------------------------------------------------------------------------------------


# Insertion of failed transactions from Cinetpay------------------------------------------------------------------------------
# def insert_data(x):
#     b =TrxFailedCinetpay(creation=x.creation,datePaiement=x.datePaiement,marchand=x.marchand,EmailMarchand=x.EmailMarchand,
#     NomDuService=x.NomDuService,IdTransaction=x.IdTransaction,
#     SiteId=x.SiteId,Montant=x.Montant,methodePaiment=x.methodePaiment,
#     Telephone=x.Telephone,EtatTransaction=x.EtatTransaction,IdPaiment=x.IdPaiment)
#     b.save()
#     print('sauvé')
#-----------------------------------------------------------------------------------------------------------------------------


# Insertion of trx correspondent------------------------------------------------------------------------------
def insert_correspondent(x):
    b =TrxFailedCinetpay(creation=x.creation,datePaiement=x.datePaiement,marchand=x.marchand,EmailMarchand=x.EmailMarchand,
    NomDuService=x.NomDuService,IdTransaction=x.IdTransaction,
    SiteId=x.SiteId,Montant=x.Montant,methodePaiment=x.methodePaiment,
    Telephone=x.Telephone,EtatTransaction=x.EtatTransaction,IdPaiment=x.IdPaiment)
    b.save()
    print('sauvé')
#-----------------------------------------------------------------------------------------------------------------------------



# Insertion transaction from operator and not from Cinetpay (difference)------------------------------------------------------
# def insert_data(x):
#     b =TrxDifference(datepaiment=x.datepaiment, idpaiment=x.idpaiment,status=x.status,telephone=x.telephone,montant=x.montant)
#     b.save()
#     print('sauvé')
#-----------------------------------------------------------------------------------------------------------------------------


# # competitive approach-------------------------------------------------------------------------------------------- 
# def concurent_manager():
#     NUM_WORKERS = 20
#     start_time = time.time()
#     with concurrent.futures.ThreadPoolExecutor(max_workers = NUM_WORKERS) as executor :
#         futures = {executor.submit(insert_data(trx), trx) for trx in TRANSACTION_LIST}
#         concurrent.futures.wait(futures)
#     end_time = time.time()
#     print("Time for inserting : %ssecs" % (end_time-start_time) )
    
# TRANSACTION_LIST = []
# def reconcile(request):
    
#     if request.method == 'POST' :
#         transaction = request.POST['valeur']
#         trx = json.loads(transaction)
#         for x in trx :
#             TRANSACTION_LIST.append(x)

#     concurent_manager()
#     return render(request, 'reconcile/excel_to_json.html')

# -----------------------------------------------------------------------------------------------------------------




# Approach by task --------------------------------------------------------------------------------------------------
# def task_manager():

#     NUM_WORKERS = 1
#     task_queue = Queue()
#     def worker ():
#         while True :
#             data = task_queue.get()
#             insert_data(data)

#             task_queue.task_done()
#     start_time = time.time()
#     threads = [Thread(target=worker) for _ in range(NUM_WORKERS)]

#     [task_queue.put(item) for item in TRANSACTION_LIST]

#     [thread.start() for thread in threads]

#     task_queue.join()

#     end_time = time.time()
#     print("Time for inserting : %ssecs" % (end_time-start_time) )
#--------------------------------------------------------------------------------------------------------------------


#transaction from operator and not from Cinetpay------------------------------------------------------------------------
def match_table():
    difference = TrxOperateur.objects.exclude(idpaiment__in=TrxCinetpay.objects.values_list('IdPaiment', flat=True))
    print(len(difference))
    return difference
#-----------------------------------------------------------------------------------------------------------------------

def compare_date(first,second):
    # zero_obj = datetime.strptime('first', '%Y-%m-%d %H:%M:%S')
    # print(type(first))
    # print(type(second))
    # diff = first - second
    # print(diff)
    if (first <= second):
        return True
    else :
        return False



# #ONECI MTNCI-------------------------------------------------------------------------------------------------------------
# def Cinetpay_transaction_success(first,last):
#     success_trx = []  
#     all_trx = TrxCinetpay.objects.all()
#     # create a function for this and use task_manager
#     for trx in all_trx :
#         if trx.datePaiement != "null" and trx.IdPaiment !="null" and trx.methodePaiment=="MOMO" and trx.marchand =="ONECI - RNPP" and trx.NomDuService=="ONECI":            
#             trx_obj = datetime.strptime(trx.datePaiement, '%Y-%m-%d %H:%M:%S')
#             if trx_obj <= last and trx_obj >= first :
#                 success_trx.append(trx)
#     print(len(success_trx))
#     return success_trx
# #---------------------------------------------------------------------------------------------------------------------


# #ONECI MTNCI-------------------------------------------------------------------------------------------------------------
# def Cinetpay_transaction_failed(first,last):
#     failed_trx = []  
#     all_trx = TrxCinetpay.objects.all()
#     # create a function for this and use task_manager
#     for trx in all_trx :
#         if trx.EtatTransaction != "Successfully Processed Transaction" and trx.methodePaiment=="MOMO" and trx.marchand =="ONECI - RNPP" and trx.NomDuService=="ONECI":            
#             trx_obj = datetime.strptime(trx.datePaiement, '%Y-%m-%d %H:%M:%S')
#             if trx_obj <= last and trx_obj >= first :
#                 failed_trx.append(trx)
#     print(len(failed_trx))
#     return failed_trx
# #----------------------------------------------------------------------------------------------------------------------



#DDVA MTNCI-------------------------------------------------------------------------------------------------------------
# def Cinetpay_transaction_success(first,last):
#     success_trx = []  
#     all_trx = TrxCinetpay.objects.all()
#     # create a function for this and use task_manager
#     for trx in all_trx :
#             if trx.EtatTransaction=="SUCCES" and trx.methodePaiment=="DDVAMTNCI" and trx.marchand =="DDVA" :            
#                 trx_obj = datetime.strptime(trx.datePaiement, '%Y-%m-%d %H:%M:%S')
#                 if trx_obj <= last and trx_obj >= first :
#                     success_trx.append(trx)
#     print(len(success_trx))
#     return success_trx
#---------------------------------------------------------------------------------------------------------------------


#DDVA MTNCI-------------------------------------------------------------------------------------------------------------
# def Cinetpay_transaction_failed(first,last):
#     failed_trx = []  
#     all_trx = TrxCinetpay.objects.all()
#     # create a function for this and use task_manager
#     for trx in all_trx :
#         if trx.EtatTransaction != "SUCCES" and trx.methodePaiment=="DDVAMTNCI" and trx.marchand =="DDVA":
#             trx.creation = str(trx.creation).replace('+00:00','')          
#             trx_obj = datetime.strptime(str(trx.creation), '%Y-%m-%d %H:%M:%S')
#             if trx_obj <= last and trx_obj >= first :
#                 failed_trx.append(trx)
#     print(len(failed_trx))
#     return failed_trx
#----------------------------------------------------------------------------------------------------------------------

#DDVA ORANGE CI-------------------------------------------------------------------------------------------------------------
# def Cinetpay_transaction_success(first,last):
#     success_trx = []  
#     all_trx = TrxCinetpay.objects.all()
#     # create a function for this and use task_manager
#     for trx in all_trx :
#             if trx.EtatTransaction=="SUCCES" and trx.methodePaiment=="DDVAOMCI" and trx.marchand =="DDVA" :            
#                 trx_obj = datetime.strptime(trx.datePaiement, '%Y-%m-%d %H:%M:%S')
#                 if trx_obj <= last and trx_obj >= first :
#                     success_trx.append(trx)
#     print(len(success_trx))
#     return success_trx
#---------------------------------------------------------------------------------------------------------------------


#DDVA ORANGE CI-------------------------------------------------------------------------------------------------------------
# def Cinetpay_transaction_failed(first,last):
#     failed_trx = []  
#     all_trx = TrxCinetpay.objects.all()
#     # create a function for this and use task_manager
#     for trx in all_trx :
#         if trx.EtatTransaction != "SUCCES" and trx.methodePaiment=="DDVAOMCI" and trx.marchand =="DDVA":
#             trx.creation = str(trx.creation).replace('+00:00','')          
#             trx_obj = datetime.strptime(str(trx.creation), '%Y-%m-%d %H:%M:%S')
#             if trx_obj <= last and trx_obj >= first :
#                 failed_trx.append(trx)
#     print(len(failed_trx))
#     return failed_trx
#----------------------------------------------------------------------------------------------------------------------


# this method is on the model's manager
def get_closest_to(self,target):
    closest_greater_qs = self.objects.filter(creation__gt=target).order_by('creation')
    closest_less_qs    = self.objects.filter(creation__lt=target).order_by('-creation')

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

    if closest_greater.creation - target > target - closest_less.creation:
        return closest_less
    else:
        return closest_greater


def get_closest_to_dt(qs, dt):
    greater = qs.objects.filter(creation__gt=dt).order_by("creation").first()
    less = qs.objects.filter(creation__gt=dt).order_by("-creation").first()

    if greater and less:
        return greater if abs(greater.creation - dt) < abs(less.creation - dt) else less
    else:
        return greater or less



# Insertion correspondent of each transaction------------------------------------------------------------------------------
def insert_data(x,t):
    b =TrxRightCorrespodent(datePaiement =x.datepaiment,status =x.status,telephone=x.telephone,montant = x.montant,
    creationCorrespondent =t.creation,AmountCorrespodent=t.Montant,methodePaimentCorrespondant=t.methodePaiment,
    TelephoneCorrespondant=t.Telephone,StautTransactionCorrespondent=t.EtatTransaction)
    b.save()
    print('sauvé')
#-----------------------------------------------------------------------------------------------------------------------------


#Detect each correspondant of Cinetpay failed transaction--------------------------------------------------------------
def detect_correspondent():
    difference = TrxDifference.objects.all()
    for trx in difference :
        corresp = TrxFailedCinetpay.objects.filter(Montant=trx.montant,Telephone=trx.telephone)
        right_corresp = TrxFailedCinetpay.objects.filter(Montant=trx.montant,Telephone=trx.telephone,creation=trx.datepaiment) 
        # insert transaction for which datePaiment and creation are the same
        for t in right_corresp :
            print(trx.telephone,trx.datepaiment,trx.montant,"-->",t.Telephone,t.creation,t.Montant)
            insert_data(trx,t)
        TrxgetRightCorrenpondent = TrxRightCorrespodent.objects.all()
        # Delete trx from failedTransaction anf from difference because she has now her correspondent
        for s in TrxgetRightCorrenpondent : 
            TrxFailedCinetpay.objects.filter(Telephone=s.TelephoneCorrespondant,Montant = s.AmountCorrespodent).delete()
            TrxDifference.objects.filter(telephone=s.telephone,montant = s.montant).delete()
        if len(corresp) != 0 :
            for x in corresp :
                insert_correspondent(x)
            final =get_closest_to(TrxCorrespondent, trx.datepaiment)
            if final :
                print(trx.telephone,trx.datepaiment,trx.montant,"-->",final.Telephone,final.creation,final.Montant)
            TrxCorrespondent.objects.all().delete()
        else :
            print("no correspondent")
        # final =get_closest_to(TrxFailedCinetpay, trx.datepaiment,trx.montant,trx.telephone)
        # final = get_closest_to_dt(TrxFailedCinetpay, trx.datepaiment,trx.montant,trx.telephone)
                    
#-----------------------------------------------------------------------------------------------------------------------
   

       

TRANSACTION_LIST = []
def reconcile(request):
    if request.method == 'POST' :
        # transaction = request.POST['valeur']
        # trx = json.loads(transaction)
        # for x in trx :
        #     x['telephone'] = str(x['telephone']).replace('225','')
        #     x['Datepaiment'] = x['Datepaiment'].replace('04/05/2021 ','2021-05-04')
        #     print(x['telephone'],x['Datepaiment'])
        #     # TRANSACTION_LIST.append(x)
        #     insert_data(x)


        #DDVA Orange file treatment--------------------------------------------------------------------------------------------
        # transaction = request.POST['valeur']
        # trx = json.loads(transaction)
        # for x in trx :
        #     x['date'] = x['date'].replace('04/05/2021','2021-05-04')
        #     insert_data(x)
        #------------------------------------------------------------------------------------------------------------

        # Recover success/failed/difference transactions from operator and insert-----------------------------------------------------------------
        # debut = request.POST['debut']
        # fin = request.POST['fin']
        # debut_obj = datetime.strptime(debut, "%Y-%m-%dT%H:%M")
        # fin_obj = datetime.strptime(fin, "%Y-%m-%dT%H:%M")
        # print(type(fin_obj))
        #--------insert failed trx ----------------------------------------------------------------
        # failed_trx = Cinetpay_transaction_failed(debut_obj,fin_obj)
        # print(type(failed_trx))
        # for x in failed_trx :
        #     insert_data(x)
        #------------------------------------------------------------------------------------------

        #--------insert successfuly trx -----------------------------------------------------------
        # success_trx = Cinetpay_transaction_success(debut_obj,fin_obj)
        # for x in success_trx :
        #     insert_data(x)
        # -----------------------------------------------------------------------------------------
        detect_correspondent()
        #--------insert differnce trx -----------------------------------------------------------
        # difference = match_table()
        # for x in difference :
        #     insert_data(x)
        # -----------------------------------------------------------------------------------------

    return render(request, 'reconcile/excel_to_json.html')
# ----------------------------------------------------------------------------------------------------------------------



# Approche serielle-----------------------------------------------------------------------------------------------------
# def reconcile(request):
#     TRANSACTION_LIST = []

#     if request.method == 'POST':
#         data = request.POST['valeur']
#         dat = json.loads(data)
#         start_time = time.time()
#         for x in dat :
#             b =TrxOperateur(date=x['date'],reference=x['reference'],operation=x['operation'],status=x['statut'],mode=x['mode'],CompteOM=x['compteOm'],correspondant=x['correspondant'],credit=x['credit'])
#             b.save()
#             print('sauvé')
        
#         end_time = time.time()
#         print("Time for inserting : %ssecs" % (end_time-start_time) )

        
#     return render(request, 'reconcile/excel_to_json.html')

# -----------------------------------------------------------------------------------------------------------------------

def update_transaction():
    pass



def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def excel_to_json(request):
    return render(request, 'reconcile/excel_to_json.html')

