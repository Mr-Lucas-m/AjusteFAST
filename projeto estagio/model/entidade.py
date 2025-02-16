import pandas as pd
import base64
import io
import tabula
import camelot
from PyPDF2 import PdfReader
import numpy as np
import json
import tempfile
from model.components.components import definindo_colunas_de_linhas_2, filterResume, putTables, filterResume_PDF_caixa, convert, is_date, filterResume, getNanValues, treat_pdf, decodePDF, reader,ler, replaceIoBytesIo, filterN, createFile, str_to_number, filterResume_PDF_, drop_rows_invalid, identificador_layout_txt, filterResume_PDF_2,mapear_valores, identificador_sinais_do_banco, obter_conta


class Entidade:
    def __init__(self):
        self.bancoDoBrasil = None
        self.penultimatratou=False
                    
    def quantidade_pg(self, value):
        reader = PdfReader(value)
        total_pg = len(reader.pages)
        
        return total_pg
    
    def tratar_Banpara(self, value):      
        try:           
            pdfReaded = decodePDF(value)
            if pdfReaded[0]==False:
                return pdfReaded
            else:
                value = pdfReaded[1]
                
            columns =''        
            pag = self.quantidade_pg(value)
            mas_paginas = min(pag, pag)
            tabelas = []     
                         
            nomeBanco = 'BANPARA'   
            for p in range(1 ,mas_paginas + 1):              
                if p==1:
                    cabeçalho = tabula.read_pdf(value, pages='1', area=[1, 50, 220, 860] ,multiple_tables=False, guess=True, stream=True)
                    tabela  = tabula.read_pdf(value, pages='1', area=[270, 50, 860, 860], columns=[250, 340, 400, 600], multiple_tables=False, guess=True, stream=True)
                    valueConta = obter_conta(cabeçalho[0], 'Banco do Estado do Pará S/A', 'Conta ')
                    fixdf = reader(tabela)
                    if fixdf[0]==True:
                        df = fixdf[1]
                        columns = df.columns
                        tabelas.append(df.values)                    
                        #columnValue = [i for i in df[0].columns]
                    else:
                        return fixdf
                                                                                   
            onlyListTable = [ta for i in tabelas for ta in i]
            onlyListTable = [[np.nan if isinstance(va, str) and va.startswith('Unnamed') else va for va in i] for i in onlyListTable]
            df = pd.DataFrame(onlyListTable, columns=columns)      
            df = filterResume(df, "--------------")              
            if df[0]==True:
                df =df[1]               
                return [True, df,valueConta,nomeBanco]    
            else:
               return df                      
        except Exception as e:           
            return [False, e.args]
    
    def tratar_Sicred(self, value):              
        try:
            pdfReaded = decodePDF(value)
            if pdfReaded[0]==False:
                return pdfReaded
            else:
                value = pdfReaded[1]
                       
            pag = self.quantidade_pg(value)
            mas_paginas = min(pag, pag)
            tabelas = []  
            nomeBanco = 'SICRED'    
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
                temp_file.write(value.getvalue())  # Escreve os bytes no arquivo temporário
                value = temp_file.name  # Obtém o caminho do arquivo temporário                    
            for p in range(1 ,mas_paginas + 1):              
                if p==1:
                    cabeçalho = tabula.read_pdf(value, pages=str(p), multiple_tables=True, guess=False, stream=True, area=[1, 60 , 250, 400])
                    valueConta = obter_conta(cabeçalho[0], 'ssociado: SANTA IZABEL ALIMENTOS LTDA', 'Conta: ')
                    if p == mas_paginas:
                        tabela  = camelot.read_pdf(value, pages=str(p), flavor='stream')
                        tabela = tabela[0].df
                        tabela = definindo_colunas_de_linhas_2(tabela, ['Data', 'Descrição'])
                        tabela = tabela.reset_index(drop=True)
                        tabelas.append(tabela.values)
                        columnValue = [i for i in tabela.columns]
                    elif p == 1:
                        tabela  = camelot.read_pdf(value, pages=str(p), flavor='stream')
                        tabela = tabela[0].df
                        tabela = definindo_colunas_de_linhas_2(tabela, ['Data', 'Descrição'])
                        tabela = tabela.reset_index(drop=True)
                        tabelas.append(tabela.values)
                        columnValue = [i for i in tabela.columns]
                elif p == mas_paginas -1 or mas_paginas:
                    if p == mas_paginas -1:
                                                                      #str(p -1)
                        penultimate =  camelot.read_pdf(value, pages=str(p), flavor='stream')
                        filterPenultimate = filterResume_PDF_2(penultimate[0].df.values, 'Lançamentos Futuros', 'Saldo da conta')
                        if filterPenultimate[0] == True:
                            tabelas.append(filterPenultimate[1])
                        else:
                            tabelas.append(filterPenultimate[1])
                    elif p == mas_paginas:
                        penultimate = camelot.read_pdf(value, pages=str(p), flavor='stream')
                        filterPenultimate = filterResume_PDF_2(penultimate[0].df.values, 'Lançamentos Futuros', 'Saldo da conta')
                        if filterPenultimate[0] == True:
                            tabelas.append(filterPenultimate[1]) 
                        else: 
                            tabelas.append(filterPenultimate[1]) 
                    else:
                        if p != mas_paginas -1 and mas_paginas:
                            tabela = camelot.read_pdf(value, pages=str(p), flavor='stream')
                            tabelas.append(tabela[0].df.values)
                
            onlyListTable = [ta for i in tabelas for ta in i] 
            onlyListTable = [[np.nan if isinstance(va, str) and va.startswith('Unnamed') else va for va in i] for i in onlyListTable]
            df = pd.DataFrame(onlyListTable, columns=columnValue)
            return [True, df,valueConta, nomeBanco]
        except Exception as e:              
            return [False, e.args]
    
    def tratar_Banco_do_Brasil(self, value):        
        try:         
            pdfReaded = decodePDF(value)
            if pdfReaded[0]==False:
                return pdfReaded
            else:
                value = pdfReaded[1]
            
            pag = self.quantidade_pg(value)
            mas_paginas = min(pag, pag)
            tabelas = []     
            nomeBanco = 'BANCO DO BRASIL'  
            for p in range(1 ,mas_paginas + 1):              
                if p==1:
                    cabecalho = tabula.read_pdf(value, pages=str(p), multiple_tables=True, guess=False, stream=True, area=[70, 50 , 200, 560])
                    valueConta = obter_conta(cabecalho[0], 'Cliente - Conta atual', 'Conta corrente ')
                    if p == mas_paginas:
                        values = ler(value, p-1)   
                        columnValue = values[0]                   
                        tabelas.append(values[1:])
                    elif p ==1:     
                        tabela  = tabula.read_pdf(value, pages=str(p), multiple_tables=True, guess=False, lattice=True, area=[1, 50 , 850, 560])
                        valueConta = obter_conta(cabecalho[0], 'Cliente - Conta atual', 'Conta corrente ')
                        tabelas.append(tabela[0].values)                    
                        columnValue = [i for i in tabela[0].columns]
                elif p == mas_paginas or p ==mas_paginas-1:
                    if p ==mas_paginas-1:
                        penultimate = tabula.read_pdf(value, pages=str(p), multiple_tables=True, guess=False, stream=True, area=[1, 10 , 860, 860])
                        filterPenultimate = filterResume(penultimate[0], "----------------------")
                        if type(filterPenultimate[1]) == pd.DataFrame:
                            values = ler(value, p-1)   
                            columnValue = values[0]                      
                            tabelas.append(values[1:])       
                            self.bancoDoBrasil = True                                                   
                        else: 
                            values = ler(value, p-1)                       
                            tabelas.append(values)  
                    else:     
                        if self.bancoDoBrasil ==True:
                            continue
                        else:                       
                            lastPage = tabula.read_pdf(value, pages=str(p), multiple_tables=True, guess=False, stream=True, area=[1, 10 , 860, 860]) #usnaod tabula apenas como identificador, e não trabalhando com os dados dele
                            filterLastPage = filterResume(lastPage[0], "----------------------")
                            if type(filterLastPage[1]) == pd.DataFrame:
                                values = ler(value, p-1)                       
                                tabelas.append(values)  
                            else: 
                                values = ler(value, p-1)                       
                                tabelas.append(values)                                
                else:
                    values = ler(value, p-1)                       
                    tabelas.append(values)                                                                          
            onlyListTable = [ta for i in tabelas for ta in i]
            onlyListTable = [[np.nan if isinstance(va, str) and va.startswith('Unnamed') else va for va in i] for i in onlyListTable]
            df = pd.DataFrame(onlyListTable, columns=columnValue)    
            df = convert('Lote',df)
            df = convert('Ag.\rorigem',df)                                                       
            return [True, df,valueConta,nomeBanco]  
        except Exception as e:           
            return [False, e.args]
        
        
    def tratar_Sicob(self, value):
        try:      
            pdfReaded = decodePDF(value)
            if pdfReaded[0]==False:
                return pdfReaded
            else:
                value = pdfReaded[1]                       
            pag = self.quantidade_pg(value)
            mas_paginas = min(pag, pag)
            tabelas = []     
            nomeBanco = 'SICOOB' 
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
                temp_file.write(value.getvalue())  # Escreve os bytes no arquivo temporário
                value = temp_file.name  # Obtém o caminho do arquivo temporário                     
            for p in range(1 ,mas_paginas + 1):
                if p==1:
                    cabeçalho = tabula.read_pdf(value, pages=str(p), multiple_tables=True, guess=False, stream=True, area=[40, 10 , 130, 400])
                    valueConta = obter_conta(cabeçalho[0], 'Unnamed: 0', 'CONTA:')
                    tabela  = tabula.read_pdf(value, pages=str(p), multiple_tables=True, guess=False, stream=True, area=[116, 50 , 850, 560])                   
                    tabelas.append(tabela[0].values)                    
                    columnValue = [i for i in tabela[0].columns]
                elif p == mas_paginas or p == mas_paginas -1:
                
                    if p==mas_paginas and self.penultimatratou ==True:
                        continue
                    
                    tabela = camelot.read_pdf(value, pages=str(p), flavor='stream')
                    if len(tabela) > 1:
                        seg_tabela = tabela[0]
                        tabelas.append(seg_tabela.df.values)
                        self.penultimatratou =True
                    elif len(tabela) == 1:
                        seg_tabela = tabela[0].df
                        verifi_tabela = filterResume(seg_tabela, 'RESUMO')           
                        if type(verifi_tabela) != pd.DataFrame:
                            seg_tabela = tabela[0]
                            tabelas.append(seg_tabela.df.values) 
                            self.penultimatratou =True
                        else:
                            tabelas.append(verifi_tabela.values)
                            self.penultimatratou =True
                                                                        
                else:
                    if p != mas_paginas -1 and mas_paginas:
                        tabela = tabula.read_pdf(value, pages=str(p), multiple_tables=True, guess=False, stream=True, area=[1, 50 , 850, 560])
                        columnsToValue = tabela[0].columns
                        tabelas.append([columnsToValue])  
                        tabelas.append(tabela[0].values)  

            onlyListTable = [ta for i in tabelas for ta in i]
            onlyListTable = [[np.nan if isinstance(va, str) and va.startswith('Unnamed') else va for va in i] for i in onlyListTable]
            df = pd.DataFrame(onlyListTable, columns=columnValue)                                     
            return [True, df, valueConta, nomeBanco]   
        except Exception as e:       
            return [False, e.args]
        
        
    def identificador_layout(pdf):
        pass
    
    ############ identificador de LAYOUT  ##########################
    def tratar_caixa(self, value):        
        try:         
            pdfReaded = decodePDF(value)
            if pdfReaded[0]==False:
                return pdfReaded
            else:
                value = pdfReaded[1]
            
            pdf_layout = identificador_layout_txt(value, 'Extrato por período')
            pag = self.quantidade_pg(value)
            mas_paginas = min(pag, pag)
            tabelas = []
            nomeBanco = 'CEF'
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
                temp_file.write(value.getvalue())  # Escreve os bytes no arquivo temporário
                value = temp_file.name  # Obtém o caminho do arquivo temporário   
            for p in range(1 ,mas_paginas + 1): 
                if pdf_layout == [1]:
                        if p == 1:
                            cabeçalho = tabula.read_pdf(value, pages=str(p), multiple_tables=True, guess=False, stream=True, area=[50, 1 , 250, 400])
                            valueConta = obter_conta(cabeçalho[0],'Extrato por período', 'Conta: ')
                            if p == mas_paginas:
                                tabela  = camelot.read_pdf(value, pages=str(p), flavor='stream')
                                filtro = filterResume_PDF_(tabela[0].df.values, 'SAC CAIXA:')
                                if filtro[0] == True:
                                    tabelas.append(filtro[1])
                                    columnValue = [i for i in tabela[0].columns]
                                    # columnValue += ['Sinal','Banco','C/C']
                                else:
                                    tabelas.append(filtro[1])
                                    columnValue = [i for i in tabela[0].columns]
                                    # columnValue += ['Sinal','Banco','C/C']
                            elif p == 1:
                                tabela  = tabula.read_pdf(value, pages=str(p), multiple_tables=True, guess=False, stream=True, area=[220, 10 , 820, 560])
                                tabelas.append(tabela[0].values)
                                columnValue = [i for i in tabela[0].columns]
                        elif p == mas_paginas -1 or mas_paginas:
                            if p == mas_paginas -1:
                                tabela  = camelot.read_pdf(value, pages=str(p), flavor='stream')
                                filtro = filterResume_PDF_(tabela[0].df.values, 'SAC CAIXA:')
                                if filtro[0] == True:
                                    tabelas.append(filtro[1])
                                else:
                                    filtro_fal = filtro
                                    tabelas.append(filtro_fal[1])
                            else:
                                if p == mas_paginas:
                                    tabela  = camelot.read_pdf(value, pages=str(p), flavor='stream')
                                    filtro = filterResume_PDF_(tabela[0].df.values, 'SAC CAIXA:')
                                    
                                    if filtro[0] == True:
                                        tabelas.append(filtro[1])
                                    else:
                                        tabelas.append(filtro[1])
                        else:
                            ####### tratamento das demais paginas que estao fora do if e elif:                
                            if p != mas_paginas -1 and mas_paginas:
                                tabela  = camelot.read_pdf(value, pages=str(p), flavor='stream')
                                tabelas.append(tabela[0].df.values)
                else:
                ######LEITURA E LOGICA PRO SEGUNDO layoout PDF CAIXA CINZa
                    if pdf_layout == [2]:
                        if p == 1:
                            cabeçalho = tabula.read_pdf(value, pages=str(p), multiple_tables=True, guess=False, stream=True, area=[20, 1 , 250, 400])
                            valueConta = obter_conta(cabeçalho[0], 'Extrato', 'Conta: ')
                            if p == mas_paginas:    
                                tabela  =  camelot.read_pdf(value, pages=str(p), flavor='stream')
                                tabela = definindo_colunas_de_linhas_2(tabela[0].df, ['DATA', 'NR. DOC.'])
                                filtro = filterResume_PDF_(tabela, 'SAC CAIXA:')
                                if filtro[0] == True:
                                    tabelas.append(tabela.values)
                                    columnValue = [i for i in tabela[0].columns]
                                    # columnValue += ['Sinal','Banco','C/C']
                                else:
                                    tabelas.append(tabela.values)
                            elif p == 1:
                                tabela  = camelot.read_pdf(value, pages=str(p), flavor='stream')
                                tabela = definindo_colunas_de_linhas_2(tabela[0].df, ['DATA', 'NR. DOC.'])
                                tabelas.append(tabela.values)
                                columnValue = [i for i in tabela.columns]
                                # columnValue += ['Sinal','Banco','C/C']
                        elif p == mas_paginas -1 or mas_paginas:
                            if p == mas_paginas -1:
                                tabela  = camelot.read_pdf(value, pages=str(p), flavor='stream')
                                tabela = drop_rows_invalid(tabela[0].df, 'Extrato')
                                filtro = filterResume_PDF_(tabela, 'SAC CAIXA:')
                                if filtro[0] == True:
                                    tabelas.append(tabela.values)
                                else:
                                    tabelas.append(tabela.values)
                            elif p == mas_paginas:
                                tabela = camelot.read_pdf(value, pages=str(p), flavor='stream')
                                tabela = drop_rows_invalid(tabela[0].df, 'Extrato')
                                filtro = filterResume_PDF_(tabela, 'SAC CAIXA:')
                                if filtro[0] == True:
                                    tabelas.append(tabela.values)
                                else:
                                    tabelas.append(tabela.values)
                        else:
                            if p != mas_paginas -1 and mas_paginas:
                                tabela = camelot.read_pdf(value, pages=str(p), flavor='stream')
                                tabela = drop_rows_invalid(tabela[0].df, 'Extrato')
                                tabelas.append(tabela.values)
                                
                
            onlyListTable = [ta for i in tabelas for ta in i] 
            onlyListTable = [[np.nan if isinstance(va, str) and va.startswith('Unnamed') else va for va in i] for i in onlyListTable]          
            df = pd.DataFrame(onlyListTable, columns=columnValue)
            df = convert('Nr. Doc.', df)
            df = drop_rows_invalid(df, 'Ge r_encia d:oR:::CAIxA')
            #começar o tratamento do pdf
            return [True, df,valueConta,nomeBanco]    
        except Exception as e:          
            return [False, e.args]
        
        
    def extract_names_columns(self, df):        
        return [i for i in df.columns]
    
    def tratarPdf_Excel(self, pdfs, ecxel, inputValue):     
        try:           
            notInExcel = False
            pdfsFrame = pd.DataFrame(pdfs)                       
            pdfsFrame = pdfsFrame.applymap(lambda x: x.upper() if isinstance(x, str) else x)
            pdfsFrame.columns = pdfsFrame.columns.str.upper() 
            pdfsFrame = pdfsFrame[~pdfsFrame.apply(lambda row: row.astype(str).str.contains('SALDO ANTERIOR| 000 SALDO ANTERIOR|SALDO BLOQUEADO ANTERIOR').any(), axis=1)] #excluir saldo anterior 
            co =pdfsFrame.columns               
            excelFrame = ecxel
            # Transformando todos os valores do excelFrame em maiúsculas
            excelFrame = excelFrame.applymap(lambda x: x.upper() if isinstance(x, str) else x)
            excelFrame.columns = excelFrame.columns.str.upper()                
            #PDFS 
            dataP = co[co.str.contains('^(DATA|DT. BALANCETE|DATA MOV.)', regex=True)].tolist()[0] 
            valorP = co[co.str.contains('^(VALOR|VALOR R$|VALOR (R$))', regex=True)].tolist()[0]
            documentoP = co[co.str.contains('^(DOCUMENTO|DOC.|NR. DOC.)', regex=True)].tolist()[0]
            historicoP = co[co.str.contains('^(HISTÓRICO|DESCRIÇÃO|DESCRICAO)', regex=True)].tolist()[0]                                             
            indices_to_drop = []    
                                              
            for indx, (dt_balancete, valor_r, doc, descri) in enumerate(zip(pdfsFrame[dataP], pdfsFrame[valorP], pdfsFrame[documentoP], pdfsFrame[historicoP])):                                                    
                for index, (data, valor, documento, descricao) in enumerate(zip(excelFrame['DATA'], excelFrame['VALOR'], excelFrame['ID TRANS. / NÚMERO'], excelFrame['DESCRIÇÃO'])):                                                  
                    if index in indices_to_drop:
                        continue
                    if data == dt_balancete and abs(valor) == abs(str_to_number(valor_r)) and (str(doc).replace('.', '') in documento.replace('.', '') or any(num in documento for num in [i for i in str('IOF/2-9').replace('-', '').replace('.','').split('/') if i.isdigit()]) or doc =='PIX' and '0' in documento if doc is not None else '' in documento) and descricao.replace('-','').replace(',','').replace('.','').replace(' ','') in descri.replace('-','').replace(',','').replace('.','').replace(' ',''):                           
                        pdfsFrame[historicoP].iloc[indx] = f"{inputValue}**{pdfsFrame[historicoP].iloc[indx]} {documento}"                      
                        indices_to_drop.append(index)   
                        if notInExcel is False:
                            notInExcel =True 
                        break                                                                      
            excelFrame = excelFrame.drop(indices_to_drop, errors='ignore')            
            return [True, pdfsFrame,excelFrame, notInExcel]        
        except Exception as e:          
            return [False, f'Erro na função tratarPdf_Excel: {e.args}']
        
    def get_format_padrao(self, pdfs, padraoXLS,input):
        try:
            columns2Values = ['SINAL', 'BANCO', 'C/C']
            valores_padronizados = [coluna for coluna in padraoXLS[0]]    
            valores_padronizados.extend(col for col in columns2Values if col not in valores_padronizados)
            pdfs = pd.DataFrame(pdfs)            
            # Transformar os nomes das colunas para maiúsculas
            pdfs.columns = pdfs.columns.str.upper()
            # Transformar todos os valores do DataFrame para maiúsculas
            pdfs = pdfs.applymap(lambda x: x.upper() if isinstance(x, str) else x)
            # Agora pdfs terá todas as colunas e valores em maiúsculas
            pdfs = pdfs[~pdfs.apply(lambda row: row.astype(str).str.contains('SALDO ANTERIOR|000 SALDO ANTERIOR|SALDO BLOQUEADO ANTERIOR|999 S A L D O').any(), axis=1)] #excluir saldo anterior 
            pdfs = identificador_sinais_do_banco(pdfs, 'VALOR', ['-'], ['+','C','*','D'])
            padrao = {
                'DATA': "Data do Lanc.",
                'HISTÓRICO': "Hist. Complementar",
                'VALOR': "Valor da Partida"                
            }
            for index, (historico) in enumerate(pdfs['HISTÓRICO']):
                pdfs['HISTÓRICO'].iloc[index] = f"{input}**{historico}"                
            #columns = ['Data do Lanc.', 'Hist. Complementar', 'Valor da Partida']          
            pdfs.rename(columns=padrao, inplace=True)    
            ff = pd.DataFrame(columns=valores_padronizados)
            ff[valores_padronizados] = pdfs.reindex(columns=valores_padronizados)                              
            return [True, ff]             
        except Exception as e:
            return [False, e.args]
        
        
        
