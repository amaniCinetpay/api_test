
from django.contrib.auth import authenticate
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import OperateurSerializer, PostSerializer, TacheSerializer, TrxCinetpaySerializer,TrxDifferenceSerializer,TrxRightCorrespodentSerializer,TrxOperateurSerializer,TrxreconciledSerializer,TrxRightCorrespodentDdvaVisaSerializer,TrxDifferenceDdvaVisaSerializer
from .models import Operateur, Post, Tache,TrxDifference,TrxOperateur,TrxRightCorrespodent,TrxFailedCinetpay,TrxCinetpay,TrxSuccessCinetpay,TrxCorrespondent, Trxreconciled,TrxNonereconciled,TrxDifferenceDdvaVisa,TrxNonereconciledDdvaVisa,TrxreconciledDdvaVisa,TrxRightCorrespodentDdvaVisa,TrxRightCorrespodentDdvaVisa,TrxDdvaVisa
from rest_framework.permissions import IsAuthenticated
from datetime import datetime, date
import time
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status 
from braces.views import CsrfExemptMixin
from django.db.models import Sum,Avg
import string
from .core import *
from api_test import core
from . import core
from .config import *
from copy import deepcopy

from api_test import models
# Create your views here.



class OperateurView(generics.ListCreateAPIView):
    serializer_class = OperateurSerializer
    queryset = Operateur.objects.all()

class OperateurRUD(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OperateurSerializer
    queryset = Operateur.objects.all()



class TacheView(generics.ListCreateAPIView):
    serializer_class = TacheSerializer
    queryset = Tache.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TacheRUD(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TacheSerializer
    queryset = Tache.objects.all()


class Test_view(APIView):

    # permission_classes = (IsAuthenticated, )
    def get(self, request, *args, **kwargs) :
        qs = Post.objects.all()
        serializer = PostSerializer(qs, many=True)
        return Response(serializer.data)
        
    def post(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data['data']['data']) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data )
        
        return Response(serializer.errors)

    # def post(self, request, *args, **kwargs):
    #     serializer = TrxCinetpaySerializer(data=request.data['data']['data']) 
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data )

    #     return Response(serializer.errors)

 

class Reconcile(APIView):

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get(self, request, *args, **kwargs) :
        choice = request.query_params['choix']
        operator = request.query_params['operateur']
        start = request.query_params['debut']
        end = request.query_params['fin']
        start_obj = datetime.strptime(start, "%Y-%m-%dT%H:%M")
        end_obj = datetime.strptime(end, "%Y-%m-%dT%H:%M")
        consultation = []
        if choice == '1' : # consult reconciled transaction
            if operator == '1': # ORANGE CI  
                all_trx = Trxreconciled.objects.filter(account = '0759062996')
                consultation = consult_trx(start_obj,end_obj,all_trx,operator)
                return Response({'reconciled':consultation}, status=status.HTTP_200_OK)
            elif operator == '2' : #DDVA ORANGE 
                all_trx = Trxreconciled.objects.filter(account = '0789248344')
                consultation = consult_trx(start_obj,end_obj,all_trx,operator)
                return Response({'reconciled':consultation}, status=status.HTTP_200_OK)
            elif operator == '3': # ONECI ORANGE CI
                all_trx = Trxreconciled.objects.filter(account = '0748884654')
                consultation = consult_trx(start_obj,end_obj,all_trx,operator)
                return Response({'reconciled':consultation}, status=status.HTTP_200_OK)
            elif operator == '4': # ORANGE SENEGAL
                all_trx = Trxreconciled.objects.filter(account = '786442199')
                consultation = consult_trx(start_obj,end_obj,all_trx,operator)
                return Response({'reconciled':consultation}, status=status.HTTP_200_OK)
            elif operator == '5':  # Orange Cameroun
                all_trx = Trxreconciled.objects.filter(account = '657986833')
                consultation = consult_trx(start_obj,end_obj,all_trx,operator)
                return Response({'reconciled':consultation}, status=status.HTTP_200_OK)
            elif operator == '6':  # mtnci
                all_trx = Trxreconciled.objects.filter(account = 'CINETPAY')
                consultation = consult_trx(start_obj,end_obj,all_trx,operator)
                return Response({'reconciled':consultation}, status=status.HTTP_200_OK)
            elif operator == '7':   # oneci mtn
                all_trx = Trxreconciled.objects.filter(account = 'ONECI')
                consultation = consult_trx(start_obj,end_obj,all_trx,operator)
                return Response({'reconciled':consultation}, status=status.HTTP_200_OK)
            else :
                return Response({'operator':'doesn\'t exist'}, status=status.HTTP_404_NOT_FOUND)
            
        elif choice == '2':   # consult not reconciled transaction
            if operator == '1': # ORANGE CI  
                all_trx = TrxNonereconciled.objects.filter(account = '0759062996')
                consultation = consult_trx(start_obj,end_obj,all_trx,operator)
                return Response({'Not reconciled':consultation}, status=status.HTTP_200_OK)
            if operator == '2' : #DDVA ORANGE 
                all_trx = TrxNonereconciled.objects.filter(account = '0789248344')
                consultation = consult_trx(start_obj,end_obj,all_trx,operator)
                return Response({' Not reconciled':consultation}, status=status.HTTP_200_OK)
            if operator == '3': # ONECI ORANGE CI
                all_trx = TrxNonereconciled.objects.filter(account = '0748884654')
                consultation = consult_trx(start_obj,end_obj,all_trx,operator)
                return Response({'Not reconciled':consultation}, status=status.HTTP_200_OK)
            elif operator == '4': # ORANGE SENEGAL
                all_trx = TrxNonereconciled.objects.filter(account = '786442199')
                consultation = consult_trx(start_obj,end_obj,all_trx,operator)
                return Response({' Not reconciled':consultation}, status=status.HTTP_200_OK)
            elif operator == '5':  # Orange Cameroun
                all_trx = TrxNonereconciled.objects.filter(account = '657986833')
                consultation = consult_trx(start_obj,end_obj,all_trx,operator)
                return Response({'Not reconciled':consultation}, status=status.HTTP_200_OK)
            elif operator == '6':  # mtnci
                all_trx = TrxNonereconciled.objects.filter(account = 'CINETPAY')
                consultation = consult_trx(start_obj,end_obj,all_trx,operator)
                return Response({'Not reconciled':consultation}, status=status.HTTP_200_OK)
            elif operator == '7':   # oneci mtn
                all_trx = TrxNonereconciled.objects.filter(account = 'ONECI')
                consultation = consult_trx(start_obj,end_obj,all_trx,operator)
                return Response({'Not reconciled':consultation}, status=status.HTTP_200_OK)
            else :
                return Response({'operator':'doesn\'t exist'},status=status.HTTP_404_NOT_FOUND)
        else :
            return Response({'choice':'doesn\'t exist'},status=status.HTTP_404_NOT_FOUND)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        operator = request.POST.getlist('operateur')[0]
        transaction = request.POST['valeur']
        trx = json.loads(transaction)
        debut = request.POST['debut']
        fin = request.POST['fin']
        
       

        # operator = request.data['operateur']
        # debut = request.data['debut']
        # fin = request.data['fin']
        debut_obj = datetime.strptime(debut, "%Y-%m-%dT%H:%M")
        fin_obj = datetime.strptime(fin, "%Y-%m-%dT%H:%M")

        compte = '0000000000'
        # agent = request.data['agent']
        agent = request.user


        print(operator)


        
        for config in CONFIG : #CONFIG comes from config
            if operator in config["operators"] : # all orange payment except OMBF
                CONFIG_OPERATOR = config["config"]
                INDEXES = config["index"]
                
                # required_state = verify_type_from_config(config)
                # try :
                #     assert len(required_state) == 0
                # except AssertionError :
                #     return Response({"required_field_in_config" : required_state})
                # verify = getattr( core , "verify_" + config["operatorName"])
                field = get_field_from_config(config)
                state = verify_index_from_config(trx, field)

                # state = verify(request.data['data'])
                # data = request.data['data']
                data = trx

                if len(state) == 0 :
                    # Créer les variables
                    date = datetime.now()

                    operateur = Operateur.objects.get(code=operator) 



                    index_ = {}
                    for item in INDEXES.keys() :
                        index_["index_"+item] = INDEXES[item]["fileIndex"]
                    try :
                        compte = trx[0][index_["index_account"]]
                    except IndexError :
                        return Response(
                            {
                                "account":"doesn't exist"
                            }
                        )
                    start_time  =time.time()
                    # file_treatment = getattr(core, "file_treatment_" + config["operatorName"])
                    #treat and insert trx from operator 
                    # file_treatment(request.data['data'],debut,agent)
                    for item, value in INDEXES.items() :
                        try :
                            treatment_data = getattr(core, "treatment_"+item)
                            kwargs = deepcopy(value)
                            try :
                                del kwargs["description"]
                            except Exception :
                                pass
                            treatment_data(data, **kwargs)
                        except AttributeError :
                            pass
                        except Exception as e:
                            raise e
                    try :
                        join_date_and_time(data, index_["index_date"], index_["index_time"] )
                    except Exception as e :
                        pass
                    print(compte)
                    print(operator)
                    

                    found = False
                    item = CONFIG_OPERATOR[operator]
                    if item["account"] == compte : 
                        print('jgfkhfhhgggggggg')     
                        tache = Tache.objects.create(
                            libelle='tache #{}'.format(date), 
                            description='', 
                            dateDebut=debut_obj, 
                            dateFin=fin_obj,
                            owner=request.user, 
                            operateur=operateur
                            )
                        save_file(data, agent.username, index_, tache)
                        execute_reoncile()

                        found = True
                        # a = {}
                        # start_treatment(item,a)
                        # all_failed_trx =  TrxCinetpay.objects.filter(**a)
                        # all_failed_trx = all_failed_trx.exclude(cpm_trans_status__contains="SUCCES")
                        # a["cpm_trans_status"] = "SUCCES"
                        # all_sucess_trx = TrxCinetpay.objects.filter(**a)

                        # if len(item["exclude"]) > 0 :
                        #     for exclusion in item["exclude"] :
                        #         a = {}
                        #         try :
                        #             a["payment_method__contains"] = exclusion["paymentMethod"]
                        #         except KeyError :
                        #             pass
                        #         try :
                        #             a["marchand__contains"] = exclusion["merchant"]
                        #         except KeyError :
                        #             pass
                        #         try :
                        #             a["NomDuService__contains"] = exclusion["service"]
                        #         except KeyError :
                        #             pass
                        #         all_failed_trx = all_failed_trx.exclude(**a)
                        #         all_sucess_trx = all_sucess_trx.exclude(**a)
                        # failed_trx = Cinetpay_transaction_failed(debut_obj,fin_obj,all_failed_trx)  # recover failed transactions from Cinetay
                        # success_trx = Cinetpay_transaction_success(debut_obj, fin_obj,all_sucess_trx)  # recover successfuly transactions from Cinetay
                    
                    if found == False :  
                        TrxOperateur.objects.filter().delete() 
                        return Response({'operator':'invalid'}, status=status.HTTP_406_NOT_ACCEPTABLE)
                    # second_treatment(failed_trx,success_trx,compte,agent,tache)
                    # difference = match_table(compte,agent) #match operator trx and CinetpaySucessfuly trx and return difference
                    # if len(difference) == 0 :
                    #     information  = third_treatment(agent,compte) 
                    #     return Response(information , status=status.HTTP_200_OK)
                    # information = forth_treament(difference,compte,agent,tache)
                    # end_time = time.time()
                    # # notification(request.user)
                    # notification(request.user)
                    # print("Time for reconciling : %ssecs" % (end_time-start_time) )
                    return Response({"resultat" : "La demande de traitement a été enregistrée avec succès. Nous vous notifierons le résultat à la fin du traitement."}, status=status.HTTP_200_OK)
                elif len(state) == len(trx) :
                    return Response({'file':'the headers do not match'}, status=status.HTTP_406_NOT_ACCEPTABLE)
                else :
                    return Response({'file':'empty','problem to line ':state}, status=status.HTTP_406_NOT_ACCEPTABLE)
        if operator == 'ddva_visa' : #ddva_visa  
            state = verify_ddva_visa(request.data['data'])
            if len(state) == 0 : 
                start_time  =time.time()
                #treat and insert trx from operator
                file_treatment_ddva_visa(request.data['data'],debut,agent)
                compte = request.data['data'][0]['ID du marchand']
                all_failed_trx =  TrxCinetpay.objects.filter(payment_method="DDVAVISAM").exclude(cpm_trans_status__contains="SUCCES")
                all_sucess_trx = TrxCinetpay.objects.filter(cpm_trans_status="SUCCES",payment_method="DDVAVISAM")
                failed_trx = Cinetpay_transaction_failed(debut_obj,fin_obj,all_failed_trx)  # recover failed transactions from Cinetay
                success_trx = Cinetpay_transaction_success(debut_obj, fin_obj,all_sucess_trx)  # recover successfuly transactions from Cinetay 
                # insert failed transactions from Cinetay in DB----------
                for x in failed_trx :
                    insert_failed_trx(x,compte,agent)
                #---------------------------------------------------------
                # insert successfuly transactions from Cinetay in DB------
                for x in success_trx :
                    insert_success_trx(x,compte,agent)
                #---------------------------------------------------------
                difference = match_table_ddva_visa() #match DDVA VISA trx and CinetpaySucessfuly trx and return difference    
                if len(difference) == 0 :
                    countOperator= TrxDdvaVisa.objects.filter(account= compte,agent =agent ).count()
                    countCinetpay = TrxSuccessCinetpay.objects.filter(account= compte, agent=agent).count()
                    diffCount = countOperator - countCinetpay
                    operatorA = TrxDdvaVisa.objects.filter(agent =agent ,account = compte)
                    CinetpayA = TrxSuccessCinetpay.objects.filter(account= compte, agent=agent)
                    operatorAmount = 0
                    for t in operatorA :
                        if t.amount != '-' :
                            t.amount = t.amount.translate({ord(c): None for c in string.whitespace})
                            print(t.amount)
                            operatorAmount += int(t.amount)
                    print(operatorAmount)
                    CinetpayAmount = 0
                    for t in CinetpayA :
                        if t.cpm_amount != '-' :
                            CinetpayAmount += int(t.cpm_amount)
                    print(CinetpayAmount)
                    diffAmount = operatorAmount - CinetpayAmount
                    TrxDdvaVisa.objects.filter(account= compte,agent=agent ).delete()
                    TrxSuccessCinetpay.objects.filter(account= compte,agent=agent).delete()
                    TrxFailedCinetpay.objects.filter(account= compte,agent=agent).delete()
                    TrxDifferenceDdvaVisa.objects.filter(account= compte,agent=agent).delete()
                    TrxCorrespondent.objects.filter(account= compte,agent=agent).delete()
                    TrxRightCorrespodentDdvaVisa.objects.filter(account= compte,agent=agent).delete()
                    print(TrxCinetpay.objects.filter(payment_method='DDVAVISAM').count())
                    information = {
                        'difference': 0,
                        'montantOperateur':operatorAmount,
                        'montantCinetpay':CinetpayAmount,
                        'diffMontant':diffAmount,
                        'countOperator':countOperator,
                        'countCinetpay':countCinetpay,
                        'diffCount':diffCount 
                    }
                    return Response(information , status=status.HTTP_200_OK)
                #insert trx in difference table 
                for x in difference :
                    insert_difference_ddva_visa(x,compte,agent)
                # Detect each correspondent of trx in difference
                detect_correspondent_ddva_visa(compte,agent)
                end_time = time.time()
                print("Time for reconciling : %ssecs" % (end_time-start_time) )
                # operatorAmount = TrxOperateur.objects.aggregate(Sum('amount'))
                # CinetpayAmount = TrxSuccessCinetpay.objects.aggregate(Sum('amount'))
                # print(CinetpayAmount,operatorAmount)
                # diffAmount = operatorAmount['montant__avg'] - CinetpayAmount['Montant__avg']
                diff = TrxDifferenceDdvaVisa.objects.filter(agent=agent,account = compte)
                diffSerialiser = TrxDifferenceDdvaVisaSerializer(diff, many=True)
                countOperator= TrxDdvaVisa.objects.filter(agent =agent ,account = compte).count()
                countCinetpay = TrxSuccessCinetpay.objects.filter(account= compte, agent=agent).count()
                diffCount = countOperator - countCinetpay
                operatorA = TrxDdvaVisa.objects.filter(agent =agent ,account = compte)
                CinetpayA = TrxSuccessCinetpay.objects.filter(account= compte, agent=agent)
                operatorAmount = 0
                for t in operatorA :
                    if t.amount != '-' :
                        t.amount = t.amount.translate({ord(c): None for c in string.whitespace})
                        operatorAmount += int(t.amount)
                print(operatorAmount)
                CinetpayAmount = 0
                for t in CinetpayA :
                    if t.cpm_amount != '-' :
                        CinetpayAmount += int(t.cpm_amount)
                print(CinetpayAmount)
                # TrxCinetpay.objects.filter(payment_method='DDVAVISAM').delete()
                # print(TrxCinetpay.objects.filter(payment_method='DDVAVISAM').count())
                diffAmount = operatorAmount - CinetpayAmount
                # b = TrxCorrespondentSerializer(qs, many=True)
                
                qs = TrxRightCorrespodentDdvaVisa.objects.filter(agent=agent,account = compte)
                serializer = TrxRightCorrespodentDdvaVisaSerializer(qs, many=True)
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
                return Response(information, status=status.HTTP_200_OK)
            elif len(state) == len(request.data['data']['data']) :
                return Response({'file':'the headers do not match'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            else :
                return Response({'file':'empty','problem to line ':state}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else :
            print("test")
            return Response({'operator':'doesn\'t exist'}, status=status.HTTP_404_NOT_FOUND)




    def put(self, request, *args, **kwargs) :
        agent = request.data['agent']
        compte = request.data['compte']
        rightCorresp = TrxRightCorrespodent.objects.filter(agent = agent,account=compte)
        NoneCorresp = TrxDifference.objects.filter(agent= agent,account = compte)
        # insert none reconciled transaction
        for x in NoneCorresp :
            insert_none_reconciled_trx(x)
        # Update  transaction from cinetpay database
        for x in rightCorresp :    
            TrxCinetpay.objects.filter(cel_phone_num=x.cel_phone_numCorrespondant,cpm_amount=x.AmountCorrespodent,cpm_trans_id=x.cpm_trans_idCorrespondent).update(cpm_payment_date=x.payment_date,cpm_trans_status="SUCCES",cpm_payid=x.payid)
        # insert  reconciled transaction
        final = TrxRightCorrespodent.objects.filter(agent = agent,account=compte)
        for x in final :
            insert_reconciled_trx(x)
        qs = Trxreconciled.objects.filter(  agent=agent)
        serializer = TrxreconciledSerializer(qs,many=True)
        # clean tables
        TrxOperateur.objects.filter(account= compte,agent=agent ).delete()
        TrxSuccessCinetpay.objects.filter(account= compte,agent=agent).delete()
        TrxFailedCinetpay.objects.filter(account= compte,agent=agent).delete()
        TrxDifference.objects.filter(account= compte,agent=agent).delete()
        TrxCorrespondent.objects.filter(account= compte,agent=agent).delete()
        TrxRightCorrespodent.objects.filter(account= compte,agent=agent).delete()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
            

class Catered(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    @csrf_exempt
    def post(self,request,*args,**kwargs):
        start_time = time.time()
        # return Response(json.dumps(request.data))
        item =request.data['item']
        id_tache =request.data['id_tache']
        tache = Tache.objects.get(pk=id_tache)
        debut_obj =tache.dateDebut
        fin_obj = tache.dateFin
        compte = tache.operateur.account
        agent = tache.owner

        a = {}
        start_treatment(item,a)
        all_failed_trx =  TrxCinetpay.objects.filter(**a)
        all_failed_trx = all_failed_trx.exclude(cpm_trans_status__contains="SUCCES")
        a["cpm_trans_status"] = "SUCCES"
        all_sucess_trx = TrxCinetpay.objects.filter(**a)

        if len(item["exclude"]) > 0 :
            for exclusion in item["exclude"] :
                a = {}
                try :
                    a["payment_method__contains"] = exclusion["paymentMethod"]
                except KeyError :
                    pass
                try :
                    a["marchand__contains"] = exclusion["merchant"]
                except KeyError :
                    pass
                try :
                    a["NomDuService__contains"] = exclusion["service"]
                except KeyError :
                    pass
                all_failed_trx = all_failed_trx.exclude(**a)
                all_sucess_trx = all_sucess_trx.exclude(**a)
        # failed_trx = Cinetpay_transaction_failed(debut_obj,fin_obj,all_failed_trx)  # recover failed transactions from Cinetay
        failed_trx = all_failed_trx.filter(created_at__gt = debut_obj).filter(created_at__lt = fin_obj)  # recover failed transactions from Cinetay
        # success_trx = Cinetpay_transaction_success(debut_obj, fin_obj,all_sucess_trx)  # recover successfuly transactions from Cinetay
        success_trx = all_sucess_trx.filter(created_at__gt = debut_obj).filter(created_at__lt = fin_obj)  # recover successfuly transactions from Cinetay
        second_treatment(failed_trx,success_trx,compte,agent.username,tache)
        difference = match_table(compte,agent.username) #match operator trx and CinetpaySucessfuly trx and return difference
        if len(difference) == 0 :
            information  = third_treatment(agent.username,compte,tache) 
            return Response(information , status=status.HTTP_200_OK)
        information = forth_treament(difference,compte,agent.username,tache)
        end_time = time.time()
        # notification(request.user)
        # notification(request.user)
        print("Time for reconciling : %ssecs" % (end_time-start_time) )
        return Response(information, status=status.HTTP_200_OK)

        













class Cinetpay(APIView) :
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get(self,request, *args, **kwargs) :
        print('voici le parametre',request.query_params['operateur'])
        qs = TrxRightCorrespodent.objects.all()
        serializer = TrxRightCorrespodentSerializer(qs, many=True)
        return Response(serializer.data)
    #orangeCi
    def post(self, request, *args, **kwargs):
        start_time  =time.time()
        for x in request.data:
            serializer = TrxCinetpaySerializer(data=x)
            if serializer.is_valid():
                serializer.save()
            else :
                return Response(serializer.errors)
        end_time = time.time()
        print("Time for reconciling : %ssecs" % (end_time-start_time) )
        return Response({'sucess':'ok'})
    #ddva orangeCi
    # def post(self, request, *args, **kwargs):
    #     for x in request.data['data'] :
    #         # x['cel_phone_num'] = str(x['cel_phone_num']).replace('225','')
    #         x['created_at'] = x['created_at'].replace('27/05/2021 ','2021-05-27')
    #         x['cpm_payment_date'] = x['cpm_payment_date'].replace('27/05/2021 ','2021-05-27')
    #         serializer = TrxCinetpaySerializer(data=x)
    #         if serializer.is_valid():
    #             serializer.save()
    #         else :
    #             return Response(serializer.errors)
    #     return Response({'sucess':'ok'})
        