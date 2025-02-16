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
                # if p == 1:
                #     cabeçalho = tabula.read_pdf(value, pages=str(p), multiple_tables=True, guess=False, stream=True, area=[40, 10 , 130, 400])
                #     valueConta = obter_conta(cabeçalho[0], 'Unnamed: 0', 'CONTA:')
                if p== mas_paginas:
                    cabeçalho = tabula.read_pdf(value, pages=str(p), multiple_tables=True, guess=False, stream=True, area=[40, 10 , 130, 400])
                    valueConta = obter_conta(cabeçalho[0], 'Unnamed: 0', 'CONTA:')
                    tabela  = tabula.read_pdf(value, pages=str(p), multiple_tables=True, guess=False, stream=True, area=[120, 50 , 850, 560])
                    tabelas.append(tabela[0].values)
                    columnValue = [i for i in tabela[0].columns]
                    columnValue += ['Sinal','Banco','C/C']
                elif p == 1:
                    cabeçalho = tabula.read_pdf(value, pages=str(p), multiple_tables=True, guess=False, stream=True, area=[40, 10 , 130, 400])
                    valueConta = obter_conta(cabeçalho[0], 'Unnamed: 0', 'CONTA:')
                    tabela  = tabula.read_pdf(value, pages=str(p), multiple_tables=True, guess=False, stream=True, area=[120, 50 , 850, 560])
                    tabelas.append(tabela[0].values)                    
                    columnValue = [i for i in tabela[0].columns]
                    columnValue += ['Sinal','Banco','C/C']
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
            num_colunasOnlyListTable = len(onlyListTable[0])
            num_colunasTotais = len(columnValue)
            onlyListTable = [linha + [np.nan] * (num_colunasTotais - num_colunasOnlyListTable) for linha in onlyListTable] 
            df = pd.DataFrame(onlyListTable, columns=columnValue)  
            df['C/C'] = valueConta
            df['Banco'] = nomeBanco                          
            return [True, df]   
        except Exception as e:       
            return [False, e.args]