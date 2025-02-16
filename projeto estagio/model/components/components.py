import numpy as np
import pandas as pd
from tkinter import Tk
from tkinter.filedialog import asksaveasfilename
from datetime import datetime
import pdfplumber
import base64
import io
import camelot
import tempfile
import fitz
from PIL import Image
from collections import Counter
from tkinter import filedialog
import pdfplumber
import base64
from datetime import datetime, timedelta
from collections import Counter
import tabula


def saveFrame(df):
    try:                     
        # Abre a caixa de diálogo para salvar o arquivo
        file_path = asksaveasfilename(defaultextension=".xlsx", 
                                    filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                                    title="Salvar DataFrame como Excel")

        # Verifica se o usuário não cancelou a operação
        if file_path:
            # Salva o DataFrame em um arquivo Excel
            df.to_excel(file_path, index=False)
            return [True]     
        else:
            return [True]              

    except Exception as e:
        return [False, e.args]

def drop_rows_invalid(value, row_in):
    if not isinstance(row_in, list):
        row_in = [row_in]
    row_in = [r.lower().strip() for r in row_in]
    dfdrop = value[~value.apply(
        lambda row: any(cell.lower().strip() in row_in for cell in row.astype(str)), axis=1
    )]
    return dfdrop  

def convert(value, df):
    # Localizar a coluna correspondente, independentemente de maiúsculas/minúsculas
    column_map = {col.lower(): col for col in df.columns}  # Mapeia nomes em minúsculas para os originais
    normalized_value = value.lower()  # Normaliza o valor fornecido

    # Verifica se o nome fornecido corresponde a uma coluna no DataFrame
    if normalized_value not in column_map:
        return df  # Retorna o DataFrame inalterado se a coluna não existir

    # Obter o nome original da coluna
    original_column = column_map[normalized_value]

    # Aplicar formatação à coluna correspondente
    if normalized_value == 'lote':
        df[original_column] = df[original_column].apply(
            lambda x: '{:05.0f}'.format(x) if pd.notnull(x) and isinstance(x, (float, int)) else x
        )
    elif normalized_value == 'nr. doc.':
        df[original_column] = df[original_column].apply(
            lambda x: '{:06.0f}'.format(x) if pd.notnull(x) and isinstance(x, (float, int)) else x
        )
    else:
        df[original_column] = df[original_column].apply(
            lambda x: '{:04.0f}'.format(x) if pd.notnull(x) and isinstance(x, (float, int)) else x
        )

    return df

'''def convert(value, df):
        df =df
        # Specify columns that should retain the '0000' format and convert them to strings with zero-padding
        columns_to_format = [value]  # Replace with actual column names
        for col in columns_to_format:
            if col in df.columns:  # Verifica se a coluna existe no DataFrame
                if value=='Lote':
                    df[col] = df[col].apply(lambda x: '{:05.0f}'.format(x) if pd.notnull(x) and isinstance(x, (float, int)) else x)
                elif value=='Nr. Doc.':
                    df[col] = df[col].apply(lambda x: '{:06.0f}'.format(x) if pd.notnull(x) and isinstance(x, (float, int)) else x)
                else:
                    df[col] = df[col].apply(lambda x: '{:04.0f}'.format(x) if pd.notnull(x) and isinstance(x, (float, int)) else x) 

            else:
                return df
        return df
'''

def putTables(coluns, tabelas):
    tabelas_filtradas = []
    for i in tabelas:
        if i.shape[1] == 1:  # Verifica se a tabela tem apenas uma coluna
            continue  # Ignora essa tabela se tiver apenas uma coluna
        
        # Ajuste o número de colunas do DataFrame para corresponder ao número de colunas na lista `coluns`
        if len(i.columns) == len(coluns):
            i.columns = coluns  # Atribui diretamente os nomes das colunas
        elif len(i.columns) < len(coluns):
            # Adiciona colunas extras com valores vazios, para igualar o comprimento
            i = i.reindex(columns=range(len(coluns))).fillna('')  # Adiciona colunas vazias
            i.columns = coluns  # Define os nomes das colunas
        else:
            # Trunca as colunas extras para que correspondam ao número de colunas em `coluns`
            i = i.iloc[:, :len(coluns)]  # Seleciona apenas o número necessário de colunas
            i.columns = coluns
        
        tabelas_filtradas.append(i)  # Adiciona a tabela processada à lista final
    
    return tabelas_filtradas


def is_date(data_str):
    try:
        if pd.isna(data_str):
            return False
        
        # Tenta converter a string para um objeto datetime no formato completo
        datetime.strptime(data_str, '%d/%m/%Y')
        return True
    except ValueError:
        try:
            # Tenta converter a string para um objeto datetime no formato abreviado
            datetime.strptime(data_str, '%d/%m')
            return True
        except ValueError:
            return False

def filterResume_PDF_caixa(df, word):                                 #'RESUMO'
    result =''
    mask = np.array([np.any(pd.Series(row).astype(str).str.contains(word)) for row in df])
    # Encontra o índice da primeira linha que contém a palavra
    resumo_index = np.argmax(mask) if np.any(mask) else None    
    if resumo_index is not None:
        result = df[:resumo_index]
        return [True, result]    
    else:
        result = df
    return [False, result]

def definindo_colunas_de_linhas_2(df, linha_value):
        for i in range(min(5, len(df))):  # Limita a 5 linhas ou ao total de linhas disponíveis
            linha = df.iloc[i]
        # Verifica se algum dos valores procurados está nesta linha
            if any(valor in linha.values for valor in linha_value):
                df.columns = linha  # Define as colunas para a linha encontrada
                df = df[i + 1:].reset_index(drop=True)  # A tabela começa a partir da linha abaixo
                return df
        print('nenhum ')
        return df
    
    
def identificador_layout_txt(pdf, linha_indenfic_de_layout):
    try:
        page_data = tabula.read_pdf(pdf, pages='1', multiple_tables=True, guess=False, stream=True, area=[1, 10 , 820, 560])
        page_text = " ".join(
            df.astype(str).apply(lambda x: " ".join(x), axis=1).str.cat(sep=" ") 
            for df in page_data if not df.empty
        )
        if linha_indenfic_de_layout in page_text:
            return [1] 
        else:
            return [2] 
    except Exception as e:
        return str(e)
    
    
def filterResume_PDF_2(df, word1, word2):
    result =''
    mask = np.array([np.any(pd.Series(row).astype(str).str.contains(word1)) or 
                     np.any(pd.Series(row).astype(str).str.contains(word2)) for row in df])
    
    # Encontra o índice da primeira linha que contém pelo menos uma das palavras
    resumo_index = np.argmax(mask) if np.any(mask) else None
    if resumo_index is not None:
        result = df[:resumo_index]
        return [True, result]
    else:
        result = df
    return [False, result]

    
def filterResume_PDF_(df, word):
    result =''
    mask = np.array([np.any(pd.Series(row).astype(str).str.contains(word)) for row in df])
    # Encontra o índice da primeira linha que contém a palavra
    resumo_index = np.argmax(mask) if np.any(mask) else None
    if resumo_index is not None:
        result = df[:resumo_index]
        return [True, result]
    else:
        result = df
    return [False, result]


    
def filterResume(df, word): #'RESUMO'
    try:
        result =''
        mask = df.apply(lambda row: row.astype(str).str.contains(word).any(), axis=1) 
        resumo_index = mask.idxmax() if mask.any() else None
        
        # Filtrar apenas as linhas acima da linha "Resumo"
        if resumo_index is not None:
            df = df.loc[:resumo_index-1]  # Inclui as linhas até antes de "Resumo"
            result =df
        else:
            result = False
        return [True, result]
    except Exception as e:
        return [False, e.args]

def getNanValues(df):
    values = []
    
    for i in range(len(df)):
        
        linha = df.iloc[i].values.tolist()  # Converte a linha para uma lista
        valueProximo = is_date(linha[0])
        # Verifica se o primeiro valor da linha começa com 'nan'
        if pd.isna(linha[0]) or valueProximo==False:
            values.append(linha)
        else:
            return values  # Para a busca ao encontrar uma linha que não começa com 'nan'
    
    return values


def ler(value, index):        
    with pdfplumber.open(value) as pdf:
        # Vamos pegar a primeira página do PDF
        page = pdf.pages[index]
        
        # Extrair as tabelas da página
        tables = page.extract_tables()            
        return [va for i in tables for va in i]
    
    
def treat_pdf(df, lineNow,nConta,nomeBank):
    try:   
        df=df               
        linhas_agrupadas = []
        i = 0                       
        #começar o tratamento do pdf
        while i < len(df) - 1:   # Não precisa verificar a última linha
            linha_atual = df.iloc[i].values.tolist()  #pegar epanas os valores e rejeitar as colunas
            proximo = df.iloc[i+1].values.tolist()   
            #nexProximo = df.iloc[i+2].values.tolist()   
            
            valueProximo = is_date(proximo[0])
                            
            if  valueProximo ==False or pd.isna(proximo[0]):
                stringProximo = [i for i in proximo if isinstance(i, str)]
                stringProximo = ' '.join([value for i, value in enumerate(stringProximo)])
                stringAtual = str(linha_atual[lineNow])
                contatenarValor = ' '.join([stringAtual, stringProximo])
                
                valueNexProximo = getNanValues(df.iloc[i+2:])
                if len(valueNexProximo)>0:
                    stringNexProximo = ' '.join(va for i in valueNexProximo for va in i if isinstance(va, str))              
                    contatenarValor = ' '.join([contatenarValor, stringNexProximo])
                
                linha_atual[lineNow] = contatenarValor                    
                linhas_agrupadas.append(linha_atual)
                #Skip(jogar fora)  the `proximo` row by incrementing `i` by 2 or 3
                i += 2 if len(valueNexProximo)==0 else 2+len(valueNexProximo)
            else:
                linhas_agrupadas.append(linha_atual)
                i += 1
        if i < len(df): #adicionar a ultima linha
            linhas_agrupadas.append(df.iloc[i].values.tolist())
        resultF = pd.DataFrame(linhas_agrupadas, columns=df.columns)            
        #resultF = identificador_sinais_do_banco(df, 'VALOR', ['-'], ['+','C','*','D'])
        resultF['Sinal']=None
        resultF['Banco']=None
        resultF['C/C']=None
        resultF['C/C']=nConta
        resultF['Banco']= nomeBank
        return [True, resultF]
    except Exception as e:
        return [False, e.args]
    
    
def decodePDF(value):
    try:
        pdf_data = base64.b64decode(value)
        pdf_file = io.BytesIO(pdf_data)  # Cria um objeto BytesIO a partir dos dados decodificados
        return [True, pdf_file]
    except Exception as e:
        return [False, e.args]
    
    
def reader(value):    
    try:            
        df = value[0]         
        # Processar o DataFrame para corrigir os cabeçalhos
        df.columns = [i.upper() for i in df.columns] 
        df = df[1:]  # Remover a primeira linha do DataFrame
        df.reset_index(drop=True, inplace=True)  # Resetar o índice
        # Separar a coluna "DATA DESCRICAO" em duas colunas
        if 'DATA DESCRICAO' in df.columns:
            # Supondo que a coluna "DATA DESCRICAO" é a primeira coluna
            df[['DATA', 'DESCRICAO']] = df['DATA DESCRICAO'].str.split(expand=True, n=1)
            # Remover a coluna original "DATA DESCRICAO"
            df.drop(columns=['DATA DESCRICAO'], inplace=True)
            colunas_restantes = df.columns.tolist()
            colunas_restantes.remove('DATA')
            colunas_restantes.remove('DESCRICAO')
            df = df[['DATA', 'DESCRICAO'] + colunas_restantes]
        return [True, df]        
    except Exception as e:
        return {None, e.args}
    
def replaceIoBytesIo(value):
   
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
        temp_file.write(value.getvalue())
        temp_file_path = temp_file.name
    return temp_file_path

def filterN(df, word):  # 'RESUMO'
    try:
        result = ''
        # Cria uma máscara para encontrar a linha que contém a palavra
        mask = df.apply(lambda row: row.astype(str).str.contains(word).any(), axis=1)
        resumo_index = mask.idxmax() if mask.any() else None
        
        # Filtrar apenas as linhas abaixo da linha "Resumo"
        if resumo_index is not None:
            df = df.loc[resumo_index + 1:]  # Inclui as linhas após "Resumo"
            result = df
        else:
            result = False
        
        return [True, result]
    except Exception as e:
        return [False, e.args]

def corrigir_data(value):
    try:
        if value == '':
            return value  # Retorna a string vazia sem alteração
        if isinstance(value, np.float64):
            return float(value)
        data_base = datetime(1900, 1, 1)
        numero_corrigido = value - 2
        data_final = data_base + timedelta(days=numero_corrigido)
        return data_final.strftime("%d/%m/%Y")    
    except KeyError as e:
        print(e.args)
    except TypeError as e:
        print(e)
        
    
def createFile(file):     
    try:   
        file_data = file.copy()  # Create a copy of the original data
        column_names = file_data.pop(0)  # Extract the header row
        frame = pd.DataFrame(file_data, columns=column_names) 
        frame['Data'] = frame['Data'].apply(corrigir_data)    
        #frame['Valor'] = frame['Valor'].apply(ff)    
        #frame['Valor da Partida'] = frame['Valor da Partida'].apply(float)
        return [True, frame]
    except KeyError as e:
        return [False, e.args]
    except pd.errors.ParserError:
        return [False, e.args]
    except IndexError:
        return [False, e.args]
    except TypeError as e:
        print(e)
        return [False, e.args]
    
    
def obter_conta(df, coluna, NameConta):
    try:
        df[coluna] = df[coluna].fillna("")
        valueConta = df.loc[df[coluna].str.startswith(NameConta), coluna]
        if valueConta.empty:
            return None
        return valueConta.iloc[0].replace(NameConta,'').strip()
    except Exception as e:
        return str(e)
    
def identificador_sinais_do_banco(df, coluna, negativo, positivo):
    try:
        df['SINAL'] = df[coluna].apply(
            lambda x: (
                str(x).strip()[0] if str(x).strip() and str(x).strip().startswith(tuple(negativo)) else  # Se começa com um sinal negativo
                (str(x).strip()[-1] if str(x).strip() and str(x).strip()[-1] in positivo else '+' if str(x).strip() else None)  # Se termina com um sinal positivo ou é um valor sem sinal
            )
        )
                
        df[coluna] = df[coluna].apply(
            lambda x: str(x).strip().lstrip('-').rstrip('+').rstrip('C').rstrip('*').rstrip('D') if str(x).strip() else None
        )
        if df.empty:
            return None
        return df
    except Exception as e:
        return str(e)
    
    
    


# Dicionário de cores de referência
cores_referencia = {
    "amarelo_1": (254, 242, 0), #cor do 2° layout do BB
    "azul_1": (1, 56, 97),
    "vermelho": (255, 0, 0),
    "verde": (0, 255, 0),
    "preto": (0, 0, 0),
    "branco": (255, 255, 255)
}

def cor_similar(cor1, cor2, tolerancia=50):
    """Verifica se duas cores são similares dentro de uma tolerância."""
    return all(abs(cor1[i] - cor2[i]) <= tolerancia for i in range(3))

def identificar_cor_dominante(imagem):
    """Identifica a cor dominante da imagem e retorna o nome da cor."""
    # Converter a imagem para RGB
    img = imagem.convert("RGB")
    pixels = list(img.getdata())
    
    # Contar as cores
    contador_cores = Counter(pixels)
    cor_dominante = contador_cores.most_common(1)[0][0]  # Pega a cor mais comum

    # Comparar com as cores de referência
    for nome_cor, cor_ref in cores_referencia.items():
        if cor_similar(cor_dominante, cor_ref):
            return nome_cor  # Retorna o nome da cor correspondente

    return "desconhecida"  # Se não encontrar uma cor correspondente

def identificador_layout_img(pdf_bytes):
    """Extrai imagens de um PDF fornecido como um objeto BytesIO."""
    imagens_extraidas = []
    
    try:
        # Abrir o PDF a partir do BytesIO
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        
        # Iterar sobre as páginas do PDF
        for i in range(len(doc)):
            page = doc.load_page(i)
            imagens = page.get_images(full=True)
            
            # Iterar sobre as imagens da página
            for img_index, img in enumerate(imagens):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                
                # Criar um objeto BytesIO a partir dos bytes da imagem
                img_stream = io.BytesIO(image_bytes)
                
                # Abrir a imagem usando Pillow
                imagem = Image.open(img_stream)
                imagens_extraidas.append(imagem)
        
        return imagens_extraidas
    
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        return []


def str_to_number(value):
    if value is None:
        return 0  # Retorna 0 se o valor for None

    # Remove caracteres não numéricos, exceto '.' e ','
    cleaned_value = ''.join(char for char in value if char.isdigit() or char in ',.')

    # Substitui '.' por '' e ',' por '.' para conversão correta
    cleaned_value = cleaned_value.replace('.', '').replace(',', '.')

    try:
        float_value = float(cleaned_value)  # Tenta converter para float
    except ValueError:
        print(f"Erro ao converter '{value}' para float.")  # Mensagem de erro
        return 0  # Retorna 0 em caso de erro

    return float_value



# def identificador_sequencial_pdfs(pdfs):
#     try:
#         colunas_esperadas = {
#             "Sicredi": ["DATA", "DESCRIÇÃO", "DOCUMENTO", "VALOR (R$)", "SALDO (R$)"],
#             "Sicoob": ["DATA", "DOCUMENTO", "HISTÓRICO", "VALOR"],
#             "Banco do Brasil": ["DT. BALANCETE", "DT. MOVIMENTO", "AG.\rORIGEM", "LOTE", "HISTÓRICO", "DOCUMENTO", "VALOR R$", "SALDO"],
#             "Banpará": ["DATA", "DESCRICAO", "DOC.", "VALOR", "SALDO"],
#             "Caixa Layout 1": ["DATA", "NR. DOC.", "HISTÓRICO", "VALOR (R$)", "SALDO (R$)"],
#             "Caixa Layout 2": ["DATA MOV.", "NR. DOC.", "HISTÓRICO", "VALOR", "SALDO"]
#         }

#         resultados = []  # Lista para armazenar os índices, bancos e dados
#        # for indice, pdf in enumerate(pdfs):
#         df = pdfs  # Criar DataFrame
#         colunas_pdf = df.columns.tolist()  # Pegar as colunas do PDF
#         banco_identificado = "Desconhecido"
#         for banco, colunas_banco in colunas_esperadas.items():
#             if set(colunas_pdf) == set(colunas_banco):
#                 banco_identificado = banco
#                 break
#         # Armazena índice, banco e os dados do PDF
#         resultados.append({"indice": indice, "banco": banco_identificado, "dados": df})
#         return resultados
#     except Exception as e:
#         return str(e.args)
    
    
def mapear_valores(df, banco, padraoXLS):
    """
    Ajusta os valores do DataFrame conforme o formato esperado em padraoXLS.
    """
    # Criar um dicionário para armazenar os valores ajustados
    valores_padronizados = {coluna: [] for coluna in padraoXLS}

    # Definir regras de mapeamento das colunas dos bancos para padraoXLS
    mapeamento_colunas = {
        "Sicredi": {"DATA": "Data do Lanc.", "HISTÓRICO": "Hist. Complementar", "VALOR": "Valor da Partida"},
        "Sicoob": {"DATA": "Data do Lanc.", "HISTÓRICO": "Hist. Complementar", "VALOR": "Valor da Partida"},
        "Banco do Brasil": {"DATA": "Data do Lanc.", "HISTÓRICO": "Hist. Complementar", "VALOR": "Valor da Partida"},
        "Banpará": {"DATA": "Data do Lanc.", "HISTÓRICO": "Hist. Complementar", "VALOR": "Valor da Partida"},
        "Caixa Layout 1": {"DATA": "Data do Lanc.", "HISTÓRICO": "Hist. Complementar", "VALOR": "Valor da Partida"},
        "Caixa Layout 2": {"DATA": "Data do Lanc.", "HISTÓRICO": "Hist. Complementar", "VALOR": "Valor da Partida"},
    }

    # Pegar o mapeamento correto baseado no banco identificado
    mapeamento = mapeamento_colunas.get(banco, {})

    # Percorrer cada coluna do mapeamento e organizar os valores em listas
    for coluna_pdf, coluna_padrao in mapeamento.items():
        if coluna_pdf in df.columns:
            valores_padronizados[coluna_padrao] = df[coluna_pdf].tolist()  # Converter a coluna para lista

    # Criar uma lista de dicionários onde cada dicionário representa uma linha do DataFrame
    linhas_ajustadas = [
        {coluna: valores_padronizados[coluna][i] if i < len(valores_padronizados[coluna]) else None for coluna in padraoXLS}
        for i in range(len(df))
    ]

    return linhas_ajustadas 
