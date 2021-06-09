from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from . import models
from .models import TrxOperateur, TrxCinetpay,TrxFailedCinetpay,TrxDifference,TrxCorrespondent,TrxDifference,TrxCorrespondent,TrxRightCorrespodent,TrxSuccessCinetpay
from django.core import serializers
import json
import time
from queue import Empty, Queue
from threading import Thread
import concurrent.futures
from datetime import datetime
from django.db.models import Sum,Avg


# # Operator insertion-------------------------------------------------------------------------------------------------------------------------
# def insert_data(x):
#     b =TrxOperateur(datepaiment=x['Datepaiment'], idpaiment=x['idpaiment'],status=x['Statut'],telephone=x['telephone'],montant=x['Montant'])
#     b.save()
#     print('sauvé')
#----------------------------------------------------------------------------------------------------------------------------------------------

# Orange Operator insertion precisely----------------------------------------------------------------------------------------------------------
# def insert_data(x):
#     b =TrxOperateur(datepaiment=x['date'] +" "+ x['heure'], idpaiment=x['idpaiment'],status=x['status'],telephone=x['telephone'],montant=x['montant'])
#     b.save()
#     print('sauvé')
#----------------------------------------------------------------------------------------------------------------------------------------------

# # Cinetpay-----------------------------------------------------------------------------------------------------------------------------------
def insert_data(x):
    b =TrxCinetpay(creation=x['CREATION'],datePaiement=x['DATE PAIEMENT'],marchand=x['MARCHAND'],
    NomDuService=x['NOM DU SERVICE'],IdTransaction=x['ID TRANSACTION'],
    SiteId=x['SITE_ID'],Montant=x['MONTANT'],methodePaiment=x['METHODE PAIEMENT'],
    Telephone=x['TELEPHONE'],EtatTransaction=x['ETAT TRANSACTION'],IdPaiment=x['ID PAIEMENT'])
    b.save()
    print('sauvé')
#----------------------------------------------------------------------------------------------------------------------------------------------


# Insertion of failed transactions from Cinetpay-----------------------------------------------------------------------------------------------
# def insert_data(x):
#     b =TrxFailedCinetpay(creation=x.creation,datePaiement=x.datePaiement,marchand=x.marchand,EmailMarchand=x.EmailMarchand,
#     NomDuService=x.NomDuService,IdTransaction=x.IdTransaction,
#     SiteId=x.SiteId,Montant=x.Montant,methodePaiment=x.methodePaiment,
#     Telephone=x.Telephone,EtatTransaction=x.EtatTransaction,IdPaiment=x.IdPaiment)
#     b.save()
#     print('sauvé')
#----------------------------------------------------------------------------------------------------------------------------------------------

# Insertion of trx correspondent---------------------------------------------------------------------------------------------------------------
def insert_correspondent(x):
    b =TrxCorrespondent(creation=x.creation,datePaiement=x.datePaiement,marchand=x.marchand,EmailMarchand=x.EmailMarchand,
    NomDuService=x.NomDuService,IdTransaction=x.IdTransaction,
    SiteId=x.SiteId,Montant=x.Montant,methodePaiment=x.methodePaiment,
    Telephone=x.Telephone,EtatTransaction=x.EtatTransaction,IdPaiment=x.IdPaiment)
    b.save()
    print('sauvé')
#--------------------------------------------------------------------------------------------------------------------------------------------

# Insertion correspondent of each transaction------------------------------------------------------------------------------------------------
def insert_finalCorrespondant(x,t):
    b =TrxRightCorrespodent(datePaiement =x.datepaiment,idpaiment=x.idpaiment,status =x.status,telephone=x.telephone,montant = x.montant,
    creationCorrespondent =t.creation,AmountCorrespodent=t.Montant,methodePaimentCorrespondant=t.methodePaiment,
    TelephoneCorrespondant=t.Telephone,StautTransactionCorrespondent=t.EtatTransaction,IdTransactionCorrespondent = t.IdTransaction)
    b.save()
    print('sauvé')
#---------------------------------------------------------------------------------------------------------------------------------------------

# Insertion transaction from operator and not from Cinetpay (difference)----------------------------------------------------------------------
# def insert_data(x):
#     b =TrxDifference(datepaiment=x.datepaiment, idpaiment=x.idpaiment,status=x.status,telephone=x.telephone,montant=x.montant)
#     b.save()
#     print('sauvé')
#---------------------------------------------------------------------------------------------------------------------------------------------


# # competitive approach-----------------------------------------------------------------------------------------------------------------------
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

# ---------------------------------------------------------------------------------------------------------------------------------------------




# Approach by task ----------------------------------------------------------------------------------------------------------------------------
def task_manager():

    NUM_WORKERS = 2
    task_queue = Queue()
    def worker ():
        while True :
            data = task_queue.get()
            insert_data(data)

            task_queue.task_done()
    start_time = time.time()
    threads = [Thread(target=worker) for _ in range(NUM_WORKERS)]

    [task_queue.put(item) for item in TRANSACTION_LIST]

    [thread.start() for thread in threads]

    task_queue.join()

    end_time = time.time()
    print("Time for inserting : %ssecs" % (end_time-start_time) )
#---------------------------------------------------------------------------------------------------------------------------------------------


#transaction from operator and not from Cinetpay----------------------------------------------------------------------------------------------
# def match_table():
#     difference = TrxOperateur.objects.exclude(idpaiment__in=TrxCinetpay.objects.values_list('IdPaiment', flat=True))
#     print(len(difference))
#     return difference
#     # for x in ecart :
#     #     print(x)
#     # detect_correspondent(ecart)
#----------------------------------------------------------------------------------------------------------------------------------------------

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



# #ONECI MTNCI---------------------------------------------------------------------------------------------------------------------------------
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
# ---------------------------------------------------------------------------------------------------------------------------------------------


# #ONECI MTNCI---------------------------------------------------------------------------------------------------------------------------------
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
# --------------------------------------------------------------------------------------------------------------------------------------------



#DDVA MTNCI------------------------------------------------------------------------------------------------------------------------------------
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
#----------------------------------------------------------------------------------------------------------------------------------------------


#DDVA MTNCI------------------------------------------------------------------------------------------------------------------------------------
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
#----------------------------------------------------------------------------------------------------------------------------------------------

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
#----------------------------------------------------------------------------------------------------------------------------------------------


# Find the closest transaction from the difference---------------------------------------------------------------------------------------------
def get_closest_to(self,target,montant,telephone):
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
#----------------------------------------------------------------------------------------------------------------------------------------------

# def get_closest_to_dt(qs, dt,montant,telephone):
#     greater = qs.objects.filter(creation__gt=dt,Montant=montant,Telephone=telephone).order_by("creation").first()
#     less = qs.objects.filter(creation__gt=dt,Montant=montant,Telephone=telephone).order_by("-creation").first()

#     if greater and less:
#         return greater if abs(greater.creation - dt) < abs(less.creation - dt) else less
#     else:
#         return greater or less





#Detect each correspondant of Cinetpay failed transaction--------------------------------------------------------------------------------------
def detect_correspondent():
    difference = TrxDifference.objects.all()
    for trx in difference : # select each element from difference
        corresp = TrxFailedCinetpay.objects.filter(Montant=trx.montant,Telephone=trx.telephone) # select all his correspondent
        right_corresp = TrxFailedCinetpay.objects.filter(Montant=trx.montant,Telephone=trx.telephone,creation=trx.datepaiment) # select transactions for which datePaiment and creation are the same
        if len(right_corresp) != 0 : 
            for t in right_corresp : #insert those transactions in rightCorespondent table 
                print(trx.telephone,trx.datepaiment,trx.montant,"-->",t.Telephone,t.creation,t.Montant,t.IdTransaction,"direct")
                insert_finalCorrespondant(trx,t)
            TrxgetRightCorrenpondent = TrxRightCorrespodent.objects.all() # Select transactions having already their correspondents
            #And  Delete them from difference and TrxFailed table 
            for s in TrxgetRightCorrenpondent : 
                TrxFailedCinetpay.objects.filter(Telephone=s.TelephoneCorrespondant,Montant = s.AmountCorrespodent).delete()
                TrxDifference.objects.filter(telephone=s.telephone,montant = s.montant).delete()
        else :
            if len(corresp) != 0 : # check if he has any correspondent
                for x in corresp : # if yes ,insert his correspondent 
                    insert_correspondent(x)
                final =get_closest_to(TrxCorrespondent, trx.datepaiment,trx.montant,trx.telephone) # select the closest from him through datepaiement and creation 
                print(trx.telephone,trx.datepaiment,trx.montant,"-->",final.Telephone,final.creation,final.Montant,final.IdTransaction)
                insert_finalCorrespondant(trx, final)
                #And  Delete them from difference and TrxFailed table 
                TrxgetRightCorrenpondent = TrxRightCorrespodent.objects.all() # Select transactions having already their correspondents
                for s in TrxgetRightCorrenpondent : 
                    TrxFailedCinetpay.objects.filter(Telephone=s.TelephoneCorrespondant,Montant = s.AmountCorrespodent).delete()
                    TrxDifference.objects.filter(telephone=s.telephone,montant = s.montant).delete()
            else :
                print(trx.telephone,"doesn't have any correspondent")
                
#----------------------------------------------------------------------------------------------------------------------------------------------
   



def update_transaction(request):
    if request.method == "POST" :
        print('mettre à jour')
    # correspondent = TrxRightCorrespodent.objects.all()
    # for trx in correspondent :
    #     TrxCinetpay.objects.filter(Telephone=trx.TelephoneCorrespondant,Montant=trx.AmountCorrespodent,IdTransaction=trx.IdTransactionCorrespondent).update(IdPaiment=trx.idpaiment,EtatTransaction="SUCCES")
    





# TRANSACTION_LIST = []
# def reconcile(request):
#     if request.method == 'POST' : 
#         start_time = time.time()
#         transaction = request.POST['valeur']
#         operateur = request.POST.getlist('operateur')[0]
      
#         trx = json.loads(transaction)
#         for x in trx :
#             x['TELEPHONE'] = str(x['TELEPHONE']).replace('225','')
#             x['CREATION'] = x['CREATION'].replace('06/05/2021 ','2021-05-06')
#             x['DATE PAIEMENT'] = x['DATE PAIEMENT'].replace('06/05/2021 ','2021-05-06')
#             print(x['TELEPHONE'],x['CREATION'],x['DATE PAIEMENT'] )
#             TRANSACTION_LIST.append(x)
#             insert_data(x)
#         end_time = time.time()
#         print("Time for inserting : %ssecs" % (end_time-start_time) )


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
        # detect_correspondent()
        #--------insert differnce trx -----------------------------------------------------------
        # difference = match_table()
        # for x in difference :
        #     insert_data(x)
        # -----------------------------------------------------------------------------------------

    # return render(request, 'reconcile/excel_to_json.html')
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

        
    # return render(request, 'reconcile/excel_to_json.html')

# -----------------------------------------------------------------------------------------------------------------------



def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def excel_to_json(request):
    return render(request, 'reconcile/excel_to_json.html')



























































#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#                                        work  properly                                                               +
#                                                                                                                     +
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++




#DDVA MTNCI ********************************************************************************************************************************

# # Operator insertion-------------------------------------------------------------------------------------------------
# def insert_operator_trx(x):
#     b =TrxOperateur(datepaiment=x['Datepaiment'], idpaiment=x['idpaiment'],status=x['Statut'],telephone=x['telephone'],montant=x['Montant'])
#     b.save()
#     print('sauvé')
# # #------------------------------------------------------------------------------------------------------------------------------



# # #DDVA MTNCI CI-------------------------------------------------------------------------------------------------------------
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
# # #---------------------------------------------------------------------------------------------------------------------


# # #DDVA MTNCI CI-------------------------------------------------------------------------------------------------------------
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
# # #----------------------------------------------------------------------------------------------------------------------

# # # Insertion of failed transactions from Cinetpay------------------------------------------------------------------------------
# def insert_failed_trx(x):
#     b =TrxFailedCinetpay(creation=x.creation,datePaiement=x.datePaiement,marchand=x.marchand,EmailMarchand=x.EmailMarchand,
#     NomDuService=x.NomDuService,IdTransaction=x.IdTransaction,
#     SiteId=x.SiteId,Montant=x.Montant,methodePaiment=x.methodePaiment,
#     Telephone=x.Telephone,EtatTransaction=x.EtatTransaction,IdPaiment=x.IdPaiment)
#     b.save()
#     print('sauvé')
# # #-----------------------------------------------------------------------------------------------------------------------------

# # # Insertion of successfully transactions from Cinetpay------------------------------------------------------------------------------
# def insert_success_trx(x):
#     b =TrxSuccessCinetpay(creation=x.creation,datePaiement=x.datePaiement,marchand=x.marchand,EmailMarchand=x.EmailMarchand,
#     NomDuService=x.NomDuService,IdTransaction=x.IdTransaction,
#     SiteId=x.SiteId,Montant=x.Montant,methodePaiment=x.methodePaiment,
#     Telephone=x.Telephone,EtatTransaction=x.EtatTransaction,IdPaiment=x.IdPaiment)
#     b.save()
#     print('sauvé')
# # #-----------------------------------------------------------------------------------------------------------------------------

# # #transaction from operator and not from Cinetpay------------------------------------------------------------------------
# def match_table():
#     difference = TrxOperateur.objects.exclude(idpaiment__in=TrxSuccessCinetpay.objects.values_list('IdPaiment', flat=True))
#     return difference
# # #-----------------------------------------------------------------------------------------------------------------------

# # # Insertion transaction from operator and not from Cinetpay (difference)------------------------------------------------------
# def insert_difference(x):
#     b =TrxDifference(datepaiment=x.datepaiment, idpaiment=x.idpaiment,status=x.status,telephone=x.telephone,montant=x.montant)
#     b.save()
#     print('sauvé')
# # #-----------------------------------------------------------------------------------------------------------------------------



# TRANSACTION_LIST = []
# def reconcile(request):
#     if request.method == 'POST' :
#         start_time = time.time()
#         transaction = request.POST['valeur']
#         trx = json.loads(transaction)
#         debut = request.POST['debut']
#         fin = request.POST['fin']
#         debut_obj = datetime.strptime(debut, "%Y-%m-%dT%H:%M")
#         fin_obj = datetime.strptime(fin, "%Y-%m-%dT%H:%M")
#         #insert trx in operator table
#         b = debut.split('T')[0]
#         for x in trx :
#             x['telephone'] = str(x['telephone']).replace('225','')
#             s = x['Datepaiment'].split('  ')[1]
#             x['Datepaiment'] = " ".join([b,s])
#             print(x['Datepaiment'])
#             insert_operator_trx(x)
 
#         failed_trx = Cinetpay_transaction_failed(debut_obj,fin_obj)  # recover failed transactions from Cinetay
#         success_trx = Cinetpay_transaction_success(debut_obj, fin_obj)  # recover successfuly transactions from Cinetay
#         # insert failed transactions from Cinetay in DB----------
#         for x in failed_trx :
#             insert_failed_trx(x)
#         #---------------------------------------------------------
#         # insert successfuly transactions from Cinetay in DB------
#         for x in success_trx :
#             insert_success_trx(x)
#         #---------------------------------------------------------

#         difference = match_table() #match operator trx and CinetpaySucessfuly trx and return difference
#         #insert trx in difference table
#         for x in difference :
#             insert_difference(x)
#         # Detect each correspondent of trx in difference
#         detect_correspondent()
#         end_time = time.time()
#         print("Time for reconciling : %ssecs" % (end_time-start_time) )
        
#     return render(request, 'reconcile/excel_to_json.html')

#DDVA MTNCI ********************************************************************************************************************************







#ONECI MTNCI ********************************************************************************************************************************

# # # Operator insertion-------------------------------------------------------------------------------------------------
# def insert_operator_trx(x):
#     b =TrxOperateur(datepaiment=x['EndDateTime'], idpaiment=x['idpaiment'],status=x['ResponseMessage'],telephone=x['telephone'],montant=x['Amount'])
#     b.save()
#     print('sauvé')
# # # #------------------------------------------------------------------------------------------------------------------------------



# # ONECI MTNCI CI-------------------------------------------------------------------------------------------------------------
# def Cinetpay_transaction_success(first,last):
#     success_trx = []  
#     all_trx = TrxCinetpay.objects.all()
#     # create a function for this and use task_manager
#     for trx in all_trx :
#         if trx.EtatTransaction == "SUCCES"  and trx.methodePaiment=="MOMO" and trx.marchand =="ONECI - RNPP" and trx.NomDuService=="ONECI":            
#             trx_obj = datetime.strptime(trx.datePaiement, '%Y-%m-%d %H:%M:%S')
#             if trx_obj <= last and trx_obj >= first :
#                 success_trx.append(trx)
#     print(len(success_trx))
#     return success_trx
# # # #---------------------------------------------------------------------------------------------------------------------


# # # #ONECI MTNCI CI-------------------------------------------------------------------------------------------------------------
# def Cinetpay_transaction_failed(first,last):
#     failed_trx = []  
#     all_trx = TrxCinetpay.objects.all()
#     # create a function for this and use task_manager
#     for trx in all_trx :
#         if trx.EtatTransaction != "SUCCES" and trx.methodePaiment=="MOMO" and trx.marchand =="ONECI - RNPP" and trx.NomDuService=="ONECI":            
#             trx.creation = str(trx.creation).replace('+00:00','')          
#             trx_obj = datetime.strptime(str(trx.creation), '%Y-%m-%d %H:%M:%S')
#             if trx_obj <= last and trx_obj >= first :
#                 failed_trx.append(trx)
#     print(len(failed_trx))
#     return failed_trx
# # # #----------------------------------------------------------------------------------------------------------------------

# # # # Insertion of failed transactions from Cinetpay------------------------------------------------------------------------------
# def insert_failed_trx(x):
#     b =TrxFailedCinetpay(creation=x.creation,datePaiement=x.datePaiement,marchand=x.marchand,EmailMarchand=x.EmailMarchand,
#     NomDuService=x.NomDuService,IdTransaction=x.IdTransaction,
#     SiteId=x.SiteId,Montant=x.Montant,methodePaiment=x.methodePaiment,
#     Telephone=x.Telephone,EtatTransaction=x.EtatTransaction,IdPaiment=x.IdPaiment)
#     b.save()
#     print('sauvé')
# # # #-----------------------------------------------------------------------------------------------------------------------------

# # # # Insertion of successfully transactions from Cinetpay------------------------------------------------------------------------------
# def insert_success_trx(x):
#     b =TrxSuccessCinetpay(creation=x.creation,datePaiement=x.datePaiement,marchand=x.marchand,EmailMarchand=x.EmailMarchand,
#     NomDuService=x.NomDuService,IdTransaction=x.IdTransaction,
#     SiteId=x.SiteId,Montant=x.Montant,methodePaiment=x.methodePaiment,
#     Telephone=x.Telephone,EtatTransaction=x.EtatTransaction,IdPaiment=x.IdPaiment)
#     b.save()
#     print('sauvé')
# # # #-----------------------------------------------------------------------------------------------------------------------------

# # # #transaction from operator and not from Cinetpay------------------------------------------------------------------------
# def match_table():
#     difference = TrxOperateur.objects.exclude(idpaiment__in=TrxSuccessCinetpay.objects.values_list('IdPaiment', flat=True))
#     return difference
# # # #-----------------------------------------------------------------------------------------------------------------------

# # # # Insertion transaction from operator and not from Cinetpay (difference)------------------------------------------------------
# def insert_difference(x):
#     b =TrxDifference(datepaiment=x.datepaiment, idpaiment=x.idpaiment,status=x.status,telephone=x.telephone,montant=x.montant)
#     b.save()
#     print('sauvé')
# # # #-----------------------------------------------------------------------------------------------------------------------------



# # TRANSACTION_LIST = []
# def reconcile(request):
#     if request.method == 'POST' :
#         start_time = time.time()
#         transaction = request.POST['valeur']
#         trx = json.loads(transaction)
#         debut = request.POST['debut']
#         fin = request.POST['fin']
#         debut_obj = datetime.strptime(debut, "%Y-%m-%dT%H:%M")
#         fin_obj = datetime.strptime(fin, "%Y-%m-%dT%H:%M")
#         #insert trx in operator table
#         for x in trx :
#             x['telephone'] = str(x['telephone']).replace('225','')
#             x['EndDateTime'] = x['EndDateTime'].split('.')[0]
#             x['EndDateTime'] = x['EndDateTime'].replace('/','-')
#             insert_operator_trx(x)
 
#         failed_trx = Cinetpay_transaction_failed(debut_obj,fin_obj)  # recover failed transactions from Cinetay
#         success_trx = Cinetpay_transaction_success(debut_obj, fin_obj)  # recover successfuly transactions from Cinetay
#         # insert failed transactions from Cinetay in DB----------
#         for x in failed_trx :
#             insert_failed_trx(x)
#         #---------------------------------------------------------
#         # insert successfuly transactions from Cinetay in DB------
#         for x in success_trx :
#             insert_success_trx(x)
#         #---------------------------------------------------------

#         difference = match_table() #match operator trx and CinetpaySucessfuly trx and return difference
#         #insert trx in difference table
#         for x in difference :
#             insert_difference(x)
#         # Detect each correspondent of trx in difference
#         detect_correspondent()
#         end_time = time.time()
#         print("Time for reconciling : %ssecs" % (end_time-start_time) )
        
#     return render(request, 'reconcile/excel_to_json.html')

#ONECI MTNCI ********************************************************************************************************************************






#MTNCI **************************************************************************************************************************************

# # # # Operator insertion-------------------------------------------------------------------------------------------------
# def insert_operator_trx_mtn_ci(x):
#     b =TrxOperateur(datepaiment=x['EndDateTime'], idpaiment=x['idpaiment'],status=x['ResponseMessage'],telephone=x['telephone'],montant=x['Amount'])
#     b.save()
#     print('sauvé')
# # # # #------------------------------------------------------------------------------------------------------------------------------




# # MTNCI CI-------------------------------------------------------------------------------------------------------------
# def Cinetpay_transaction_success(first,last):
#     success_trx = []  
#     all_trx = TrxCinetpay.objects.all()
#     # create a function for this and use task_manager
#     for trx in all_trx :
#             if trx.EtatTransaction == "SUCCES" and trx.methodePaiment!="DDVAMTNCI" and trx.marchand !="DDVA" and trx.methodePaiment=="MOMO" and trx.marchand !="ONECI - RNPP" and trx.NomDuService !="ONECI" :            
#                 trx_obj = datetime.strptime(trx.datePaiement, '%Y-%m-%d %H:%M:%S')
#                 if trx_obj <= last and trx_obj >= first :
#                     success_trx.append(trx)
#     print(len(success_trx))
#     return success_trx
# # #---------------------------------------------------------------------------------------------------------------------


# #MTNCI CI-------------------------------------------------------------------------------------------------------------
# def Cinetpay_transaction_failed(first,last):
#     failed_trx = []  
#     all_trx = TrxCinetpay.objects.all()
#     # create a function for this and use task_manager
#     for trx in all_trx :
#         if trx.EtatTransaction != "SUCCES" and trx.methodePaiment!="DDVAMTNCI" and trx.marchand !="DDVA" and trx.methodePaiment=="MOMO" and trx.marchand !="ONECI - RNPP" and trx.NomDuService !="ONECI":
#             trx.creation = str(trx.creation).replace('+00:00','')          
#             trx_obj = datetime.strptime(str(trx.creation), '%Y-%m-%d %H:%M:%S')
#             if trx_obj <= last and trx_obj >= first :
#                 failed_trx.append(trx)
#     print(len(failed_trx))
#     return failed_trx
# # #----------------------------------------------------------------------------------------------------------------------

# # # Insertion of failed transactions from Cinetpay------------------------------------------------------------------------------
# def insert_failed_trx(x):
#     b =TrxFailedCinetpay(creation=x.creation,datePaiement=x.datePaiement,marchand=x.marchand,EmailMarchand=x.EmailMarchand,
#     NomDuService=x.NomDuService,IdTransaction=x.IdTransaction,
#     SiteId=x.SiteId,Montant=x.Montant,methodePaiment=x.methodePaiment,
#     Telephone=x.Telephone,EtatTransaction=x.EtatTransaction,IdPaiment=x.IdPaiment)
#     b.save()
#     print('sauvé')
# # #-----------------------------------------------------------------------------------------------------------------------------

# # # Insertion of successfully transactions from Cinetpay------------------------------------------------------------------------------
# def insert_success_trx(x):
#     b =TrxSuccessCinetpay(creation=x.creation,datePaiement=x.datePaiement,marchand=x.marchand,EmailMarchand=x.EmailMarchand,
#     NomDuService=x.NomDuService,IdTransaction=x.IdTransaction,
#     SiteId=x.SiteId,Montant=x.Montant,methodePaiment=x.methodePaiment,
#     Telephone=x.Telephone,EtatTransaction=x.EtatTransaction,IdPaiment=x.IdPaiment)
#     b.save()
#     print('sauvé')
# # #-----------------------------------------------------------------------------------------------------------------------------

# # #transaction from operator and not from Cinetpay------------------------------------------------------------------------
# def match_table():
#     difference = TrxOperateur.objects.exclude(idpaiment__in=TrxSuccessCinetpay.objects.values_list('IdPaiment', flat=True))
#     return difference
# # #-----------------------------------------------------------------------------------------------------------------------

# # # Insertion transaction from operator and not from Cinetpay (difference)------------------------------------------------------
# def insert_difference(x):
#     b =TrxDifference(datepaiment=x.datepaiment, idpaiment=x.idpaiment,status=x.status,telephone=x.telephone,montant=x.montant)
#     b.save()
#     print('sauvé')
# # #-----------------------------------------------------------------------------------------------------------------------------



# TRANSACTION_LIST = []
# def reconcile(request):
#     if request.method == 'POST' :
#         start_time = time.time()
#         transaction = request.POST['valeur']
#         trx = json.loads(transaction)
#         debut = request.POST['debut']
#         fin = request.POST['fin']
#         debut_obj = datetime.strptime(debut, "%Y-%m-%dT%H:%M")
#         fin_obj = datetime.strptime(fin, "%Y-%m-%dT%H:%M")
#         #insert trx in operator table
#         b = debut.split('T')[0]
#         for x in trx :
#             x['telephone'] = str(x['telephone']).replace('225','')
#             x['EndDateTime'] = x['EndDateTime'].split('.')[0]
#             b = x['EndDateTime'].split(' ')[0]
#             x['EndDateTime'] = x['EndDateTime'].replace(b,debut.split('T')[0]) 
#             print(x['EndDateTime'])
#             insert_operator_trx(x)
 
#         failed_trx = Cinetpay_transaction_failed(debut_obj,fin_obj)  # recover failed transactions from Cinetay
#         success_trx = Cinetpay_transaction_success(debut_obj, fin_obj)  # recover successfuly transactions from Cinetay
#         # insert failed transactions from Cinetay in DB----------
#         for x in failed_trx :
#             insert_failed_trx(x)
#         #---------------------------------------------------------
#         # insert successfuly transactions from Cinetay in DB------
#         for x in success_trx :
#             insert_success_trx(x)
#         #---------------------------------------------------------

#         difference = match_table() #match operator trx and CinetpaySucessfuly trx and return difference
#         #insert trx in difference table
#         for x in difference :
#             insert_difference(x)
#         # Detect each correspondent of trx in difference
#         detect_correspondent()
#         end_time = time.time()
#         print("Time for reconciling : %ssecs" % (end_time-start_time) )
        
#     return render(request, 'reconcile/excel_to_json.html')

#MTNCI ********************************************************************************************************************************









#ONECI ORANGE ********************************************************************************************************************************

# # Orange Operator insertion precisely------------------------------------------------------------------------------------------
# def insert_operator_trx(x):
#     b =TrxOperateur(datepaiment=x['date'] +" "+ x['heure'], idpaiment=x['idpaiment'],status=x['status'],telephone=x['telephone'],montant=x['montant'])
#     b.save()
#     print('sauvé')
# #------------------------------------------------------------------------------------------------------------------------------



# #ONECI ORANGE CI-------------------------------------------------------------------------------------------------------------
# def Cinetpay_transaction_success(first,last):
#     success_trx = []  
#     all_trx = TrxCinetpay.objects.all()
#     # create a function for this and use task_manager
#     for trx in all_trx :
#             if trx.EtatTransaction=="SUCCES" and trx.methodePaiment=="OM" and trx.marchand =="ONECI - RNPP" and trx.NomDuService=="ONECI" :            
#                 trx_obj = datetime.strptime(trx.datePaiement, '%Y-%m-%d %H:%M:%S')
#                 if trx_obj <= last and trx_obj >= first :
#                     success_trx.append(trx)
#     print(len(success_trx))
#     return success_trx
# #---------------------------------------------------------------------------------------------------------------------


# #ONECI ORANGE CI-------------------------------------------------------------------------------------------------------------
# def Cinetpay_transaction_failed(first,last):
#     failed_trx = []  
#     all_trx = TrxCinetpay.objects.all()
#     # create a function for this and use task_manager
#     for trx in all_trx :
#         if trx.EtatTransaction != "SUCCES" and trx.methodePaiment=="OM" and trx.marchand =="ONECI - RNPP" and trx.NomDuService=="ONECI":
#             trx.creation = str(trx.creation).replace('+00:00','')          
#             trx_obj = datetime.strptime(str(trx.creation), '%Y-%m-%d %H:%M:%S')
#             if trx_obj <= last and trx_obj >= first :
#                 failed_trx.append(trx)
#     print(len(failed_trx))
#     return failed_trx
# #----------------------------------------------------------------------------------------------------------------------

# # Insertion of failed transactions from Cinetpay------------------------------------------------------------------------------
# def insert_failed_trx(x):
#     b =TrxFailedCinetpay(creation=x.creation,datePaiement=x.datePaiement,marchand=x.marchand,EmailMarchand=x.EmailMarchand,
#     NomDuService=x.NomDuService,IdTransaction=x.IdTransaction,
#     SiteId=x.SiteId,Montant=x.Montant,methodePaiment=x.methodePaiment,
#     Telephone=x.Telephone,EtatTransaction=x.EtatTransaction,IdPaiment=x.IdPaiment)
#     b.save()
#     print('sauvé')
# #-----------------------------------------------------------------------------------------------------------------------------

# # Insertion of successfully transactions from Cinetpay------------------------------------------------------------------------------
# def insert_success_trx(x):
#     b =TrxSuccessCinetpay(creation=x.creation,datePaiement=x.datePaiement,marchand=x.marchand,EmailMarchand=x.EmailMarchand,
#     NomDuService=x.NomDuService,IdTransaction=x.IdTransaction,
#     SiteId=x.SiteId,Montant=x.Montant,methodePaiment=x.methodePaiment,
#     Telephone=x.Telephone,EtatTransaction=x.EtatTransaction,IdPaiment=x.IdPaiment)
#     b.save()
#     print('sauvé')
# #-----------------------------------------------------------------------------------------------------------------------------

# #transaction from operator and not from Cinetpay------------------------------------------------------------------------
# def match_table():
#     difference = TrxOperateur.objects.exclude(idpaiment__in=TrxSuccessCinetpay.objects.values_list('IdPaiment', flat=True))
#     return difference
# #-----------------------------------------------------------------------------------------------------------------------

# # Insertion transaction from operator and not from Cinetpay (difference)------------------------------------------------------
# def insert_difference(x):
#     b =TrxDifference(datepaiment=x.datepaiment, idpaiment=x.idpaiment,status=x.status,telephone=x.telephone,montant=x.montant)
#     b.save()
#     print('sauvé')
# #-----------------------------------------------------------------------------------------------------------------------------



# TRANSACTION_LIST = []
# def reconcile(request):
#     if request.method == 'POST' :
#         start_time = time.time()
#         transaction = request.POST['valeur']
#         trx = json.loads(transaction)
#         debut = request.POST['debut']
#         fin = request.POST['fin']
#         debut_obj = datetime.strptime(debut, "%Y-%m-%dT%H:%M")
#         fin_obj = datetime.strptime(fin, "%Y-%m-%dT%H:%M")
#         # print(debut.split('T')[0])
#         # insert trx in operator table
#         for x in trx :
#             b = x['date']
#             x['date'] = x['date'].replace(b,debut.split('T')[0])
#             print(x['date'])
#             insert_operator_trx(x)
 
#         failed_trx = Cinetpay_transaction_failed(debut_obj,fin_obj)  # recover failed transactions from Cinetay
#         success_trx = Cinetpay_transaction_success(debut_obj, fin_obj)  # recover successfuly transactions from Cinetay
#         # insert failed transactions from Cinetay in DB----------
#         for x in failed_trx :
#             insert_failed_trx(x)
#         #---------------------------------------------------------
#         # insert successfuly transactions from Cinetay in DB------
#         for x in success_trx :
#             insert_success_trx(x)
#         #---------------------------------------------------------

#         difference = match_table() #match operator trx and CinetpaySucessfuly trx and return difference
#         #insert trx in difference table
#         for x in difference :
#             insert_difference(x)
#         # Detect each correspondent of trx in difference
#         detect_correspondent()
#         end_time = time.time()
#         print("Time for reconciling : %ssecs" % (end_time-start_time) )
        
#     return render(request, 'reconcile/excel_to_json.html')

#ONECI ORANGE ********************************************************************************************************************************





#DDVA ORANGE ********************************************************************************************************************************

# # Orange Operator insertion precisely------------------------------------------------------------------------------------------
# def insert_operator_trx(x):
#     b =TrxOperateur(datepaiment=x['date'] +" "+ x['heure'], idpaiment=x['idpaiment'],status=x['status'],telephone=x['telephone'],montant=x['montant'])
#     b.save()
#     print('sauvé')
# #------------------------------------------------------------------------------------------------------------------------------



# #DDVA ORANGE CI-------------------------------------------------------------------------------------------------------------
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
# #---------------------------------------------------------------------------------------------------------------------


# #DDVA ORANGE CI-------------------------------------------------------------------------------------------------------------
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
# #----------------------------------------------------------------------------------------------------------------------

# # Insertion of failed transactions from Cinetpay------------------------------------------------------------------------------
# def insert_failed_trx(x):
#     b =TrxFailedCinetpay(creation=x.creation,datePaiement=x.datePaiement,marchand=x.marchand,EmailMarchand=x.EmailMarchand,
#     NomDuService=x.NomDuService,IdTransaction=x.IdTransaction,
#     SiteId=x.SiteId,Montant=x.Montant,methodePaiment=x.methodePaiment,
#     Telephone=x.Telephone,EtatTransaction=x.EtatTransaction,IdPaiment=x.IdPaiment)
#     b.save()
#     print('sauvé')
# #-----------------------------------------------------------------------------------------------------------------------------

# # Insertion of successfully transactions from Cinetpay------------------------------------------------------------------------------
# def insert_success_trx(x):
#     b =TrxSuccessCinetpay(creation=x.creation,datePaiement=x.datePaiement,marchand=x.marchand,EmailMarchand=x.EmailMarchand,
#     NomDuService=x.NomDuService,IdTransaction=x.IdTransaction,
#     SiteId=x.SiteId,Montant=x.Montant,methodePaiment=x.methodePaiment,
#     Telephone=x.Telephone,EtatTransaction=x.EtatTransaction,IdPaiment=x.IdPaiment)
#     b.save()
#     print('sauvé')
# #-----------------------------------------------------------------------------------------------------------------------------

# #transaction from operator and not from Cinetpay------------------------------------------------------------------------
# def match_table():
#     difference = TrxOperateur.objects.exclude(idpaiment__in=TrxSuccessCinetpay.objects.values_list('IdPaiment', flat=True))
#     return difference
# #-----------------------------------------------------------------------------------------------------------------------

# # Insertion transaction from operator and not from Cinetpay (difference)------------------------------------------------------
# def insert_difference(x):
#     b =TrxDifference(datepaiment=x.datepaiment, idpaiment=x.idpaiment,status=x.status,telephone=x.telephone,montant=x.montant)
#     b.save()
#     print('sauvé')
# #-----------------------------------------------------------------------------------------------------------------------------



# TRANSACTION_LIST = []
# def reconcile(request):
#     if request.method == 'POST' :
#         start_time = time.time()
#         transaction = request.POST['valeur']
#         trx = json.loads(transaction)
#         debut = request.POST['debut']
#         fin = request.POST['fin']
#         debut_obj = datetime.strptime(debut, "%Y-%m-%dT%H:%M")
#         fin_obj = datetime.strptime(fin, "%Y-%m-%dT%H:%M")
#         # print(debut.split('T')[0])
#         # insert trx in operator table
#         for x in trx :
#             b = x['date']
#             x['date'] = x['date'].replace(b,debut.split('T')[0])
#             print(x['date'])
#             insert_operator_trx(x)
 
#         failed_trx = Cinetpay_transaction_failed(debut_obj,fin_obj)  # recover failed transactions from Cinetay
#         success_trx = Cinetpay_transaction_success(debut_obj, fin_obj)  # recover successfuly transactions from Cinetay
#         # insert failed transactions from Cinetay in DB----------
#         for x in failed_trx :
#             insert_failed_trx(x)
#         #---------------------------------------------------------
#         # insert successfuly transactions from Cinetay in DB------
#         for x in success_trx :
#             insert_success_trx(x)
#         #---------------------------------------------------------

#         difference = match_table() #match operator trx and CinetpaySucessfuly trx and return difference
#         #insert trx in difference table
#         for x in difference :
#             insert_difference(x)
#         # Detect each correspondent of trx in difference
#         detect_correspondent()
#         end_time = time.time()
#         print("Time for reconciling : %ssecs" % (end_time-start_time) )
        
#     return render(request, 'reconcile/excel_to_json.html')

#DDVA ORANGE ********************************************************************************************************************************








#ORANGECI ***********************************************************************************************************************************


# Orange Operator insertion precisely------------------------------------------------------------------------------------------
# def insert_operator_trx(x):
#     b =TrxOperateur(datepaiment=x['date'] +" "+ x['heure'], idpaiment=x['idpaiment'],status=x['status'],telephone=x['telephone'],montant=x['montant'])
#     b.save()
#     print('sauvé')
#------------------------------------------------------------------------------------------------------------------------------



#ORANGE CI-------------------------------------------------------------------------------------------------------------
# def Cinetpay_transaction_success(first,last):
#     success_trx = []  
#     all_trx = TrxCinetpay.objects.all()
#     # create a function for this and use task_manager
#     for trx in all_trx :
#             if trx.EtatTransaction == "SUCCES" and trx.methodePaiment !="DDVAOMCI" and trx.marchand  !="DDVA" and trx.methodePaiment=="OM" and trx.marchand !="ONECI - RNPP" and trx.NomDuService !="ONECI":            
#                 trx_obj = datetime.strptime(trx.datePaiement, '%Y-%m-%d %H:%M:%S')
#                 if trx_obj <= last and trx_obj >= first :
#                     success_trx.append(trx)
#     print(len(success_trx))
#     return success_trx
#---------------------------------------------------------------------------------------------------------------------


#ORANGE CI-------------------------------------------------------------------------------------------------------------
# def Cinetpay_transaction(first,last):
#     failed_trx = []  
#     all_trx = TrxCinetpay.objects.all()
#     # create a function for this and use task_manager
#     for trx in all_trx :
#         if trx.EtatTransaction != "SUCCES" and trx.methodePaiment !="DDVAOMCI" and trx.marchand  !="DDVA" and trx.methodePaiment=="OM" and trx.marchand !="ONECI - RNPP" and trx.NomDuService !="ONECI":
#             trx.creation = str(trx.creation).replace('+00:00','')          
#             trx_obj = datetime.strptime(str(trx.creation), '%Y-%m-%d %H:%M:%S')
#             if trx_obj <= last and trx_obj >= first :
#                 failed_trx.append(trx)
#     print(len(failed_trx))
#     return failed_trx
#----------------------------------------------------------------------------------------------------------------------

# Insertion of failed transactions from Cinetpay------------------------------------------------------------------------------
# def insert_failed_trx(x):
#     b =TrxFailedCinetpay(creation=x.creation,datePaiement=x.datePaiement,marchand=x.marchand,EmailMarchand=x.EmailMarchand,
#     NomDuService=x.NomDuService,IdTransaction=x.IdTransaction,
#     SiteId=x.SiteId,Montant=x.Montant,methodePaiment=x.methodePaiment,
#     Telephone=x.Telephone,EtatTransaction=x.EtatTransaction,IdPaiment=x.IdPaiment)
#     b.save()
#     print('sauvé')
#-----------------------------------------------------------------------------------------------------------------------------

# Insertion of successfully transactions from Cinetpay------------------------------------------------------------------------
# def insert_success_trx(x):
#     b =TrxSuccessCinetpay(creation=x.creation,datePaiement=x.datePaiement,marchand=x.marchand,EmailMarchand=x.EmailMarchand,
#     NomDuService=x.NomDuService,IdTransaction=x.IdTransaction,
#     SiteId=x.SiteId,Montant=x.Montant,methodePaiment=x.methodePaiment,
#     Telephone=x.Telephone,EtatTransaction=x.EtatTransaction,IdPaiment=x.IdPaiment)
#     b.save()
#     print('sauvé')
#-----------------------------------------------------------------------------------------------------------------------------

#transaction from operator and not from Cinetpay------------------------------------------------------------------------
# def match_table():
#     difference = TrxOperateur.objects.exclude(idpaiment__in=TrxSuccessCinetpay.objects.values_list('IdPaiment', flat=True))
#     return difference
#-----------------------------------------------------------------------------------------------------------------------

# Insertion transaction from operator and not from Cinetpay (difference)------------------------------------------------------
# def insert_difference(x):
#     b =TrxDifference(datepaiment=x.datepaiment, idpaiment=x.idpaiment,status=x.status,telephone=x.telephone,montant=x.montant)
#     b.save()
#     print('sauvé')
#-----------------------------------------------------------------------------------------------------------------------------



# TRANSACTION_LIST = []
# def reconcile(request):
#     if request.method == 'POST' :
#         start_time = time.time()
#         transaction = request.POST['valeur']
#         trx = json.loads(transaction)
#         debut = request.POST['debut']
#         fin = request.POST['fin']
#         debut_obj = datetime.strptime(debut, "%Y-%m-%dT%H:%M")
#         fin_obj = datetime.strptime(fin, "%Y-%m-%dT%H:%M")
#         # print(debut.split('T')[0])
#         # insert trx in operator table
#         for x in trx :
#             b = x['date']
#             x['date'] = x['date'].replace(b,debut.split('T')[0])
#             print(x['date'])
#             insert_operator_trx(x)

#         failed_trx = Cinetpay_transaction_failed(debut_obj,fin_obj)  # recover failed transactions from Cinetay
#         success_trx = Cinetpay_transaction_success(debut_obj, fin_obj)  # recover successfuly transactions from Cinetay
#         # insert failed transactions from Cinetay in DB----------
#         for x in failed_trx :
#             insert_failed_trx(x)
#         #---------------------------------------------------------
#         # insert successfuly transactions from Cinetay in DB------
#         for x in success_trx :
#             insert_success_trx(x)
#         #---------------------------------------------------------

#         difference = match_table() #match operator trx and CinetpaySucessfuly trx and return difference
#         #insert trx in difference table
#         for x in difference :
#             insert_difference(x)
#         # Detect each correspondent of trx in difference
#         detect_correspondent()
#         end_time = time.time()
#         print("Time for reconciling : %ssecs" % (end_time-start_time) )
        
#     return render(request, 'reconcile/excel_to_json.html')
    

#ORANGE CI ********************************************************************************************************************************














def insert_operator_trx_ddva_mtn(x):
    b =TrxOperateur(datepaiment=x['Datepaiment'], idpaiment=x['idpaiment'],status=x['Statut'],telephone=x['telephone'],montant=x['Montant'])
    b.save()
    print('sauvé')


def Cinetpay_transaction_success_ddva_mtn(first,last):
    success_trx = []  
    all_trx = TrxCinetpay.objects.filter(EtatTransaction="SUCCES",methodePaiment="DDVAMTNCI",marchand ="DDVA" )
    # create a function for this and use task_manager
    for trx in all_trx :        
        trx_obj = datetime.strptime(trx.datePaiement, '%Y-%m-%d %H:%M:%S')
        if trx_obj <= last and trx_obj >= first :
            success_trx.append(trx)
    print(len(success_trx))
    return success_trx


def Cinetpay_transaction_failed_ddva_mtn(first,last):
    failed_trx = []  
    all_trx = TrxCinetpay.objects.filter(methodePaiment="DDVAMTNCI",marchand ="DDVA").exclude(EtatTransaction__contains="SUCCES")
    # create a function for this and use task_manager
    for trx in all_trx :
        trx.creation = str(trx.creation).replace('+00:00','')          
        trx_obj = datetime.strptime(str(trx.creation), '%Y-%m-%d %H:%M:%S')
        if trx_obj <= last and trx_obj >= first :
            failed_trx.append(trx)
    print(len(failed_trx))
    return failed_trx

def insert_operator_trx_oneci_mtn(x):
    b =TrxOperateur(datepaiment=x['EndDateTime'], idpaiment=x['idpaiment'],status=x['ResponseMessage'],telephone=x['telephone'],montant=x['Amount'])
    b.save()
    print('sauvé')

    


def Cinetpay_transaction_success_oneci_mtn(first,last):
    success_trx = []  
    all_trx = TrxCinetpay.objects.filter(EtatTransaction = "SUCCES",methodePaiment="MOMO",marchand ="ONECI - RNPP",NomDuService="ONECI")
    # create a function for this and use task_manager
    for trx in all_trx :           
        trx_obj = datetime.strptime(trx.datePaiement, '%Y-%m-%d %H:%M:%S')
        if trx_obj <= last and trx_obj >= first :
            success_trx.append(trx)
    print(len(success_trx))
    return success_trx


def Cinetpay_transaction_failed_oneci_mtn(first,last):
    failed_trx = []  
    all_trx = TrxCinetpay.objects.filter(methodePaiment="MOMO",marchand ="ONECI - RNPP",NomDuService="ONECI").exclude(EtatTransaction__contains="SUCCES")
    # create a function for this and use task_manager
    for trx in all_trx :           
        trx.creation = str(trx.creation).replace('+00:00','')          
        trx_obj = datetime.strptime(str(trx.creation), '%Y-%m-%d %H:%M:%S')
        if trx_obj <= last and trx_obj >= first :
            failed_trx.append(trx)
    print(len(failed_trx))
    return failed_trx


def insert_operator_trx_mtn_ci(x):
    b =TrxOperateur(datepaiment=x['EndDateTime'], idpaiment=x['idpaiment'],status=x['ResponseMessage'],telephone=x['telephone'],montant=x['Amount'])
    b.save()
    print('sauvé')


def Cinetpay_transaction_success_mtn_ci(first,last):
    success_trx = []  
    all_trx = TrxCinetpay.objects.filter(methodePaiment="MOMO",EtatTransaction="SUCCES").exclude(methodePaiment__contains="DDVAMTNCI",marchand__contains="DDVA",NomDuService__contains="ONECI").exclude(marchand__contains="ONECI - RNPP")
    # create a function for this and use task_manager
    for trx in all_trx :
        trx_obj = datetime.strptime(trx.datePaiement, '%Y-%m-%d %H:%M:%S')
        if trx_obj <= last and trx_obj >= first :
            success_trx.append(trx)
    print(len(success_trx))
    return success_trx

    
def Cinetpay_transaction_failed_mtn_ci(first,last):
    failed_trx = []  
    all_trx = TrxCinetpay.objects.filter(methodePaiment="MOMO").exclude(methodePaiment__contains="DDVAMTNCI",marchand__contains="DDVA",NomDuService__contains="ONECI").exclude(marchand__contains="ONECI - RNPP").exclude(EtatTransaction__contains="SUCCES")
    # create a function for this and use task_manager
    for trx in all_trx :
        trx.creation = str(trx.creation).replace('+00:00','')          
        trx_obj = datetime.strptime(str(trx.creation), '%Y-%m-%d %H:%M:%S')
        if trx_obj <= last and trx_obj >= first :
            failed_trx.append(trx)
    print(len(failed_trx))
    return failed_trx


def Cinetpay_transaction_success_oneci_orange_ci(first,last):
    success_trx = []  
    all_trx = TrxCinetpay.objects.filter(EtatTransaction="SUCCES",methodePaiment="OM",marchand="ONECI - RNPP",NomDuService="ONECI")
    # create a function for this and use task_manager
    for trx in all_trx :           
        trx_obj = datetime.strptime(trx.datePaiement, '%Y-%m-%d %H:%M:%S')
        if trx_obj <= last and trx_obj >= first :
            success_trx.append(trx)
    print(len(success_trx))
    return success_trx


def Cinetpay_transaction_failed_oneci_orange_ci(first,last):
    failed_trx = []  
    all_trx = TrxCinetpay.objects.filter(methodePaiment="OM",marchand ="ONECI - RNPP",NomDuService="ONECI").exclude(EtatTransaction__contains="SUCCES")
    # create a function for this and use task_manager
    for trx in all_trx :
        trx.creation = str(trx.creation).replace('+00:00','')          
        trx_obj = datetime.strptime(str(trx.creation), '%Y-%m-%d %H:%M:%S')
        if trx_obj <= last and trx_obj >= first :
            failed_trx.append(trx)
    print(len(failed_trx))
    return failed_trx


def Cinetpay_transaction_success_ddva_orange(first,last):
    success_trx = []  
    all_trx = TrxCinetpay.objects.filter(EtatTransaction="SUCCES",methodePaiment="DDVAOMCI",marchand ="DDVA")
    # create a function for this and use task_manager
    for trx in all_trx :            
        trx_obj = datetime.strptime(trx.datePaiement, '%Y-%m-%d %H:%M:%S')
        if trx_obj <= last and trx_obj >= first :
            success_trx.append(trx)
    print(len(success_trx))
    return success_trx


def Cinetpay_transaction_failed_ddva_orange(first,last):
    failed_trx = []  
    all_trx = TrxCinetpay.objects.filter(methodePaiment="DDVAOMCI",marchand ="DDVA").exclude(EtatTransaction__contains="SUCCES")
    # create a function for this and use task_manager
    for trx in all_trx :
        trx.creation = str(trx.creation).replace('+00:00','')          
        trx_obj = datetime.strptime(str(trx.creation), '%Y-%m-%d %H:%M:%S')
        if trx_obj <= last and trx_obj >= first :
            failed_trx.append(trx)
    print(len(failed_trx))
    return failed_trx


# Orange Operator insertion precisely------------------------------------------------------------------------------------------
def insert_operator_trx(x):
    b =TrxOperateur(datepaiment=x['date'] +" "+ x['heure'], idpaiment=x['idpaiment'],status=x['status'],telephone=x['telephone'],montant=x['montant'])
    b.save()
    print('sauvé')
#------------------------------------------------------------------------------------------------------------------------------


def Cinetpay_transaction_success_orange_ci(first,last):
    success_trx = []  
    all_trx = TrxCinetpay.objects.filter(EtatTransaction = "SUCCES",methodePaiment="OM").exclude(methodePaiment__contains="DDVAOMCI",
    marchand__contains="DDVA",NomDuService__contains="ONECI").exclude(marchand__contains="ONECI - RNPP")
    # create a function for this and use task_manager
    for trx in all_trx :
        trx_obj = datetime.strptime(trx.datePaiement, '%Y-%m-%d %H:%M:%S')
        if trx_obj <= last and trx_obj >= first :
            success_trx.append(trx)
    print(len(success_trx))
    return success_trx


def Cinetpay_transaction_failed_orange_ci(first,last):
    failed_trx = []  
    all_trx = TrxCinetpay.objects.filter(methodePaiment="OM").exclude(methodePaiment__contains="DDVAOMCI", marchand__contains="DDVA" ,NomDuService__contains="ONECI").exclude( marchand__contains="ONECI - RNPP").exclude(EtatTransaction__contains="SUCCES")
    # create a function for this and use task_manager
    for trx in all_trx :
        trx.creation = str(trx.creation).replace('+00:00','')          
        trx_obj = datetime.strptime(str(trx.creation), '%Y-%m-%d %H:%M:%S')
        if trx_obj <= last and trx_obj >= first :
            failed_trx.append(trx)
    print(len(failed_trx))
    return failed_trx


# Insertion of failed transactions from Cinetpay------------------------------------------------------------------------------
def insert_failed_trx(x):
    b =TrxFailedCinetpay(creation=x.creation,datePaiement=x.datePaiement,marchand=x.marchand,EmailMarchand=x.EmailMarchand,
    NomDuService=x.NomDuService,IdTransaction=x.IdTransaction,
    SiteId=x.SiteId,Montant=x.Montant,methodePaiment=x.methodePaiment,
    Telephone=x.Telephone,EtatTransaction=x.EtatTransaction,IdPaiment=x.IdPaiment)
    b.save()
    print('sauvé')
#-----------------------------------------------------------------------------------------------------------------------------


# Insertion of successfully transactions from Cinetpay------------------------------------------------------------------------
def insert_success_trx(x):
    b =TrxSuccessCinetpay(creation=x.creation,datePaiement=x.datePaiement,marchand=x.marchand,EmailMarchand=x.EmailMarchand,
    NomDuService=x.NomDuService,IdTransaction=x.IdTransaction,
    SiteId=x.SiteId,Montant=x.Montant,methodePaiment=x.methodePaiment,
    Telephone=x.Telephone,EtatTransaction=x.EtatTransaction,IdPaiment=x.IdPaiment)
    b.save()
    print('sauvé')
#-----------------------------------------------------------------------------------------------------------------------------



#transaction from operator and not from Cinetpay------------------------------------------------------------------------------
def match_table():
    difference = TrxOperateur.objects.exclude(idpaiment__in=TrxSuccessCinetpay.objects.values_list('IdPaiment', flat=True))
    return difference
#-----------------------------------------------------------------------------------------------------------------------

# Insertion transaction from operator and not from Cinetpay (difference)------------------------------------------------------
def insert_difference(x):
    b =TrxDifference(datepaiment=x.datepaiment, idpaiment=x.idpaiment,status=x.status,telephone=x.telephone,montant=x.montant)
    b.save()
    print('sauvé')
#-----------------------------------------------------------------------------------------------------------------------------


def verify_ddva_orange_ci(file) : 
    empty_trx =[]
    field = [ "date","heure","idpaiment","status","montant" ,"telephone" ]
    for  count ,x in enumerate(file) :
        if field == list(x.keys()) :
            pass
        else :
            empty_trx.append(count)
    return empty_trx



def verify_orange_ci(file) : 
    pass

def verify_oneci_orange_ci(file):
    pass
 
def verify_mtn_ci(file):
    pass

def verify_ddva_mtn_ci(file):
    pass

def verify_oneci_mtn_ci(file):
    pass

# GENERAL ***********************************************************************************************************************************


operator = '0'
TRANSACTION_LIST = []
def reconcile(request):
    if request.method == 'POST' : 
        operator = request.POST.getlist('operateur')[0]
        transaction = request.POST['valeur']
        trx = json.loads(transaction)
        debut = request.POST['debut']
        fin = request.POST['fin']
        debut_obj = datetime.strptime(debut, "%Y-%m-%dT%H:%M")
        fin_obj = datetime.strptime(fin, "%Y-%m-%dT%H:%M")


        if operator == '1' :  # orange_ci
            state = verify_orange_ci(trx)
            if len(state) == 0 : 
                start_time  =time.time()
                for x in trx :
                        b = x['date']
                        x['date'] = x['date'].replace(b,debut.split('T')[0])
                        print(x['date'])
                        insert_operator_trx(x) 
                failed_trx = Cinetpay_transaction_failed_orange_ci(debut_obj,fin_obj)  # recover failed transactions from Cinetay
                success_trx = Cinetpay_transaction_success_orange_ci(debut_obj, fin_obj)  # recover successfuly transactions from Cinetay
                # insert failed transactions from Cinetay in DB----------
                for x in failed_trx :
                    insert_failed_trx(x)
                #---------------------------------------------------------
                # insert successfuly transactions from Cinetay in DB------
                for x in success_trx :
                    insert_success_trx(x)
                #---------------------------------------------------------

                difference = match_table() #match operator trx and CinetpaySucessfuly trx and return difference
                #insert trx in difference table
                for x in difference :
                    insert_difference(x)
                # Detect each correspondent of trx in difference
                detect_correspondent()
                end_time = time.time()
                print("Time for reconciling : %ssecs" % (end_time-start_time) )

                data = TrxRightCorrespodent.objects.all()
                diff = TrxDifference.objects.all()
                
                return render(request, 'reconcile/display.html',{'correspondent': data, 'difference' : diff})
            else :
                return render(request, 'reconcile/error.html',{'file':trx,'etat':state})


        if operator == '2' : #ddva orange
            state = verify_ddva_orange_ci(trx)
            if len(state) == 0 :
                start_time  =time.time()
                #insert trx in operator table
                for x in trx :
                    b = x['date']
                    x['date'] = x['date'].replace(b,debut.split('T')[0])
                    print(x['date'])
                    insert_operator_trx(x)
        
                failed_trx = Cinetpay_transaction_failed_ddva_orange(debut_obj,fin_obj)  # recover failed transactions from Cinetay
                success_trx = Cinetpay_transaction_success_ddva_orange(debut_obj, fin_obj)  # recover successfuly transactions from Cinetay
                # insert failed transactions from Cinetay in DB----------
                for x in failed_trx :
                    insert_failed_trx(x)
                #---------------------------------------------------------
                # insert successfuly transactions from Cinetay in DB------
                for x in success_trx :
                    insert_success_trx(x)
                #---------------------------------------------------------

                difference = match_table() #match operator trx and CinetpaySucessfuly trx and return difference
                #insert trx in difference table
                for x in difference :
                    insert_difference(x)
                # Detect each correspondent of trx in difference
                detect_correspondent()
                end_time = time.time()
                print("Time for reconciling : %ssecs" % (end_time-start_time) )
                data = TrxRightCorrespodent.objects.all()
                # operatorAmount = TrxOperateur.objects.aggregate(Sum('montant'))
                # CinetpayAmount = TrxSuccessCinetpay.objects.aggregate(Sum('Montant'))
                # print(CinetpayAmount,operatorAmount)
                # diffAmount = operatorAmount['montant__avg'] - CinetpayAmount['Montant__avg']
                diff = TrxDifference.objects.all()
                countOperator= TrxOperateur.objects.all().count()
                countCinetpay = TrxSuccessCinetpay.objects.all().count()
                diffCount = countOperator - countCinetpay

                information = {
                    'correspondent': data, 
                    'difference':diff,
                    # 'total':operatorAmount,
                    # 'montantCinetpay':CinetpayAmount,
                    # 'diffMontant':diffAmount,
                    'countOperator':countOperator,
                    'countCinetpay':countCinetpay,
                    'diffCount':diffCount 
                }
                
                return render(request, 'reconcile/display.html',information)
            else :  
                return render(request, 'reconcile/error.html',{'file':trx,'etat':state})



        if operator == '3':  # oneci orange ci
            state = verify_oneci_orange_ci(trx)
            if len(state) == 0 :
                start_time  =time.time()
                # insert trx in operator table
                for x in trx :
                    b = x['date']
                    x['date'] = x['date'].replace(b,debut.split('T')[0])
                    print(x['date'])
                    insert_operator_trx(x)
        
                failed_trx = Cinetpay_transaction_failed_oneci_orange_ci(debut_obj,fin_obj)  # recover failed transactions from Cinetay
                success_trx = Cinetpay_transaction_success_oneci_orange_ci(debut_obj, fin_obj)  # recover successfuly transactions from Cinetay
                # insert failed transactions from Cinetay into DB----------
                for x in failed_trx :
                    insert_failed_trx(x)
                #---------------------------------------------------------
                # insert successfuly transactions from Cinetay into DB------
                for x in success_trx :
                    insert_success_trx(x)
                #---------------------------------------------------------

                difference = match_table() #match operator trx and CinetpaySucessfuly trx and return difference
                #insert trx in difference table
                for x in difference :
                    insert_difference(x)
                # Detect each correspondent of trx in difference
                detect_correspondent()
                end_time = time.time()
                print("Time for reconciling : %ssecs" % (end_time-start_time) )

                data = TrxRightCorrespodent.objects.all()
                operatorAmount = TrxOperateur.objects.aggregate(Sum('montant'))
                CinetpayAmount = TrxSuccessCinetpay.objects.aggregate(Sum('Montant'))
                print(operatorAmount)
                diffAmount = operatorAmount['montant__sum'] - CinetpayAmount['Montant__sum']
                diff = TrxDifference.objects.all()
                countOperator= TrxOperateur.objects.all().count()
                countCinetpay = TrxSuccessCinetpay.objects.all().count()
                diffCount = countOperator - countCinetpay
                
                trx = {
                    'correspondent': data, 
                    'difference':diff,
                    'total':operatorAmount,
                    'montantCinetpay':CinetpayAmount,
                    'diffMontant':diffAmount,
                    'countOperator':countOperator,
                    'countCinetpay':countCinetpay,
                    'diffCount':diffCount 
                }
                
                return render(request, 'reconcile/display.html',trx)
            else :
                return render(request, 'reconcile/error.html',{'file':trx,'etat':state})



        if operator == '4' : # mtn ci
            state = verify_mtn_ci(trx)
            if len(state) == 0 :
                start_time  =time.time()
                #insert trx in operator table
                b = debut.split('T')[0]
                for x in trx :
                    x['telephone'] = str(x['telephone']).replace('225','')
                    x['EndDateTime'] = x['EndDateTime'].split('.')[0]
                    b = x['EndDateTime'].split(' ')[0]
                    x['EndDateTime'] = x['EndDateTime'].replace(b,debut.split('T')[0]) 
                    print(x['EndDateTime'])
                    insert_operator_trx_mtn_ci(x)
        
                failed_trx = Cinetpay_transaction_failed_mtn_ci(debut_obj,fin_obj)  # recover failed transactions from Cinetay
                success_trx = Cinetpay_transaction_success_mtn_ci(debut_obj, fin_obj)  # recover successfuly transactions from Cinetay
                # insert failed transactions from Cinetay in DB----------
                for x in failed_trx :
                    insert_failed_trx(x)
                #---------------------------------------------------------
                # insert successfuly transactions from Cinetay in DB------
                for x in success_trx :
                    insert_success_trx(x)
                #---------------------------------------------------------

                difference = match_table() #match operator trx and CinetpaySucessfuly trx and return difference
                #insert trx in difference table
                for x in difference :
                    insert_difference(x)
                # Detect each correspondent of trx in difference
                detect_correspondent()
                end_time = time.time()
                print("Time for reconciling : %ssecs" % (end_time-start_time) )

                data = TrxRightCorrespodent.objects.all()
                operatorAmount = TrxOperateur.objects.aggregate(Sum('montant'))
                CinetpayAmount = TrxSuccessCinetpay.objects.aggregate(Sum('Montant'))
                print(operatorAmount)
                diffAmount = operatorAmount['montant__sum'] - CinetpayAmount['Montant__sum']
                diff = TrxDifference.objects.all()
                countOperator= TrxOperateur.objects.all().count()
                countCinetpay = TrxSuccessCinetpay.objects.all().count()
                diffCount = countOperator - countCinetpay
                
                trx = {
                    'correspondent': data, 
                    'difference':diff,
                    'total':operatorAmount,
                    'montantCinetpay':CinetpayAmount,
                    'diffMontant':diffAmount,
                    'countOperator':countOperator,
                    'countCinetpay':countCinetpay,
                    'diffCount':diffCount 
                }
                
                return render(request, 'reconcile/display.html',trx)
            else :
                return render(request, 'reconcile/error.html',{'file':trx,'etat':state})



        if operator == '5' : # ddva mtn ci
            state = verify_ddva_mtn_ci(trx)        
            if len(state) == 0 :
                start_time  =time.time()
                #insert trx in operator table
                b = debut.split('T')[0]
                for x in trx :
                    x['telephone'] = str(x['telephone']).replace('225','')
                    s = x['Datepaiment'].split('  ')[1]
                    x['Datepaiment'] = " ".join([b,s])
                    print(x['Datepaiment'])
                    insert_operator_trx_ddva_mtn(x)
        
                failed_trx = Cinetpay_transaction_failed_ddva_mtn(debut_obj,fin_obj)  # recover failed transactions from Cinetay
                success_trx = Cinetpay_transaction_success_ddva_mtn(debut_obj, fin_obj)  # recover successfuly transactions from Cinetay
                # insert failed transactions from Cinetay in DB----------
                for x in failed_trx :
                    insert_failed_trx(x)
                #---------------------------------------------------------
                # insert successfuly transactions from Cinetay in DB------
                for x in success_trx :
                    insert_success_trx(x)
                #---------------------------------------------------------

                difference = match_table() #match operator trx and CinetpaySucessfuly trx and return difference
                #insert trx in difference table
                for x in difference :
                    insert_difference(x)
                # Detect each correspondent of trx in difference
                detect_correspondent()
                end_time = time.time()
                print("Time for reconciling : %ssecs" % (end_time-start_time) )

                data = TrxRightCorrespodent.objects.all()
                operatorAmount = TrxOperateur.objects.aggregate(Sum('montant'))
                CinetpayAmount = TrxSuccessCinetpay.objects.aggregate(Sum('Montant'))
                print(operatorAmount)
                diffAmount = operatorAmount['montant__sum'] - CinetpayAmount['Montant__sum']
                diff = TrxDifference.objects.all()
                countOperator= TrxOperateur.objects.all().count()
                countCinetpay = TrxSuccessCinetpay.objects.all().count()
                diffCount = countOperator - countCinetpay
                
                trx = {
                    'correspondent': data, 
                    'difference':diff,
                    'total':operatorAmount,
                    'montantCinetpay':CinetpayAmount,
                    'diffMontant':diffAmount,
                    'countOperator':countOperator,
                    'countCinetpay':countCinetpay,
                    'diffCount':diffCount 
                }
                
                return render(request, 'reconcile/display.html',trx)
            else :
                return render(request, 'reconcile/error.html',{'file':trx,'etat':state})



        if operator == '6': # oneci mtn ci
            state = verify_oneci_mtn_ci(trx) 
            if len(state) == 0 :
                start_time  =time.time()
                #insert trx in operator table
                for x in trx :
                    x['telephone'] = str(x['telephone']).replace('225','')
                    x['EndDateTime'] = x['EndDateTime'].split('.')[0]
                    x['EndDateTime'] = x['EndDateTime'].replace('/','-')
                    insert_operator_trx_oneci_mtn(x)
        
                failed_trx = Cinetpay_transaction_failed_oneci_mtn(debut_obj,fin_obj)  # recover failed transactions from Cinetay
                success_trx = Cinetpay_transaction_success_oneci_mtn(debut_obj, fin_obj)  # recover successfuly transactions from Cinetay
                # insert failed transactions from Cinetay in DB----------
                for x in failed_trx :
                    insert_failed_trx(x)
                #---------------------------------------------------------
                # insert successfuly transactions from Cinetay in DB------
                for x in success_trx :
                    insert_success_trx(x)
                #---------------------------------------------------------

                difference = match_table() #match operator trx and CinetpaySucessfuly trx and return difference
                #insert trx in difference table
                for x in difference :
                    insert_difference(x)
                # Detect each correspondent of trx in difference
                detect_correspondent()
                end_time = time.time()
                print("Time for reconciling : %ssecs" % (end_time-start_time) )

                data = TrxRightCorrespodent.objects.all()
                operatorAmount = TrxOperateur.objects.aggregate(Sum('montant'))
                CinetpayAmount = TrxSuccessCinetpay.objects.aggregate(Sum('Montant'))
                print(operatorAmount)
                diffAmount = operatorAmount['montant__sum'] - CinetpayAmount['Montant__sum']
                diff = TrxDifference.objects.all()
                countOperator= TrxOperateur.objects.all().count()
                countCinetpay = TrxSuccessCinetpay.objects.all().count()
                diffCount = countOperator - countCinetpay
                
                trx = {
                    'correspondent': data, 
                    'difference':diff,
                    'total':operatorAmount,
                    'montantCinetpay':CinetpayAmount,
                    'diffMontant':diffAmount,
                    'countOperator':countOperator,
                    'countCinetpay':countCinetpay,
                    'diffCount':diffCount 
                }
                
                return render(request, 'reconcile/display.html',trx)
            else :
                return render(request, 'reconcile/error.html',{'file':trx,'etat':state})
        # if operator == '7':
        #     moov_ci(request)
        # if operator == '8' :
        #     ddva_moov_ci(request)
        # if operator == '9' :
        #     oneci_moov_ci(request)
        # if operator == '10' :
        #     ddva_visa(request) :
        # if operator == '11' :
        #     oneci_visa(request)
        # if operator == '12' :
        #     orange_senegal(request)
        # if operator == '13' :
        #     free_senegal(request)
        # if operator == '14' :
        #     mtn_cameroun(request)
        # if operator == '15' :
        #     orange_cameroun(request)
        # if operator == '16' :
        #     orange_burkina(request)
        # if operator == '17' :
        #     moov_burkina(request) 
        # if operator == '18' :
        #     moov_togo(request)
        # if operator == '19' :
        #     orange_rdc(request)
    return render(request, 'reconcile/excel_to_json.html')


    # GENERAL ***********************************************************************************************************************************


