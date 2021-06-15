CONFIG = [
            {
                "operators" : ["OMCI", "DDVAOMCI", "OMONECI", "OMSN", "OMCM","OMRDC"],
                "operatorName" : "orange_ci",
                "typeOperator" : "Mobile Money",
                "index" : {
                    "date" : {
                        "fileIndex" : "Date",
                        "description" : "date",
                        "format" : "DD/mm/YYYY"
                    },
                    # "datetime" : {
                    #     "fileIndex" : "EndDateTime",
                    #     "description" : "date et heure",
                    #     "format" : "DD/mm/YYYY HH:MM:SS"
                    # },
                    "msisdn" : {
                        "fileIndex" : "Correspondant",
                        "description" : "numéro",
                        "indicative" : "225",
                        "digit" : 10,
                    },
                    "time" : {
                        "fileIndex" : "Heure",
                        "description" : "heure",
                        "format" : "HH:MM:SS",
                    },
                    "reference" : {
                        "fileIndex" : "Référence",
                        "description" : "Référence de paiement",
                    },
                    "status" : {
                        "fileIndex" : "Statut",
                        "type" : "status"
                    },
                    "amount" : { 
                        "fileIndex" : "Crédit",
                    },
                    # "idTransaction" : {
                    #     "fileIndex" : "idTransaction",
                    #     "descripttion" : "Id de la transaction",
                    # },
                    "account" : {
                        "fileIndex" : "Compte OM",
                        "descripttion" : "Compte de CinetPay chez l'opérateur",
                    }
                },
                
                "config" : {
                    "OMCI" :
                        {
                            "operator" : "OMCI",# orange_ci
                            "account" : "0759062996",
                            "paymentMethod" : "OM",
                            "exclude" : [
                                {
                                    "paymentMethod" : "DDVAOMCI",
                                    "merchant" : "DDVA",
                                    "serviceName" : "ONECI"
                                },
                                {
                                    "merchant" : "ONECI - RNPP"
                                }
                            ]
                        },
                    "DDVAOMCI" :  #ddva_orange
                        {
                            "account" : "0789248344",
                            "paymentMethod" : "DDVAOMCI",
                            "serviceName" : "DDVA",
                            "merchant" : "DDVA",
                            "exclude" : []
                        },
                    "OMONECI" : {
                        "operator" : "OMONECI", # oneci_orange_ci
                        "account" : "0748884654",
                        "paymentMethod" : "OM",
                        "serviceName" : "ONECI",
                        "merchant":"ONECI - RNPP",
                        "exclude" : []
                    },
                    "OMSN" : {
                        "operator" : "OMSN", # Orange Sénégal
                        "account" : "786442199",
                        "paymentMethod" : "OMSN",
                        "exclude" : []
                    },
                    "OMCM" : {
                        "operator" : "OMCM", # Orange Cameroun
                        "account" : "657986833",
                        "paymentMethod" : "OMCM",
                        "exclude" : []
                    },
                    "OMRDC" : {
                        "operator" : "OMRDC", # Orange RDC
                        "account" : "0899539928",
                        "paymentMethod" : "OMCD",
                        "exclude" : []
                    },
                }
            },
            {
                "operators" : ["MTNCI", "ONECIMTN"], # mtnci or mtn-oneci
                "operatorName" : "mtnci",
                "typeOperator" : "Mobile Money",
                "index" : {
                    "datetime" : {
                        "fileIndex" : "EndDateTime",
                        "description" : "date et heure",
                        "format" : "mm/DD/YYYY HH:MM:SS"
                    },
                    "msisdn" : {
                        "fileIndex" : "MSISDN",
                        "description" : "numéro",
                        "indicative" : "225",
                        "digit" : 10,
                    },
                    "reference" : {
                        "fileIndex" : "TransactionId",
                        "description" : "Référence de paiement",
                    },
                    "status" : {
                        "fileIndex" : "ResponseMessage",
                        "type" : "status"
                    },
                    "amount" : { 
                        "fileIndex" : "Amount",
                    },
                    "idTransaction" : {
                        "fileIndex" : "IdTransactionCP",
                        "descripttion" : "Id de la transaction",
                    },
                    "account" : {
                        "fileIndex" : "ServiceProviderCode",
                        "descripttion" : "Compte de CinetPay chez l'opérateur",
                    }
                },
                
                "config" : {
                    "MTNCI" :
                        {
                            # mtnci
                            "account" : "CINETPAY",
                            "paymentMethod" : "MOMO",
                            "serviceName" : "ONECI",
                            "exclude" : [
                                {
                                    "paymentMethod" : "DDVAMTNCI",
                                    "merchant" : "DDVA",
                                    "service" : "ONECI"
                                },
                                {
                                    "merchant" : "ONECI - RNPP"
                                }
                            ]
                        },
                    "ONECIMTN" :  # oneci_mtn
                        {
                            "account" : "ONECI",
                            "paymentMethod" : "MOMO",
                            "serviceName" : "ONECI",
                            "merchant" : "ONECI - RNPP",
                            "exclude" : []
                        },
                }
            },
            
            {
                "operators" : ["ONECIMOOV","MOOVCI"], #oneci_moov and moovci
                "operatorName" : "oneci_moov",
                "typeOperator" : "Mobile Money",
                "index" : {
                    "datetime" : {
                        "fileIndex" : "DATE",
                        "description" : "date et heure",
                        "format" : "YYYY-mm-DD HH:MM:SS"
                    },
                    "msisdn" : {
                        "fileIndex" : "S/D",
                        "description" : "numéro",
                        "indicative" : "225",
                        "digit" : 10,
                    },
                    "reference" : {
                        "fileIndex" : "RefID",
                        "description" : "Référence de paiement",
                    },
                    "status" : {
                        "fileIndex" : "STATUS",
                        "type" : "status"
                    },
                    "amount" : { 
                        "fileIndex" : "CR",
                    },
                    "account" : {
                        "fileIndex" : "COMPTE",
                        "descripttion" : "Compte de CinetPay chez l'opérateur",
                    }
                },
                
                "config" : {
                    "ONECIMOOV" : #oneci_moov
                        {
                            "account" : "ONECI",
                            "paymentMethod" : "FLOOZ",
                            "serviceName" : "ONECI",
                            "merchant":"ONECI - RNPP",
                            "exclude" : []
                        },
                    "MOOVCI" :  # moovci
                        {
                        "operator" : "MOOVCI",# moovci
                        "account" : "CINETPAY",
                        "paymentMethod" : "FLOOZ",
                        "exclude" : [
                            {
                                "paymentMethod" : "DDVAMOOVCI",
                                "merchant" : "DDVA",
                                "serviceName" : "ONECI"
                            },
                            {
                                "merchant" : "ONECI - RNPP"
                            }
                        ]
                    },
                }
            },
                   {
                "operators" : ["DDVAMOOVCI"], #ddva_moov
                "operatorName" : "DDVAMOOVCI",
                "typeOperator" : "Mobile Money",
                "index" : {
                    "datetime" : {
                        "fileIndex" : "TIMESTAMP",
                        "description" : "date et heure",
                        "format" : "DD-mm-YYYY  HH:MM:SS"
                    },
                    "msisdn" : {
                        "fileIndex" : "FRMSISDN",
                        "description" : "numéro",
                        "indicative" : "225",
                        "digit" : 10,
                    },
                    "reference" : {
                        "fileIndex" : "REFERENCEID",
                        "description" : "Référence de paiement",
                    },
                    "status" : {
                        "fileIndex" : "STATUS",
                        "type" : "status"
                    },
                    "amount" : { 
                        "fileIndex" : "AMOUNT",
                    },
                    "account" : {
                        "fileIndex" : "TOMSISDN",
                        "descripttion" : "Compte de CinetPay chez l'opérateur",
                    }
                },
                
                "config" : {
                    "DDVAMOOVCI" : #ddva_moov
                        {
                            "account" : "2250000000544",
                            "paymentMethod" : "DDVAMOOVCI",
                            "merchant":"DDVA",
                            "exclude" : []
                        },
                    }
            },
              {
                "operators" : ["DDVAMTNCI"], #ddva_mtnci
                "operatorName" : "DDVAMTNCI",
                "typeOperator" : "Mobile Money",
                "index" : {
                    "datetime" : {
                        "fileIndex" : "Date",
                        "description" : "date et heure",
                        "format" : "DD-mm-YYYY  HH:MM:SS"
                    },
                    "msisdn" : {
                        "fileIndex" : "Numero",
                        "description" : "numéro",
                        "indicative" : "225",
                        "digit" : 10,
                    },
                    "reference" : {
                        "fileIndex" : "Identifiant",
                        "description" : "Référence de paiement",
                    },
                    "status" : {
                        "fileIndex" : "Statut",
                        "type" : "status"
                    },
                    "amount" : { 
                        "fileIndex" : "Montant",
                    },
                    "account" : {
                        "fileIndex" : "Compte",
                        "descripttion" : "Compte de CinetPay chez l'opérateur",
                    }
                },
                
                "config" : {
                    "DDVAMTNCI" : #ddva_mtnci
                        {
                            "account" : "2250556810817",
                            "paymentMethod" : "DDVAMTNCI",
                            "merchant":"DDVA",
                            "exclude" : []
                        },
                    }
            },
            {
                "operators" : ["MOOVTG"], #moov_togo
                "operatorName" : "MOOVTG",
                "typeOperator" : "Mobile Money",
                "index" : {
                    "datetime" : {
                        "fileIndex" : "TRANSACTION DATE",
                        "description" : "date et heure",
                        "format" : "YYYY-mm-DD HH:MM:SS"
                    },
                    "msisdn" : {
                        "fileIndex" : "SOURCE",
                        "description" : "numéro",
                        "indicative" : "228",
                        "digit" : 10,
                    },
                    "reference" : {
                        "fileIndex" : "REFERENCE ID",
                        "description" : "Référence de paiement",
                    },
                    "status" : {
                        "fileIndex" : "STATUS",
                        "type" : "status"
                    },
                    "amount" : { 
                        "fileIndex" : "AMOUNT",
                    },
                    "account" : {
                        "fileIndex" : "DESTINATION",
                        "descripttion" : "Compte de CinetPay chez l'opérateur",
                    }
                },
                
                "config" : {
                    "MOOVTG" : #moov_togo
                        {
                            "account" : "22800000472",
                            "paymentMethod" : "FLOOZTG",
                            "exclude" : []
                        },
                    }
            },
             {
                "operators" : ["FREESN"], #free_senegal
                "operatorName" : "FREESN",
                "typeOperator" : "Mobile Money",
                "index" : {
                    "datetime" : {
                        "fileIndex" : "Transaction Date & Time",
                        "description" : "date et heure",
                        "format" : "DD-mm-YYYY  HH:MM:SS"
                    },
                    "msisdn" : {
                        "fileIndex" : "Payer Mobile Number",
                        "description" : "numéro",
                        "indicative" : "228",
                        "digit" : 10,
                    },
                    "reference" : {
                        "fileIndex" : "Transaction Id",
                        "description" : "Référence de paiement",
                    },
                    "status" : {
                        "fileIndex" : "Transaction Status",
                        "type" : "status"
                    },
                    "amount" : { 
                        "fileIndex" : "Transaction Amount",
                    },
                    "account" : {
                        "fileIndex" : "Payee Mobile Number",
                        "descripttion" : "Compte de CinetPay chez l'opérateur",
                    }
                },
                
                "config" : {
                    "FREESN" : #free_senegal
                        {
                            "account" : "762054568",
                            "paymentMethod" : "FREESN",
                            "exclude" : []
                        },
                    }
            },
             {
                "operators" : ["MTNCM"], #MTN_CM
                "operatorName" : "MTNCM",
                "typeOperator" : "Mobile Money",
                "index" : {
                    "datetime" : {
                        "fileIndex" : "Date",
                        "description" : "date et heure",
                        "format" : "DD-mm-YYYY  HH:MM:SS"
                    },
                    "msisdn" : {
                        "fileIndex" : "Number",
                        "description" : "numéro",
                        "indicative" : "237",
                        "digit" : 10,
                    },
                    "reference" : {
                        "fileIndex" : "Id",
                        "description" : "Référence de paiement",
                    },
                    "status" : {
                        "fileIndex" : "Status",
                        "type" : "status"
                    },
                    "amount" : { 
                        "fileIndex" : "Amount",
                    },
                    "account" : {
                        "fileIndex" : "Behalf Of",
                        "descripttion" : "Compte de CinetPay chez l'opérateur",
                    }
                },
                
                "config" : {
                    "MTNCM" : #MTN_CM
                        {
                            "account" : "237681635363",
                            "paymentMethod" : "MTNCM",
                            "exclude" : []
                        },
                    }
            },
            {
                "operators" : ["OMBF"], #OMBF
                "operatorName" : "OMBF",
                "typeOperator" : "Mobile Money",
                "index" : {
                    "datetime" : {
                        "fileIndex" : "Transaction Date",
                        "description" : "date et heure",
                        "format" : "DD-mm-YYYY  HH:MM:SS"
                    },
                    "msisdn" : {
                        "fileIndex" : "Sender Mobile Number",
                        "description" : "numéro",
                        "indicative" : "237",
                        "digit" : 8,
                    },
                    "reference" : {
                        "fileIndex" : "Transaction ID",
                        "description" : "Référence de paiement",
                    },
                    "status" : {
                        "fileIndex" : "Status",
                        "type" : "status"
                    },
                    "amount" : { 
                        "fileIndex" : "Transaction Amount",
                    },
                    "account" : {
                        "fileIndex" : "Receiver Mobile Number",
                        "descripttion" : "Compte de CinetPay chez l'opérateur",
                    }
                },
                
                "config" : {
                    "OMBF" : #OMBF
                        {
                            "account" : "65910683",
                            "paymentMethod" : "OMBF",
                            "exclude" : []
                        },
                    }
            },
            
        ]





TO_VERIFY = {
    "msisdn" : {
        "required" : ["indicative", "digit", "fileIndex"],
    },
    "reference" : {
        "required" : ["fileIndex"]
    },
    "status" :{
        "required" : ["fileIndex"]
    },
    "idTransaction" : {
        "required" : ["fileIndex"]
    },
    "amount" : {
        "required" : ["fileIndex"]
    },
    "date" : {
        "required" : ["fileIndex", "format"]
    },
    "time" : {
        "required" : ["fileIndex", "format"]
    },
    "datetime" : {
        "required" : ["fileIndex", "format"]
    },
    "account" : {
        "required" : ["fileIndex"]
    }
}