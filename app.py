# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22  2018

@author: Yacine BOUSLAHI
"""

from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np


app = Flask(__name__)
global flag, table

flag = 1
table = None

@app.route('/', methods = ['GET'])
def graph():
    """ 
	Extraire les donnees d'un client en fonction de num passer en 
    parametre via l'interface web 
	"""
    
    global table
    client =''
    labels = ['2012','2013','2014','2015']
    ca = []
    charge = []
    ecart = []
    
    num = request.args.get('num')
    
    if num == None:
        num = 20000001
    else:
        num = int(num)
    print('num  : %s'% num)
    
    import_excel()  
    
    if num in table.index:
        ca = table.loc[table.index == num,['CA_2012', 'CA_2013', 'CA_2014', 'CA_2015']].values.tolist()[0]
        charge = table.loc[table.index == num,['Charge_2012', 'Charge_2013', 'Charge_2014', 'Charge_2015']].values.tolist()[0]
        client = table.loc[table.index == num,['Lib']].values.tolist()[0][0]
        situation = table.loc[table.index == num,['Sit']].values.tolist()[0][0]
        
        print(list(ca))
        print(list(charge))
        
        ecart = np.round(np.array(charge) / np.array(ca), 2)
        ecart = np.nan_to_num(ecart)
        print(list(ecart))
        print(list(labels))
    else:
        client = 'Num  Invalide'
        situation =''
        print("num invalide")

    info = {'client':client, 'situation':situation, 'num ': num}
    return render_template('graph.html', labels=labels, ca=ca, charge=charge, ecart=ecart, info=info)
    #return jsonify(labels=labels, ca=ca, charge=charge, ecart=ecart, info=info)


def import_excel():
    """ 
	la fonction importe un fichier excel
    """
    global table, flag
    if flag:
        print("Chargement de la table ")
        table = pd.read_excel(io="Table.xlsx", sheet_name='I', header=0, index_col='Num')
        table.fillna(0, inplace=True)
        flag = 0
    else:
        print("pas de rechargement de fichier")


if __name__ == '__main__':
    app.run(port=5000)
    app.secret_key = 'mykey' 
    app.run(debug=True)
    
#TODO: 
