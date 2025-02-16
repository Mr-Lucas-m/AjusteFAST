

import {toUploadFille, showProgress, showAlertDanger, mensageStatusRemove, readPdf, progresso, showMensageStatus, removeUploadButton, verifyStatusAfterProcess} from '../main.js'


let counter=0;
//let valueProgress =0;
let valueProgressGlobal =40/3;
let valueBanks =0;
let listResult =[];
let listNameBak =[];

export class ControllerJs{
    
    async startController(listPdf, filleExcelModel, inputValue, nameBank) {
        try{
            console.log("contro")
            if(listPdf){
                for(const value of listPdf) {                           
                        valueBanks= 60/listPdf.length;
                        removeUploadButton();
                        if(value[1]=="1"){                            
                            counter=0;                                          
                            const internList =[]                                        
                            let valueProgress1 = valueBanks/value[0].length/3; 
                            
                            for(let fille of value[0]){       
                                counter++;                 
                               // listNameBak.push([nameBank[parseInt(value[0])], value[0].length]);             
                                progresso(Math.ceil(valueProgress1));
                                const readerPdfV = await readPdf(fille);
                                if(readerPdfV[0]==false){
                                    return readerPdfV;
                                }
                                showProgress();
                                progresso(Math.ceil(valueProgress1));
                                showMensageStatus("Tratando o " +counter +"º PDF do Sicob");                                    
                                const pythonReadPdf = await window.pywebview.api.Sicob(readerPdfV.data);  
                                if(pythonReadPdf[0]==false){
                                    return pythonReadPdf
                                }
                                progresso(Math.ceil(valueProgress1));
                                const verifyStatusAfterProcessV = await verifyStatusAfterProcess([pythonReadPdf[1],pythonReadPdf[2],pythonReadPdf[3]],2,counter);
                                if(verifyStatusAfterProcessV[0]==false){
                                    return verifyStatusAfterProcessV
                                }
                                internList.push(verifyStatusAfterProcessV[1]);
                            }
                            listResult.push([internList, 1]);
                        }                                                        
                        
                        else if(value[1]=="2"){
                            const internList =[];
                            counter=0;                                                         
                            let valueProgress2 = valueBanks/value[0].length/3;                            
                            for(let fille of value[0]){     
                              //  listNameBak.push([nameBank[parseInt(value[0])], value[0].length]);             
                                counter++;                                                       
                                progresso(Math.ceil(valueProgress2));
                                const readerPdfV  = await readPdf(fille);
                                if(readerPdfV[0]==false){
                                    return readerPdfV;
                                }
                                showProgress();
                                progresso(Math.ceil(valueProgress2));
                                showMensageStatus("Tratando o " +counter +"º PDF do Banco do Brasil");                                    
                                const pythonReadPdf = await window.pywebview.api.Banco_do_Brasil(readerPdfV.data);  
                                if(pythonReadPdf[0]==false){
                                    return pythonReadPdf
                                }

                                progresso(Math.ceil(valueProgress2));
                                const verifyStatusAfterProcessV = await verifyStatusAfterProcess([pythonReadPdf[1],pythonReadPdf[2],pythonReadPdf[3]],4,counter);
                                if(verifyStatusAfterProcessV[0]==false){
                                    return verifyStatusAfterProcessV
                                }
                                internList.push(verifyStatusAfterProcessV[1]);
                            }       
                            listResult.push([internList, 2]);                
                        }
                        else if(value[1]=="3"){
                            const internList =[]    
                            counter=0;                                                         
                            let valueProgress3 = valueBanks/value[0].length/3;                            
                            for(let fille of value[0]){  
                                counter++;                                                             
                                progresso(Math.ceil(valueProgress3));                               
                                const readerPdfV  = await readPdf(fille);
                                if(readerPdfV[0]==false){
                                    return readerPdfV;
                                }
                                showProgress();
                                progresso(Math.ceil(valueProgress3));
                                showMensageStatus("Tratando o " +counter +"º PDF do Sicred");                                    
                                const pythonReadPdf = await window.pywebview.api.Sicred(readerPdfV.data);  
                                if(pythonReadPdf[0]==false){
                                    return pythonReadPdf
                                }

                                progresso(Math.ceil(valueProgress3));
                                const verifyStatusAfterProcessV = await verifyStatusAfterProcess([pythonReadPdf[1],pythonReadPdf[2],pythonReadPdf[3]],4,counter);
                                if(verifyStatusAfterProcessV[0]==false){
                                    return verifyStatusAfterProcessV
                                }
                                internList.push(verifyStatusAfterProcessV[1]);
                            }           
                            listResult.push([internList, 3]);                      
                        }
                        else if(value[1]=="4"){
                            const internList =[]     
                            counter=0;                                                         
                            let valueProgress4 = valueBanks/value[0].length/3;                            
                            for(let fille of value[0]){  
                                counter++;                                                             
                                progresso(Math.ceil(valueProgress4));                                
                                const readerPdfV  = await readPdf(fille);
                                if(readerPdfV[0]==false){
                                    return readerPdfV;
                                }
                                showProgress();
                                progresso(Math.ceil(valueProgress4));
                                showMensageStatus("Tratando o " +counter +"º PDF da Caixa");                                    
                                const pythonReadPdf = await window.pywebview.api.caixa(readerPdfV.data);  
                                if(pythonReadPdf[0]==false){
                                    return pythonReadPdf
                                }

                                progresso(Math.ceil(valueProgress4));
                                const verifyStatusAfterProcessV = await verifyStatusAfterProcess([pythonReadPdf[1],pythonReadPdf[2],pythonReadPdf[3]],2,counter);
                                if(verifyStatusAfterProcessV[0]==false){
                                    return verifyStatusAfterProcessV
                                }
                                internList.push(verifyStatusAfterProcessV[1]);
                            }
                            listResult.push([internList, 4]);                                
                        }
                        else if(value[1]=="5"){
                            const internList =[]  
                            counter=0;                                                         
                            let valueProgress5 = valueBanks/value[0].length/3; 
                           
                            for(let fille of value[0]){            
                                counter++;                                                   
                                progresso(Math.ceil(valueProgress5)); 
                                const readerPdfV  = await readPdf(fille);
                                if(readerPdfV[0]==false){
                                    return readerPdfV;
                                }
                                showProgress();
                                progresso(Math.ceil(valueProgress5));
                                showMensageStatus("Tratando o " +counter +"º PDF do Banpará");                                    
                                const pythonReadPdf = await window.pywebview.api.Banpara(readerPdfV.data);  
                                if(pythonReadPdf[0]==false){
                                    return pythonReadPdf
                                }

                                progresso(Math.ceil(valueProgress5));
                                const verifyStatusAfterProcessV = await verifyStatusAfterProcess([pythonReadPdf[1],pythonReadPdf[2],pythonReadPdf[3]],1,counter);
                                if(verifyStatusAfterProcessV[0]==false){
                                    return verifyStatusAfterProcessV
                                }
                                internList.push(verifyStatusAfterProcessV[1]);
                            }     
                            listResult.push([internList, 5]);                            
                        };        
                };
                progresso(Math.ceil(valueProgressGlobal));
                showMensageStatus("Finalizando o tratamento de todos os bancos"); 
               // const treatPdfs_excel = await window.pywebview.api.tratarPdf_Excel(JSON.stringify(listResult), JSON.stringify(excelSaanValue), inputValue, nameBank);
                const formatP = await window.pywebview.api.get_padrao(JSON.stringify(listResult), filleExcelModel, inputValue);
                if(formatP[0]==false){
                    return formatP;
                }else{
                    showMensageStatus("Salve os dados tratados");
                    progresso(Math.ceil(valueProgressGlobal)-1);
                    const save = await window.pywebview.api.salvarFrame(formatP[1]);
                    if(save[0]=false){
                        return save;
                    }
                    progresso(1);
                    return [true];
                }
            }else{
                console.log("sem arquivos");
            };
            
        }catch(e){
            console.log(e)
        };                                    
    }
}