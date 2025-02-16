from model.entidade import Entidade
from tkinter import Tk, Toplevel
from tkinter.filedialog import asksaveasfilename
from model.components.components import saveFrame, treat_pdf,createFile
import json
import webview
import pandas as pd

class Controller:
      def __init__(self):      
         self.entidade = Entidade()
         
      def get_padrao(self,pdfs ,padrao, input):   
         renomeacao = {
            'DATA MOV.':'DATA',
            'DT. BALANCETE':'DATA',
            'DESCRICAO': 'HISTÓRICO',  # Renomeia DESCRICAO para HISTÓRICO
            'DESCRIÇÃO': 'HISTÓRICO',
            'NR. DOC.': 'DOC.',         # Renomeia NR. DOC. para DOC.
            'DOCUMENTO':'DOC.', 
            'VALOR (R$)': 'VALOR',      # Renomeia VALOR (R$) para VALOR
            'VALOR R$': 'VALOR',
            'SALDO (R$)': 'SALDO'       # Renomeia SALDO (R$) para SALDO
         }
         listRes=[]      
         pdfs = json.loads(pdfs)        
         for i in pdfs:
            for va in i[0]:
               df = pd.DataFrame(json.loads(va))        
               df.columns = df.columns.str.upper() 
               df.rename(columns=renomeacao, inplace=True)# Renomear colunas conforme o mapeamento                            
               listRes.append(df) # Adiciona o DataFrame à lista         
         df_final = pd.concat(listRes, ignore_index=True)# Combina todos os DataFrames em um único DataFrame
         result = self.entidade.get_format_padrao(df_final ,padrao,input)
         return [result[0], json.loads(result[1].to_json(orient='records'))] if result[0]==True else result        
      
      def tratarPdf_Excel(self, pdfs, ecxel, inputValue, nameBank):          
         namesErro = []                  
         ecxel = createFile(json.loads(ecxel))  
         ecxel = ecxel[1]
         result =[]
         listR = json.loads(pdfs)
         notInExe = []
         res = None
      
         for index,i in enumerate(listR):
            for va in i[0]:                             
               res = self.entidade.tratarPdf_Excel(json.loads(va), ecxel, inputValue)
               if res[0]==True:                      
                  result.append(res[1])
                  ecxel = res[2]                  
                  if res[3]==False:
                     notInExe.append(nameBank[index]) 
                  res = None
                  break                
               elif res[0]==False:                  
                  bankName = nameBank[index]
                  namesErro.append([bankName, res[1]])
                  res = None
                  continue
         if len(result)>0:
            resultF = [True, [json.loads(i.to_json(orient='records')) for i in result]]     
         else: 
            resultF=False
         return [resultF, notInExe, namesErro]  
         
      
      def caixa(self, pdf):
         result = self.entidade.tratar_caixa(pdf)
         return [result[0] ,result[1].to_json(orient='records'), result[2], result[3]] if result[0]==True else result
                        
      def Banpara(self, pdf):
         result = self.entidade.tratar_Banpara(pdf)
         return [result[0] ,result[1].to_json(orient='records'), result[2], result[3]] if result[0]==True else result
      
      def Sicred(self, pdf):
         result = self.entidade.tratar_Sicred(pdf)
         return  [result[0] ,result[1].to_json(orient='records'), result[2], result[3]] if result[0]==True else result
      
      def Banco_do_Brasil(self, pdf):
         result = self.entidade.tratar_Banco_do_Brasil(pdf)
         return  [result[0] ,result[1].to_json(orient='records'), result[2], result[3]] if result[0]==True else result
      
      def Sicob(self, pdf):
         result = self.entidade.tratar_Sicob(pdf)
         return  [result[0] ,result[1].to_json(orient='records'), result[2], result[3]] if result[0]==True else result
      
      def salvarFrame(self, pdf):
         df = pd.DataFrame(pdf)
         result = saveFrame(df)
         return result
      
      def treatPdf(self, pdf, position):
         pdfV = json.loads(pdf[0])
         nConta = pdf[1]
         nomeBank=pdf[2]
         df = pd.DataFrame(pdfV)      
         result = treat_pdf(df, position,nConta,nomeBank)
         return [result[0] ,result[1].to_json(orient='records')] if result[0]==True else result

      def save(self, value):
         pdf = json.loads(value)
         df = pd.DataFrame(pdf)  
         result = saveFrame(df)
         return result
      
      


         