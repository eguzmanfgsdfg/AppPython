def model(input) -> str:    
   # -*- coding: utf-8 -*-
    """
    Created on Sun Jan 21 19:15:02 2024

    @author: Victor Sánchez
    """

    ##########################
    #CARGA DE MODELOS
    ##########################

    #Librerias
    import numpy as np
    import torch

    #LOAD EL ENCODER GUARDADO
    from sklearn.preprocessing import LabelEncoder
    import numpy as np

    le = LabelEncoder()
    le.classes_ = np.load('./classes.npy', allow_pickle=True)

    # Model class
    model = torch.load('./full_model_scripted.pt')
    model.eval()

    input = [[
    '0fa2b371-1017-4859-98bf-61a63ca34eac','','','',40,0,'0','','','19/01/2024 00:35:23','0','104.28.92.207','[BZP154]Fixwir_8457239_BR','','473702******5130','0','0','MC-13379191','0','','0','47370291','US','65101','JEFFERSON CITY','MO','OTHER','Visa','0','0','0','0',40,'elvisjrbridgeman@icloud.com','ELVIS BRIDGEMAN','0','0','0'
    ]]

    #-------------------
    #PRUEBA DEL MODELO
    #-------------------
    from sklearn.metrics import accuracy_score

    def softmax(x): #Función para establecer la salida como función de probabilidad
        return torch.exp(x) / torch.exp(x).sum(axis=-1,keepdims=True)

    def fit(model, dataset, scheduler=None, log_each=1, weight_decay=0):

        #TRANSFORMACIÓN A VARIABLES CATEGÓRICAS AGRUAPADAS
        monto = input[0][4]
        if (monto <= 50): rango = 'tier_1_50'
        elif (monto > 50) & (monto <= 250): rango = 'tier_2_250'
        elif (monto > 250) & (monto <= 500) : rango = 'tier_3_500'
        elif (monto > 500) & (monto <= 1000): rango = 'tier_4_1000'
        elif (monto > 1000) & (monto <= 1500): rango = 'tier_5_1500'
        elif (monto > 1500) & (monto <= 2000): rango = 'tier_6_2000'
        elif (monto > 2000) & (monto <= 2500): rango = 'tier_7_2500'
        elif (monto > 2500) & (monto <= 5000): rango = 'tier_8_5000'
        elif  (monto > 5000): rango = 'tier_9_5001'

        monto_2 = input[0][5]
        if (monto_2 <= 50): rango_in_bank_currency = 'tier_1_50'
        elif (monto_2 > 50) & (monto_2 <= 250): rango_in_bank_currency = 'tier_2_250'
        elif (monto_2 > 250) & (monto_2 <= 500) : rango_in_bank_currency = 'tier_3_500'
        elif (monto_2 > 500) & (monto_2 <= 1000): rango_in_bank_currency = 'tier_4_1000'
        elif (monto_2 > 1000) & (monto_2 <= 1500): rango_in_bank_currency = 'tier_5_1500'
        elif (monto_2 > 1500) & (monto_2 <= 2000): rango_in_bank_currency = 'tier_6_2000'
        elif (monto_2 > 2000) & (monto_2 <= 2500): rango_in_bank_currency = 'tier_7_2500'
        elif (monto_2 > 2500) & (monto_2 <= 5000): rango_in_bank_currency = 'tier_8_5000'
        elif  (monto_2 > 5000): rango_in_bank_currency = 'tier_9_5001'


        #SELECCIÓN DE CAMPOS PARA MODELO ML
        X = [[input[0][1],input[0][2],rango,rango_in_bank_currency,input[0][6], #'Afiliacion', 'SubAffiliation','Amount', 'additionalAmount', 'currency',
            input[0][7],input[0][8],input[0][10],input[0][11],input[0][12], #'Promo Months','months','entryMode','IPAddress','Merchant Account Name',
            input[0][13],input[0][19],input[0][20],input[0][21],input[0][22], #'Bank Account Name','Descriptor','operation', 'Bin8', 'Customer Country',
            input[0][23],input[0][25],input[0][25],input[0][26],input[0][27], #'Customer Zip Code', 'Customer City','Customer State','Credit Card Type', 'Credit Card Brand',
            rango_in_bank_currency]] #'Amount Charged in Bank Currency'

        new_data_list = X[0]
        for unique_item in np.unique(input):
            if unique_item not in le.classes_:
                new_data_list = ['Unknown' if x==unique_item else x for x in new_data_list]

        #ACPLICACIÓN DEL MODELO
        model.eval()
        with torch.no_grad():
            X = np.array(new_data_list)
            X = le.transform(X) #Transformación de datos
            X = torch.tensor(X).float().view(-1,21).to(torch.int64)
            y_pred = model(X)
            ypred_prob = softmax(model(X))
            ypred_prob = ypred_prob[0][0]
            ypred_prob = ypred_prob.numpy()
            ypred_prob = round(ypred_prob.item(),4)
            y_predfin = torch.argmax(softmax(y_pred), axis=1)
            y_predfin = y_predfin[0]
            y_predfin = y_predfin.numpy()
            y_predfin = y_predfin.item()

        return {'y_pred':y_predfin, 'ypred_prob':ypred_prob}

    #SE EVALUAN LOS DATOS CON EL MODELO YA GUARDADO
    hist_adam = fit(model,input)

    print('Valores predichos')
    print(hist_adam['y_pred'])

    print('Score (probabilidad de fraude)')
    print(hist_adam['ypred_prob'])
    return hist_adam['ypred_prob']