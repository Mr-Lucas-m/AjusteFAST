import { ControllerJs } from "../controlerJs/controller.js";
import {removeSpinner,showSpinner, readPdf, removeBtnsFromMensageStatus, showBtnsFromMensageStatus, removeSelectTypeBank, toUploadFille, clearInput, showInputOk,showAlertDanger, ShowSuccessMensage, ShowErroMnsage,resetAll, ShowcontinueSystem, RemoveSuccessMensage, showSelectTypeBank, resetSystem, readExcel, removeMensageStatus, removeUploadButton, RemoveContinueSystem, RemoveErroMnsage} from "../main.js";

let inputFille = document.getElementById('fileInput');
const mensageStatus = document.getElementById('mensageStatus');
const uploadButton = document.getElementById('uploadButton');
const spanMensageStatus = document.getElementById('spanMensageStatus');
const InputOk = document.getElementById('confirm');
const btns = document.getElementById('btns');
const confirmMoreFille = document.getElementById('confirmMoreFille');
const denyMoreFille = document.getElementById('denyMoreFille');
//others
const validTypePdf = 'pdf';
const validTypeExcel = 'xlsx';
const validExtensions = [validTypeExcel, 'xls']; // Tipos válidos

let fillePdf = '';
let filleExcel = '';
let inputValue = '';
let fillesPDFList = '';
let filleExcelModel = '';
let excelSaanValue ='';
let selectedBank = '';
let modelFille = '';
let listPdf = [];
let listNameBank =[];


async function toggleButton() {  
    showSelectTypeBank();
    removeMensageStatus();  

    const checkInputs = document.getElementsByClassName('form-check-input');
    const btnNexSelectedBanc = document.getElementById('btnNex');  
    btnNexSelectedBanc.style.display = 'none';

    // Clear previous event listeners
    Array.from(checkInputs).forEach(i => {
        const existingClickListener = i.getAttribute('data-click-listener');
        if (existingClickListener) {
            i.removeEventListener('click', existingClickListener);
        }
    });

    Array.from(checkInputs).forEach(i => {
        const handleClick = () => {
            btnNexSelectedBanc.style.display = 'block';

            const handleNextClick = async () => {
                const selectedRadio = Array.from(checkInputs).find(input => input.checked);
                if (selectedRadio) {
                    //selectedBank = selectedRadio.id; // Get the text associated with the selected button
                    selectedRadio.checked = false; // Uncheck the selected button
                    selectedRadio.disabled = true;
                    // Remove the event listeners
                    i.removeEventListener('click', handleClick);
                    btnNexSelectedBanc.removeEventListener('click', handleNextClick);
                    console.log('removed'); // Log when the listener is removed
                    await removeSelectTypeBank();
                    // Only call uploadPDFs after clicking "Next"
                    await uploadPDFs(selectedRadio.value);
                }
            };

            btnNexSelectedBanc.addEventListener('click', handleNextClick);
        };

        // Store the function reference to remove it later
        i.setAttribute('data-click-listener', handleClick);
        i.addEventListener('click', handleClick);
    });
}

window.onload = function() {
    if (navigator.onLine) {
        removeSpinner();
        toggleButton(); // Chama a função se houver internet
    } else {
        showSpinner();
    }
};

function TypeBanckNumber(value){
    switch (value) {
        case "BANCO SICOB":
            return "1" 
        case "BANCO DO BRASIL":
            return "2" 
        case "BANCO SICOB":
            return "1"  
        case "SICRED":
            return "3"
        case "CAIXA":
            return "4"  
        case "BANPARA":
            return "5"   
        default:
            break;
    }
}

async function uploadPDFs(nameBank) {
    removeMensageStatus();         
    let contueSystem = true;

    while (contueSystem) {        
                
        fillePdf = await toUploadFille('Você deve selecionar os arquivos PDF que deseja tratar apenas do ' + nameBank + " pode ser quantos você desejar",false, '.pdf');
        listPdf.push([fillePdf, TypeBanckNumber(nameBank)]);
        listNameBank.push(nameBank);
        removeMensageStatus();         
        contueSystem = await ShowcontinueSystem("Deseja tratar outros PDFS de outro banco?");    
        RemoveContinueSystem();    
        if (contueSystem) {            
            // Only call toggleButton after confirming the user wants to process another bank
            await toggleButton();           
        }
    }
   
    //filleExcel = await toUploadFille('Agora você deve selecionar o arquivo Excel extraido do Saan, é obrigatório conter os mesmos dados dos PDFS que vc selecionou',false, true);        
       

    RemoveSuccessMensage();
    inputValue = await toUploadFille('Por favor, digite o Código Histórico Padrão',true, false);
    modelFille = await toUploadFille('Por último, inclua o modelo para garantir que a extração siga um formato padrão',false, true);
    removeMensageStatus();
    
    //ShowSuccessMensage("Aguarde..");
    //const readingSaanExcel = await readExcel(filleExcel[0]);
    //if(readingSaanExcel[0]==false){
    //    ShowErroMnsage(readingSaanExcel[1]);
    //}else{           
    //    excelSaanValue = readingSaanExcel[1];            
    //    clearInput();            
    //};

    ShowSuccessMensage("Aguarde, validando o arquivo do Modelo padrão");
    const readingXls = await readExcel(modelFille[0]);
    if(readingXls[0]==false){
        ShowErroMnsage(readingXls[1]);
    }else{           
        filleExcelModel = readingXls[1];            
        clearInput();            
    };   
    // Inicia o controlador
    resetAll();
    const controller = await new ControllerJs().startController(listPdf, filleExcelModel, inputValue, listNameBank);
    resetAll();
    ShowSuccessMensage("Aguarde");  
    if (controller[0] == true) {
        await new Promise(resolve => {
            setTimeout(() => {        
                ShowSuccessMensage("Operação bem sucedida");  
                resolve(); // Resolve a Promise após exibir a mensagem
            }, 4000); // Espera 4 segundos antes de exibir a próxima mensagem
        });
        await new Promise(resolve => {
            setTimeout(() => {        
                ShowSuccessMensage("Obrigado por usar o sistema! Você pode fechar esta janela agora");  
                resolve(); // Resolve a Promise após exibir a mensagem
            }, 4000); // Espera 4 segundos antes de exibir a próxima mensagem
        });                
    } else {
        RemoveSuccessMensage();
        if(controller.length>2){
            if(controller[2].length>0){                
                ShowErroMnsage(`Erro ao tratar o banco: ${controller[2][0][0]} <br> Detalhes do erro: <br>
                    ${controller[2][0][1]}
                `);
            }
        }else{
            ShowErroMnsage("Erro: "+controller[1]);
        }
        
        
    }
};









