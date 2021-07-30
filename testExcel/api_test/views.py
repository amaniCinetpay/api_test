
from django.contrib.auth import authenticate
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import OperateurSerializer,ProfileSerializer, PostSerializer, TacheSerializer, TrxCinetpaySerializer,TrxDifferenceSerializer,TrxRightCorrespodentSerializer,TrxOperateurSerializer,TrxreconciledSerializer,TacheSerializer,TrxRightCorrespodentDdvaVisaSerializer,TrxDifferenceDdvaVisaSerializer
from .models import Operateur,Profile, Post,Role, User,Tache,TrxDifference,TrxOperateur,TrxRightCorrespodent,TrxFailedCinetpay,TrxCinetpay,TrxSuccessCinetpay,TrxCorrespondent, Trxreconciled,TrxNonereconciled,TrxDifferenceDdvaVisa,TrxNonereconciledDdvaVisa,TrxreconciledDdvaVisa,TrxRightCorrespodentDdvaVisa,TrxRightCorrespodentDdvaVisa,TrxDdvaVisa
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
from django.db.models import Sum,Avg, Q
import string
from django.core import serializers
from .core import *
from api_test import core
from . import core
from .config import *
from .constantes import *
from copy import deepcopy
from multiprocessing import Process
from api_test import models
from oauth2_provider.models import AccessToken
import datetime

# Create your views here.



class OperateurView(generics.ListCreateAPIView):
    serializer_class = OperateurSerializer
    queryset = Operateur.objects.all()

class OperateurRUD(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OperateurSerializer
    queryset = Operateur.objects.all()

class ProfileView(generics.ListCreateAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()



class TokenView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    
    def post(self, request, *args, **kwargs):
        print(request.user)
        #access_token = AccessToken.objects.get(token=request.data['token'])
        #user = access_token.user
        user = request.user
        nom = user.last_name
        prenom = user.first_name
        username = user.username
        email = user.email
       
        qs = Profile.objects.filter(user=user)
        serializer = ProfileSerializer(qs, many=True)
        print(serializer.data[0]['id'])
        role = Role.objects.get(pk=serializer.data[0]['role'])
        try :

            details = {
            'nom':nom,
            'prenom':prenom,
            'email':email,
            'usename':username,
            'role': {
                'id': serializer.data[0]['id'],
                'libelle':role.libelle,
                'parent':role.parent.id
            }
           
        }
        
        except AttributeError :
            
            details = {
            'nom':nom,
            'prenom':prenom,
            'email':email,
            'usename':username,
            'role': {
                'id': serializer.data[0]['id'],
                'libelle':role.libelle,
                'parent':None
            }
           
        }

    
        return Response({'profile':serializer.data,'details':details})

    


class ProfileRUD(generics.RetrieveUpdateDestroyAPIView):
        serializer_class = ProfileSerializer
        queryset = Profile.objects.all()



class TrxWithCorrespondent(generics.RetrieveUpdateDestroyAPIView):
    
    serializer_class = OperateurSerializer
    queryset = Operateur.objects.all()
    
    def retrieve(self, request, *args, **kwargs):
        print(kwargs['pk'])
        tache = Tache.objects.get(pk=kwargs['pk'])       
        qs = TrxRightCorrespodent.objects.filter(tache = tache)
        serializer = TrxRightCorrespodentSerializer(qs, many=True)    
        # task = Tache.objects.filter(pk=kwargs['pk'])
        # dt = serializers.serialize('json', qs)
        # dt = TacheSerializer(task)
    
        return  Response(serializer.data)





class TrxRightCorrespodentRUDView(generics.RetrieveUpdateDestroyAPIView): 
    serializer_class = TrxRightCorrespodentSerializer
    def get_queryset(self):
        return  TrxRightCorrespodent.objects.filter(tache=self.kwargs['tache_id'])
    

class TrxRightCorrespodentb(generics.ListCreateAPIView):
    serializer_class =TrxRightCorrespodentSerializer

    def get_queryset(self):
        return  TrxRightCorrespodent.objects.filter(tache=self.kwargs['tache_id'])




class TrxDifferenceRUDView(generics.RetrieveUpdateDestroyAPIView):
    
    serializer_class = TrxDifferenceSerializer
    def get_queryset(self):
        return  TrxDifference.objects.filter(tache=self.kwargs['tache_id'])
    
    # def retrieve(self, request, *args, **kwargs):
    #     print(kwargs['pk'])
    #     tache = Tache.objects.get(pk=kwargs['pk'])
    #     diff = TrxDifference.objects.filter(tache = tache)
    #     diffSerialiser = TrxDifferenceSerializer(diff, many=True)       
        
    #     # task = Tache.objects.filter(pk=kwargs['pk'])
    #     # dt = serializers.serialize('json', qs)
    #     # dt = TacheSerializer(task)
    
    #     return  Response(diffSerialiser.data)


class TrxDifferenceView(generics.ListCreateAPIView):
    serializer_class = TrxDifferenceSerializer

    def get_queryset(self):
        return  TrxDifference.objects.filter(tache=self.kwargs['tache_id'])




class TacheView(generics.ListCreateAPIView):
    serializer_class = TacheSerializer
    #queryset = Tache.objects.filter(owner=request.user)
    def get_queryset(self):
        user = self.request.user
        
        kwargs = {}
        if 'opateur__pk' in self.request.GET :
            if self.request.GET['opateur__pk'] != None :
                kwargs["operateur__code"] = self.request.GET['opateur__pk']
        if 'dateDebut' in self.request.GET and self.request.GET['dateDebut'] != None :
            kwargs["dateDebut__gt"] = self.request.GET['dateDebut']
        if 'dateFin' in self.request.GET and self.request.GET['dateFin'] != None :
            kwargs["dateFin__lt"] = self.request.GET['dateFin']
        if 'etat' in self.request.GET and self.request.GET['etat']  != None :
            kwargs["etat"] = self.request.GET['etat']
        if 'fileName__icontains' in self.request.GET and self.request.GET['fileName__icontains']  != None :
            kwargs["fileName__icontains"] = self.request.GET['fileName__icontains']
        
        role = user.profile.role
        print(role)
        role_children = role.children.all()

        user_list = []

        for r in role_children:
            profiles = r.profile_set.all()
            for p in profiles:
                user_list.append(p.user)
        
        print(user_list)

        
        return  Tache.objects.filter((Q(owner=user) | Q(owner__in=user_list)), **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TacheRUD(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TacheSerializer
    queryset = Tache.objects.all()


class UpdateProfile(APIView) :

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def post(self,request,format=None):
        data = request.data
        id = data['id']
        if 'lastname' in data :
            User.objects.filter(pk=id).update(last_name=data['lastname'])
        if 'firstname' in data :
            User.objects.filter(pk=id).update(first_name=data['firstname'])
        if 'email' in data :
            User.objects.filter(pk=id).update(email = data['email'])
        if 'telephone' in data :
            Profile.objects.filter(pk=id).update(telephone=data['telephone'])
        if 'whatsapp' in data :
            Profile.objects.filter(pk=id).update(numero_whatsapp=data['whatsapp'])

        return Response('ok')

        # Profile.objects.filter(pk=pk).update(telephone=,numero_whatsapp,matricule)


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

    # def get(self, request, *args, **kwargs) :
    #     choice = request.query_params['choix']
    #     operator = request.query_params['operateur']
    #     start = request.query_params['debut']
    #     end = request.query_params['fin']
    #     start_obj = datetime.strptime(start, "%Y-%m-%dT%H:%M")
    #     end_obj = datetime.strptime(end, "%Y-%m-%dT%H:%M")
    #     consultation = []
    #     if choice == '1' : # consult reconciled transaction
    #         if operator == '1': # ORANGE CI  
    #             all_trx = Trxreconciled.objects.filter(account = '0759062996')
    #             consultation = consult_trx(start_obj,end_obj,all_trx,operator)
    #             return Response({'reconciled':consultation}, status=status.HTTP_200_OK)
    #         elif operator == '2' : #DDVA ORANGE 
    #             all_trx = Trxreconciled.objects.filter(account = '0789248344')
    #             consultation = consult_trx(start_obj,end_obj,all_trx,operator)
    #             return Response({'reconciled':consultation}, status=status.HTTP_200_OK)
    #         elif operator == '3': # ONECI ORANGE CI
    #             all_trx = Trxreconciled.objects.filter(account = '0748884654')
    #             consultation = consult_trx(start_obj,end_obj,all_trx,operator)
    #             return Response({'reconciled':consultation}, status=status.HTTP_200_OK)
    #         elif operator == '4': # ORANGE SENEGAL
    #             all_trx = Trxreconciled.objects.filter(account = '786442199')
    #             consultation = consult_trx(start_obj,end_obj,all_trx,operator)
    #             return Response({'reconciled':consultation}, status=status.HTTP_200_OK)
    #         elif operator == '5':  # Orange Cameroun
    #             all_trx = Trxreconciled.objects.filter(account = '657986833')
    #             consultation = consult_trx(start_obj,end_obj,all_trx,operator)
    #             return Response({'reconciled':consultation}, status=status.HTTP_200_OK)
    #         elif operator == '6':  # mtnci
    #             all_trx = Trxreconciled.objects.filter(account = 'CINETPAY')
    #             consultation = consult_trx(start_obj,end_obj,all_trx,operator)
    #             return Response({'reconciled':consultation}, status=status.HTTP_200_OK)
    #         elif operator == '7':   # oneci mtn
    #             all_trx = Trxreconciled.objects.filter(account = 'ONECI')
    #             consultation = consult_trx(start_obj,end_obj,all_trx,operator)
    #             return Response({'reconciled':consultation}, status=status.HTTP_200_OK)
    #         else :
    #             return Response({'operator':'doesn\'t exist'}, status=status.HTTP_404_NOT_FOUND)
            
    #     elif choice == '2':   # consult not reconciled transaction
    #         if operator == '1': # ORANGE CI  
    #             all_trx = TrxNonereconciled.objects.filter(account = '0759062996')
    #             consultation = consult_trx(start_obj,end_obj,all_trx,operator)
    #             return Response({'Not reconciled':consultation}, status=status.HTTP_200_OK)
    #         if operator == '2' : #DDVA ORANGE 
    #             all_trx = TrxNonereconciled.objects.filter(account = '0789248344')
    #             consultation = consult_trx(start_obj,end_obj,all_trx,operator)
    #             return Response({' Not reconciled':consultation}, status=status.HTTP_200_OK)
    #         if operator == '3': # ONECI ORANGE CI
    #             all_trx = TrxNonereconciled.objects.filter(account = '0748884654')
    #             consultation = consult_trx(start_obj,end_obj,all_trx,operator)
    #             return Response({'Not reconciled':consultation}, status=status.HTTP_200_OK)
    #         elif operator == '4': # ORANGE SENEGAL
    #             all_trx = TrxNonereconciled.objects.filter(account = '786442199')
    #             consultation = consult_trx(start_obj,end_obj,all_trx,operator)
    #             return Response({' Not reconciled':consultation}, status=status.HTTP_200_OK)
    #         elif operator == '5':  # Orange Cameroun
    #             all_trx = TrxNonereconciled.objects.filter(account = '657986833')
    #             consultation = consult_trx(start_obj,end_obj,all_trx,operator)
    #             return Response({'Not reconciled':consultation}, status=status.HTTP_200_OK)
    #         elif operator == '6':  # mtnci
    #             all_trx = TrxNonereconciled.objects.filter(account = 'CINETPAY')
    #             consultation = consult_trx(start_obj,end_obj,all_trx,operator)
    #             return Response({'Not reconciled':consultation}, status=status.HTTP_200_OK)
    #         elif operator == '7':   # oneci mtn
    #             all_trx = TrxNonereconciled.objects.filter(account = 'ONECI')
    #             consultation = consult_trx(start_obj,end_obj,all_trx,operator)
    #             return Response({'Not reconciled':consultation}, status=status.HTTP_200_OK)
    #         else :
    #             return Response({'operator':'doesn\'t exist'},status=status.HTTP_404_NOT_FOUND)
    #     else :
    #         return Response({'choice':'doesn\'t exist'},status=status.HTTP_404_NOT_FOUND)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        token = request.META['HTTP_AUTHORIZATION']
        # backoffice Cinetpay---------------------------
        data = json.loads(list(request.POST.keys())[0])
        operator = data['operateur']
        transaction = data['fichier']
        trx = json.loads(transaction)
        trx = trx[list(trx.keys())[0]]
       
        debut = data['dateDebut']
        fin = data['dateFin']
        fileName = data['fileName']
        task = Tache.objects.all()


        exist = False
        for x in task :
            if x.fileName == fileName :
                exist = True
                TreatedBy = x.owner.username
                break
        if exist != True :

    
            # backoffice Cinetpay---------------------------

            # my own interface------------------------------
            # token="Bearer fdkkkkkkkklllmdsgfndkggfgf"
            # operator = request.POST.getlist('operateur')[0]
            # transaction = request.POST['fichier']
            # trx = json.loads(transaction)
        
            # # debut = request.POST['debut']
            # # fin = request.POST['fin']
            # fileName = 'fichier essai'
            # my own interface------------------------------
        

            # operator = request.data['operateur']
            # debut = request.data['debut']
            # fin = request.data['fin']
            # debut_obj = datetime.strptime(debut, "%Y-%m-%dT%H:%M")
            # fin_obj = datetime.strptime(fin, "%Y-%m-%dT%H:%M")

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
                        date = datetime.datetime.now()

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
                        

                        found = False
                        item = CONFIG_OPERATOR[operator]
                        print(item["account"],compte,"ddddddddddddddddddddddddddddddddddddd")
                        if str(item["account"]) == str(compte) :
                            
                            tache = Tache.objects.create(
                                libelle='tache #{}'.format(date), 
                                description='', 
                                dateDebut= format(date), 
                                dateFin=format(date),
                                owner=request.user, 
                                operateur=operateur,
                                fileName= fileName
                                )
                            
                            
                                

                            default_date = "2050-05-04 23:00:00"
                            min_dat = datetime.datetime.strptime(default_date, '%Y-%m-%d %H:%M:%S')

                            default_dat = "1990-05-04 23:59:00"
                            max_dat = datetime.datetime.strptime(default_dat, '%Y-%m-%d %H:%M:%S')

                            date_table=save_file(data, agent.username, index_, tache,min_dat,max_dat,compte)
                            print('je veux rentre')
                        
                            
                            debut = date_table[0]
                            fin = date_table[1]
                            # debut = str(debut).split(' ')[0]+' 00:00'
                            # fin = str(fin).split(' ')[0]+' 23:59'
                            
                            minu = 1
                            minu_subtracted = datetime.timedelta(minutes=minu)
                            debut_obj = datetime.datetime.strptime(str(debut), '%Y-%m-%d %H:%M:%S')
                            debut_obj = debut_obj - minu_subtracted
                            fin_obj = datetime.datetime.strptime(str(fin), '%Y-%m-%d %H:%M:%S')
                            
                            Tache.objects.filter(pk=tache.id).update(dateDebut=debut_obj,dateFin=fin_obj)


                            execute_reconcile(item,tache.id,token)   
                            # p = Process(target=execute_reconcile, args=(item,tache,))
                            # p.start()
                            print('je suis passe')

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
                        details= {
                        'id':tache.id,
                        'fileName':tache.fileName,
                        'libelle':tache.libelle,
                        'description':tache.description,
                        'dateDebut':tache.dateDebut,
                        'dateFin':tache.dateFin,
                        'owner':tache.owner.username,
                        'operateur':tache.operateur.code,
                        'etat':tache.etat,
                        'dateCreation':tache.dateCreation,
                        'dateFinCollect':tache.dateFinCollect,
                        'dateUpdate':tache.dateUpdate,
                        'dateValidation' :tache.dateValidation,
                        'dateFinValidation':tache.dateFinValidation,
                        'montantOperateur':tache.montantOperateur,
                        'montantCinetpay':tache.montantCinetpay,
                        'diffMontant':tache.diffMontant,
                        'countOperator':tache.countOperator,
                        'countCinetpay':tache.countCinetpay,
                        'diffCount':tache.diffCount,
                        'montantOperateurAfter' :tache.montantOperateurAfter,
                        'montantCinetpayAfter':tache.montantCinetpayAfter,
                        'diffMontantAfter':tache.diffMontantAfter,
                        'countOperatorAfter':tache.countOperatorAfter,
                        'countCinetpayAfter':tache.countCinetpayAfter,
                        'diffCountAfter':tache.diffCountAfter,
                        'TrxReconciled':tache.TrxReconciled,
                        'TrxNonereconciled':tache.TrxNonereconciled
                         }
                        return Response({"resultat" : "La demande de traitement a été enregistrée avec succès. Nous vous notifierons le résultat à la fin du traitement.",'details':details}, status=status.HTTP_200_OK)
                    elif len(state) == len(trx) :
                        return Response({'file':'the headers do not match'}, status=status.HTTP_406_NOT_ACCEPTABLE)
                    else :
                        return Response({'file':'empty','problem to line ':state}, status=status.HTTP_406_NOT_ACCEPTABLE)
            if operator == 'DDVAVISA' : #ddva_visa  
                # operateur = Operateur.objects.get(code=operator) 
                # date = datetime.now()
                # tache = Tache.objects.create(
                #     libelle='tache #{}'.format(date), 
                #     description='', 
                #     dateDebut=debut_obj, 
                #     dateFin=fin_obj,
                #     owner=request.user, 
                #     operateur=operateur
                #     )
                # state = verify_ddva_visa(trx)
                
                state = verify_ddva_visa(trx)
        
                if len(state) == 0 : 
                    tache =start_treatment_ddva(operator,request,trx,fileName)
                    start_time  =time.time()



                    #treat and insert trx from operator
                    # file_treatment_ddva_visa(trx,debut,agent.username,tache)
                    # information = second_treatment_ddva(trx,debut_obj,fin_obj,agent,tache)
                
                    execute_reconcile_ddva(trx,tache.id,token)



            #         compte = trx[0]['ID du marchand']
            #         all_failed_trx =  TrxCinetpay.objects.filter(payment_method="DDVAVISAM").exclude(cpm_trans_status__contains="SUCCES")
            #         all_sucess_trx = TrxCinetpay.objects.filter(cpm_trans_status="SUCCES",payment_method="DDVAVISAM")
            #         # failed_trx = Cinetpay_transaction_failed(debut_obj,fin_obj,all_failed_trx)  # recover failed transactions from Cinetay
            #         # success_trx = Cinetpay_transaction_success(debut_obj, fin_obj,all_sucess_trx)  # recover successfuly transactions from Cinetay 
            #         failed_trx = all_failed_trx.filter(created_at__gt = debut_obj).filter(created_at__lt = fin_obj)  # recover failed transactions from Cinetay
            #         success_trx = all_sucess_trx.filter(created_at__gt = debut_obj).filter(created_at__lt = fin_obj) # recover successfuly transactions from Cinetay 
            #         # insert failed transactions from Cinetay in DB----------
            #         for x in failed_trx :
            #             insert_failed_trx(x,compte,agent.username,tache)
            #         #---------------------------------------------------------
            #         # insert successfuly transactions from Cinetay in DB------
            #         for x in success_trx :
            #             insert_success_trx(x,compte,agent.username,tache)
            #         #---------------------------------------------------------
            #         difference = match_table_ddva_visa(compte,agent.username) #match DDVA VISA trx and CinetpaySucessfuly trx and return difference    
            #         if len(difference) == 0 :
            #             Tache.objects.filter(pk=tache.id).update(etat=ETAT_TACHE[2][0])
            #             countOperator= TrxDdvaVisa.objects.filter(account= compte,agent =agent,tache=tache ).count()
            #             countCinetpay = TrxSuccessCinetpay.objects.filter(account= compte, agent=agent,tache=tache).count()
            #             diffCount = countOperator - countCinetpay
            #             operatorA = TrxDdvaVisa.objects.filter(agent =agent ,account = compte,tache=tache)
            #             CinetpayA = TrxSuccessCinetpay.objects.filter(account= compte, agent=agent,tache=tache)
            #             operatorAmount = 0
            #             for t in operatorA :
            #                 if t.amount != '-' :
            #                     t.amount = t.amount.translate({ord(c): None for c in string.whitespace})
            #                     print(t.amount)
            #                     operatorAmount += int(t.amount)
            #             print(operatorAmount)
            #             CinetpayAmount = 0
            #             for t in CinetpayA :
            #                 if t.cpm_amount != '-' :
            #                     CinetpayAmount += int(t.cpm_amount)
            #             print(CinetpayAmount)
            #             diffAmount = operatorAmount - CinetpayAmount
            #             TrxDdvaVisa.objects.filter(account= compte,agent=agent,tache=tache ).delete()
            #             TrxSuccessCinetpay.objects.filter(account= compte,agent=agent,tache=tache).delete()
            #             TrxFailedCinetpay.objects.filter(account= compte,agent=agent,tache=tache).delete()
            #             TrxDifferenceDdvaVisa.objects.filter(account= compte,agent=agent,tache=tache).delete()
            #             TrxCorrespondent.objects.filter(account= compte,agent=agent,tache=tache).delete()
            #             TrxRightCorrespodentDdvaVisa.objects.filter(account= compte,agent=agent,tache=tache).delete()
            #             print(TrxCinetpay.objects.filter(payment_method='DDVAVISAM').count())
            #             information = {
            #                 'difference': 0,
            #                 'montantOperateur':operatorAmount,
            #                 'montantCinetpay':CinetpayAmount,
            #                 'diffMontant':diffAmount,
            #                 'countOperator':countOperator,
            #                 'countCinetpay':countCinetpay,
            #                 'diffCount':diffCount 
            #             }
            #             # notification(request.user,tache.id)
            #             print(tache.id)
            #             return Response(information , status=status.HTTP_200_OK)
            #         #insert trx in difference table 
            #         for x in difference :
            #             insert_difference_ddva_visa(x,compte,agent.username,tache)
            #         # Detect each correspondent of trx in difference
            #         detect_correspondent_ddva_visa(compte,agent.username,tache)
            #         end_time = time.time()
            #         print("Time for reconciling : %ssecs" % (end_time-start_time) )
            #         # operatorAmount = TrxOperateur.objects.aggregate(Sum('amount'))
            #         # CinetpayAmount = TrxSuccessCinetpay.objects.aggregate(Sum('amount'))
            #         # print(CinetpayAmount,operatorAmount)
            #         # diffAmount = operatorAmount['montant__avg'] - CinetpayAmount['Montant__avg']
            #         Tache.objects.filter(pk=tache.id).update(etat=ETAT_TACHE[2][0])
            #         diff = TrxDifferenceDdvaVisa.objects.filter(agent=agent,account = compte)
            #         diffSerialiser = TrxDifferenceDdvaVisaSerializer(diff, many=True)
            #         countOperator= TrxDdvaVisa.objects.filter(agent =agent ,account = compte).count()
            #         countCinetpay = TrxSuccessCinetpay.objects.filter(account= compte, agent=agent).count()
            #         diffCount = countOperator - countCinetpay
            #         operatorA = TrxDdvaVisa.objects.filter(agent =agent ,account = compte)
            #         CinetpayA = TrxSuccessCinetpay.objects.filter(account= compte, agent=agent)
            #         operatorAmount = 0
            #         for t in operatorA :
            #             if t.amount != '-' :
            #                 t.amount = t.amount.translate({ord(c): None for c in string.whitespace})
            #                 operatorAmount += int(t.amount)
            #         print(operatorAmount)
            #         CinetpayAmount = 0
            #         for t in CinetpayA :
            #             if t.cpm_amount != '-' :
            #                 CinetpayAmount += int(t.cpm_amount)
            #         print(CinetpayAmount)
            #         # TrxCinetpay.objects.filter(payment_method='DDVAVISAM').delete()
            #         # print(TrxCinetpay.objects.filter(payment_method='DDVAVISAM').count())
            #         diffAmount = operatorAmount - CinetpayAmount
            #         # b = TrxCorrespondentSerializer(qs, many=True)
                    
            #         qs = TrxRightCorrespodentDdvaVisa.objects.filter(agent=agent,account = compte)
            #         serializer = TrxRightCorrespodentDdvaVisaSerializer(qs, many=True)
            #         information = {
            #             'With correspondent': serializer.data, 
            #             'Not correspondent':diffSerialiser.data,
            #             'montantOperateur':operatorAmount,
            #             'montantCinetpay':CinetpayAmount,
            #             'diffMontant':diffAmount,
            #             'countOperator':countOperator,
            #             'countCinetpay':countCinetpay,
            #             'diffCount':diffCount 
            #         }
        
            #         # notification(request.user,tache)
                    details= {
                        'id':tache.id,
                        'fileName':tache.fileName,
                        'libelle':tache.libelle,
                        'description':tache.description,
                        'dateDebut':tache.dateDebut,
                        'dateFin':tache.dateFin,
                        'owner':tache.owner.username,
                        'operateur':tache.operateur.code,
                        'etat':tache.etat,
                        'dateCreation':tache.dateCreation,
                        'dateFinCollect':tache.dateFinCollect,
                        'dateUpdate':tache.dateUpdate,
                        'dateValidation' :tache.dateValidation,
                        'dateFinValidation':tache.dateFinValidation,
                        'montantOperateur':tache.montantOperateur,
                        'montantCinetpay':tache.montantCinetpay,
                        'diffMontant':tache.diffMontant,
                        'countOperator':tache.countOperator,
                        'countCinetpay':tache.countCinetpay,
                        'diffCount':tache.diffCount,
                        'montantOperateurAfter' :tache.montantOperateurAfter,
                        'montantCinetpayAfter':tache.montantCinetpayAfter,
                        'diffMontantAfter':tache.diffMontantAfter,
                        'countOperatorAfter':tache.countOperatorAfter,
                        'countCinetpayAfter':tache.countCinetpayAfter,
                        'diffCountAfter':tache.diffCountAfter,
                        'TrxReconciled':tache.TrxReconciled,
                        'TrxNonereconciled':tache.TrxNonereconciled
                    }
                    
                    return Response({"resultat" : "La demande de traitement a été enregistrée avec succès. Nous vous notifierons le résultat à la fin du traitement.",'details':details}, status=status.HTTP_200_OK)
                elif len(state) == len(trx) :
                    return Response({'file':'entetes'}, status=status.HTTP_406_NOT_ACCEPTABLE)
                else :
                    return Response({'file':'empty','problem to line ':state}, status=status.HTTP_406_NOT_ACCEPTABLE)
            else :
                return Response({'operator':'doesn\'t exist'}, status=status.HTTP_404_NOT_FOUND)

        else :
            return Response({'existance':'exist','person':TreatedBy}, status=status.HTTP_406_NOT_ACCEPTABLE)


    def put(self, request,pk, *args, **kwargs) :
        agent = request.user
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
            



class ReconcileUpdate(APIView) :
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def put(self, request, pk, format=None):
        Tache.objects.filter(pk=pk).update(dateValidation=datetime.datetime.now())
       
        Tache.objects.filter(pk=pk).update(etat=ETAT_TACHE[3][0])
        tache = Tache.objects.get(pk=pk)
        rightCorresp = TrxRightCorrespodent.objects.filter(tache = tache)
        NoneCorresp = TrxDifference.objects.filter(tache = tache)
        # insert none reconciled transaction
        for x in NoneCorresp :
            insert_none_reconciled_trx(x,tache)
        # Update  transaction from cinetpay database


        countB = TrxDifference.objects.filter(tache = tache).count()
        countA = 0
        for x in rightCorresp : 
            if str(x.id) in request.data['ids'] :
                countB += 1
                print(x.id,"n'a pas subit de mise à jour")
            else :
                countA += 1
                insert_reconciled_trx(x,tache)
                TrxCinetpay.objects.filter(cel_phone_num=x.cel_phone_numCorrespondant,cpm_amount=x.AmountCorrespodent,cpm_trans_id=x.cpm_trans_idCorrespondent).update(cpm_payment_date=x.payment_date,cpm_trans_status="SUCCES",cpm_payid=x.payid)
                TrxRightCorrespodent.objects.filter(id = x.id).delete()

        # # insert  reconciled transaction
        final = TrxRightCorrespodent.objects.filter(tache=tache)
        for x in final :
            insert_reconciled_trx(x,tache)

        oldCountA = Tache.objects.get(pk=pk).TrxReconciled
        countA = countA + int(oldCountA)

        Tache.objects.filter(pk=pk).update(TrxReconciled=countA,TrxNonereconciled=countB)

     
                
      
        
    
        countOperator= TrxOperateur.objects.filter(tache= tache).count()
        operatorA = TrxOperateur.objects.filter(tache= tache)


        CinetpayAmount = 0
        countCinetpay = 0
        operatorAmount = 0

        for t in operatorA :
            dt = TrxCinetpay.objects.filter(cpm_payid=t.payid)
            for s in dt :
                try :
                    CinetpayAmount += int(s.cpm_amount)
                except ValueError as e :
                    print(e)
                    pass
                countCinetpay += 1
            try:
                operatorAmount += int(t.amount.split('.')[0])
            except ValueError as e :
                print(e)
                try : 
                    operatorAmount += int(t.amount.replace(',',''))
                except ValueError as r :
                    print(r)
                    pass
                
        diffCount = countOperator - countCinetpay
        print(operatorAmount,'equal',countOperator)   

        print(CinetpayAmount,'equal',countCinetpay)
        diffAmount = operatorAmount - CinetpayAmount
        Tache.objects.filter(pk=pk).update(dateFinValidation=datetime.datetime.now())
        Tache.objects.filter(pk=pk).update(etat=ETAT_TACHE[4][0])
        Tache.objects.filter(pk=pk).update(montantOperateurAfter=operatorAmount,montantCinetpayAfter=CinetpayAmount,diffMontantAfter=diffAmount,countOperatorAfter=countOperator,countCinetpayAfter=countCinetpay,diffCountAfter=diffCount)
            
        return Response({"update":"succes"}, status=status.HTTP_201_CREATED)








class CateredDdva(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    @csrf_exempt
    def post(self,request,*args,**kwargs):
        print('je traite à présent')
        trx =request.data['trx']
        id_tache =request.data['id_tache']
        tache = Tache.objects.get(pk=id_tache)
        # debut_obj =tache.dateDebut
        # fin_obj = tache.dateFin
        compte = tache.operateur.account
        agent = tache.owner
        Tache.objects.filter(pk=id_tache).update(etat=ETAT_TACHE[1][0])


        default_date = "2050-05-04 23:00:00"
        min_dat = datetime.datetime.strptime(default_date, '%Y-%m-%d %H:%M:%S')

        default_dat = "1990-05-04 23:59:00"
        max_dat = datetime.datetime.strptime(default_dat, '%Y-%m-%d %H:%M:%S')

        date_table=file_treatment_ddva_visa(trx,agent.username,tache,max_dat,min_dat)

        debut = date_table[0]
        fin = date_table[1]
        debut = str(debut).split(' ')[0]+' 00:00'
        fin = str(fin).split(' ')[0]+' 23:59'

        debut_obj = datetime.datetime.strptime(str(debut), '%Y-%m-%d %H:%M')
        fin_obj = datetime.datetime.strptime(str(fin), '%Y-%m-%d %H:%M')

        Tache.objects.filter(pk=id_tache).update(dateDebut=debut_obj,dateFin=fin_obj)
        information = second_treatment_ddva(trx,debut_obj,fin_obj,agent,tache)
        Tache.objects.filter(pk=id_tache).update(etat=ETAT_TACHE[2][0])
        notification(agent,tache.pk,information)
        
        return Response(information, status=status.HTTP_200_OK)







class Catered(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    @csrf_exempt
    def post(self,request,*args,**kwargs):
        print('je traite à présent')
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
        Tache.objects.filter(pk=id_tache).update(etat=ETAT_TACHE[1][0])
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
        second_treatment(failed_trx,success_trx,compte,agent,tache)
        difference = match_table(tache) #match operator trx and CinetpaySucessfuly trx and return difference

        if len(difference) == 0 :
            Tache.objects.filter(pk=id_tache).update(etat=ETAT_TACHE[4][0])
            Tache.objects.filter(pk=id_tache).update(etat=ETAT_TACHE[2][0])
            information  = third_treatment(agent,compte,tache) 
            return Response(information , status=status.HTTP_200_OK)
        else :
            information = forth_treament(difference,compte,agent,tache)
            end_time = time.time()
  
            Tache.objects.filter(pk=id_tache).update(etat=ETAT_TACHE[2][0]) 
            notification(agent,tache.pk,information)
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
    # def post(self, request, *args, **kwargs):
    #     start_time  =time.time()
    #     for x in request.data:
    #         serializer = TrxCinetpaySerializer(data=x)
    #         if serializer.is_valid():
    #             serializer.save()
    #         else :
    #             return Response(serializer.errors)
    #     end_time = time.time()
    #     print("Time for reconciling : %ssecs" % (end_time-start_time) )
    #     return Response({'sucess':'ok'})
    # ddva orangeCi
    def post(self, request, *args, **kwargs):
        # send_whatsApp()
        for x in request.data:
            # x['cel_phone_num'] = str(x['cel_phone_num']).replace('225','')
            x['created_at'] = x['created_at'].replace('27/05/2021 ','2021-05-27')
            x['cpm_payment_date'] = x['cpm_payment_date'].replace('27/05/2021 ','2021-05-27')
            serializer = TrxCinetpaySerializer(data=x)
            if serializer.is_valid():
                serializer.save()
            else :
                return Response(serializer.errors)
        return Response({'sucess':'ok'})
        



        