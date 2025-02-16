

let inputFille = document.getElementById('fileInput');
const mensageStatus = document.getElementById('mensageStatus');
const uploadButton = document.getElementById('uploadButton');
const spanMensageStatus = document.getElementById('spanMensageStatus');
const InputOk = document.getElementById('confirm');
const divSpanMensageStatus = document.getElementById('divSpanMensageStatus');
const inputCamp = document.getElementById('inputCamp');
const btns = document.getElementById('btns');
const confirmMoreFille = document.getElementById('confirmMoreFille');
const denyMoreFille = document.getElementById('denyMoreFille');
const progress = document.getElementById('progress');
const btnCancel = document.getElementById('btnCancel');
const dangerAlertDiv = document.getElementById('dangerAlert'); 
const spanMensageDanger = document.getElementById('spanMensageDanger');
const spanMensageSelectTypeBank = document.getElementById('spanMensageSelectTypeBank');
const selectTypeBank = document.getElementById('selectTypeBank');
const continueSystemV = document.getElementById('continueSystem');
const spanMensageContinueSystem = document.getElementById('spanMensageContinueSystem');
const checkInputs = document.getElementsByClassName('form-check-input');
const inputCo = document.getElementById('input');
const inputValue = document.getElementById('inputValue');
const btnNexInput = document.getElementById('btnNexInput');

const SuccessMensage = document.getElementById('SuccessMensage');
const ErroMnsage = document.getElementById('ErroMnsage');
const spinner = document.getElementById('spinner');

progress.style.display = 'none';
btnCancel.style.display = 'none';
selectTypeBank.style.display = 'none';
btnNexInput.style.display = 'none';

/**spans */
const erroSpan = document.getElementById('erroSpan');
const successSpan = document.getElementById('successSpan');

export function resetSelecteds(){
    for (let i = 0; i < checkInputs.length; i++) {
        if (checkInputs[i].checked) {
            checkInputs[i].checked = false; // Desmarcar o checkbox
        }
    }
};


export function removeSpinner(){
    spinner.style.display = 'none';
};

export function showSpinner(){   
    spinner.style.display = 'block';
};

export function resetAll(){
    removeProgress();
    removeMensageStatus();
    RemoveBtnNexInput();
    RemoveSuccessMensage();
    removeUploadButton();
    removeInput();
};

export function ShowBtnNexInput(){
    btnNexInput.style.display = 'flex';    
};

export function RemoveBtnNexInput(){
    btnNexInput.style.display = 'none';    
};

export function ShowSuccessMensage(text){
    SuccessMensage.style.display = 'block';
    successSpan.textContent = text;
};

export function RemoveSuccessMensage(){
    SuccessMensage.style.display = 'none';   
};

export async function ShowErroMnsage(text){
    ErroMnsage.style.display = 'block';
    erroSpan.textContent = text;
};

export async function RemoveErroMnsage(){
    ErroMnsage.style.display = 'none';   
};

export function toUploadFille(text, ShowInput=false,tipoArquivo=''){   
    removeInput();
    RemoveBtnNexInput();
    return new Promise((resolve) =>{
        if(tipoArquivo==true){ //if true é do saan
            tipoArquivo = '.xlsx, .xls'
            inputFille.setAttribute('accept', tipoArquivo);
        }else{
            inputFille.setAttribute('accept', tipoArquivo);
        };
        

        if(ShowInput==true){
            showInput();
            showMensageStatus(text);
           
            inputValue.addEventListener('input', ()=>{
                if(inputValue.value.length>0){
                    ShowBtnNexInput();
                }else{
                    RemoveBtnNexInput();
                }
            });
            btnNexInput.addEventListener('click', ()=>{
                resolve(inputValue.value);
            });
        }else{
            showUploadButton();
            showMensageStatus(text);
            
            inputFille.addEventListener('change', (e)=>{
                const files = e.target.files; 
                const fileArray = Array.from(files); 
                resolve(fileArray);             
            });           
        }

    })
    
};


export function showUploadButton(){
    inputCamp.style.display = 'flex';
}

export function removeUploadButton(){
    uploadButton.style.display = 'none';
    inputCamp.style.display = 'none';
}

export function showInput(){
    removeUploadButton();
    inputCo.style.display = 'flex';
}

export function removeInput(){
    inputCo.style.display = 'none';
}


export function showMensageStatus(text){   
    uploadButton.style.display = 'block';
    divSpanMensageStatus.style.display = 'block';
    mensageStatus.style.display = 'block';
    spanMensageStatus.textContent = text; 
}

export function removeMensageStatus(){
    removeUploadButton();
    removeInput();
    RemoveBtnNexInput();
    divSpanMensageStatus.style.display = 'none';
    mensageStatus.style.display = 'none';    
}

export function clearInput(){
    inputFille.value = '';
}

export function removeBtnsFromMensageStatus(){
    btns.style.display = 'none'; 
    removeUploadButton();
    removeInput();
}

export function showBtnsFromMensageStatus(){
    btns.style.display = 'inline-block';
    removeUploadButton();
 
}

export function mensageStatusRemove(){
    mensageStatus.style.display = 'none';
}
/*
function gerFilleInputValue(){   
    const fileV =  inputFille.value;            
    if(fileV){
        inputFille.value = '';
        return fileV;
    }else{
        console.log('sem arquivo')
    }
}*/

function showUploadInput(){
    uploadButton.style.display = 'block';
}


export function showInputOk(){
    InputOk.style.display = 'block';
}

function removeInputOk(){
    InputOk.style.display = 'none';
}

export function showProgress(){
    progress.style.display = 'flex'
}

export function removeProgress(){
    progress.style.display = 'none'
}

export function showBtnCancel(){
    btnCancel.style.display = 'flex'
}

export function removeBtnCancel(){
    btnCancel.style.display = 'none'
}

export function removeAlertDanger(){     
    dangerAlertDiv.style.display = 'none'
    spanMensageDanger.style.display = 'none'  
}

export async function showAlertDanger(text, time=false){ 
    mensageStatus.style.display = 'none';    
    dangerAlertDiv.style.display = 'block'
    spanMensageDanger.style.display = 'block'
    spanMensageDanger.textContent = text;
    spanMensageDanger.style.textAlign = 'center';
    if(time==true){
        // Oculta a mensagem após 3 segundos (3000 milissegundos)
        setTimeout(() => {
            removeAlertDanger();
        }, 3000);
    }
};

export async function readPdf(file) {
    return new Promise((resolve, reject) => {
        try {
            if (file) {
                const reader = new FileReader();
                reader.onload = function(event) {
                    const base64String = event.target.result.split(',')[1];       
                    resolve({ status: true, data: base64String }); // Retorna um objeto
                };
                reader.onerror = function(erro) {
                    reject({ status: false, error: erro });
                };
                reader.readAsDataURL(file); // Lê o arquivo como URL de dados
            } else {
                reject({ status: false, error: "Erro: selecione um arquivo" });
            }
        } catch (e) {
            reject({ status: false, error: e });
        }
    });
}


export async function readExcel(file) {
    return new Promise((resolve, reject) => {
        const fileReader = new FileReader();
        
        fileReader.onload = (event) => {
            const binaryStr = event.target.result;
            const workbook = XLSX.read(binaryStr, { type: "binary" });

            // Obtenha o nome da primeira planilha
            const sheetName = workbook.SheetNames[0];
            const sheetData = workbook.Sheets[sheetName];

            // Converta os dados da planilha para um formato JSON
            const data = XLSX.utils.sheet_to_json(sheetData, { header: 1 });

            // Resolva a Promise com os dados
            resolve([true, data]);
        };

        fileReader.onerror = (error) => {
            reject([false, error]);
        };

        // Use readAsBinaryString para arquivos binários
        fileReader.readAsBinaryString(file);
    });
}


export async function readJsPdf(value) {
    const listPdf = [];

    for(const i of value){
        const [sucess , base64Fille] = await readPdf(i);
        if(sucess==true){
            listPdf.push(base64Fille);
        }else{
            return [false , 'JS encontrou erro ao ler o arquivo ' + i.name]
        }
        
    }
    return listPdf;
};


export function progresso(valor) {
    // Acessa a barra de progresso
    const progressBar = document.getElementById('progress-bar');

    if (valor !== null) {
        // Obtém o valor atual da largura (em %)
        const progressText = progressBar.textContent;
        let atual = parseInt(progressText, 10); // Converte o valor de string para inteiro    

        // Calcula o novo valor (não pode ultrapassar 100%)
        let novoValor = atual + valor;
        if (novoValor > 100) novoValor = 100; // Limita em 100%

        // Atualiza a largura da barra
        progressBar.style.width = novoValor + '%';

        // Atualiza o texto da barra
        progressBar.textContent = novoValor + '%';

        // Atualiza o atributo aria-valuenow
        const progress = document.querySelector('.progress');
        progress.setAttribute('aria-valuenow', novoValor);
    } else {
        // Se valor for null, reseta a barra de progresso para 0%
        progressBar.style.width = '0%';
        progressBar.textContent = '0%';

        // Atualiza o atributo aria-valuenow
        const progress = document.querySelector('.progress');
        progress.setAttribute('aria-valuenow', 0);
    }
}


export async function showSelectTypeBank(){    
    selectTypeBank.style.display = 'block';
};

export async function removeSelectTypeBank(){
    selectTypeBank.style.display = 'none';
};

export function ShowcontinueSystem(text){
    const yes = document.getElementById('yes');
    const not = document.getElementById('not');

    return new Promise((resolve, reject) => {
        continueSystemV.style.display = 'block';
        btns.style.display = 'flex';
        spanMensageContinueSystem.textContent = text;

        yes.onclick =()=>{
            resolve(true);
        };
        not.onclick = ()=>{
            resolve(false);
        };
    })
    
};

export function RemoveContinueSystem(){
    continueSystemV.style.display = 'none';
};

export function resetSystem(){
    RemoveSuccessMensage();
    removeSelectTypeBank();
    removeMensageStatus();
    RemoveContinueSystem();
    resetSelecteds();
    progresso(null);
}

export async function verifyStatusAfterProcess(pythonReadPdf, position,counter){    
    showMensageStatus("Finalizando Tratamento deste "+counter+ "° arquivo");  
    const treatPdf = await window.pywebview.api.treatPdf(pythonReadPdf, position);
    return treatPdf
    /*if(treatPdf[0]==false){
        return treatPdf;
    }
    await showMensageStatus("Salve o documento tratado");
    await new Promise(resolve => setTimeout(resolve, 2000));
    const saving  = await window.pywebview.api.save(treatPdf[1]);
    progresso(40)
    return saving;*/
}

