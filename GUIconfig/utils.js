function ltrim(str) {
  return str.replace(/^s+/,"");
}

function getCampos() { // pega os campos do formulário e retorna uma string
  var textToWrite = '';
  
  // número de questões 
  if (document.getElementById("numQE").value != ''){
    textToWrite += 'numQE \t :: ' + document.getElementById("numQE").value;
  } else { 
    textToWrite += 'numQE \t :: 0';
  } 
  textToWrite += '\t ::  number of easy questions \n';

 if (document.getElementById("numQM").value != ''){
    textToWrite += 'numQM \t :: ' + document.getElementById("numQM").value;
  } else { 
    textToWrite += 'numQM \t :: 0';
  } 
  textToWrite += '\t ::  number of mean questions \n';

 if (document.getElementById("numQH").value != ''){
    textToWrite += 'numQH \t :: ' + document.getElementById("numQH").value;
  } else { 
    textToWrite += 'numQH \t :: 0';
  } 
  textToWrite += '\t ::  number of hard questions \n';

 if (document.getElementById("numQT").value != ''){
    textToWrite += 'numQT \t :: ' + document.getElementById("numQT").value;
  } else { 
    textToWrite += 'numQT \t :: 0';
  } 
  textToWrite += '\t ::  number of textual questions \n\n';

  // pastas 
  if (document.getElementById("folderCourse").value != ''){
    textToWrite += 'folderCourse     :: ' + document.getElementById("folderCourse").value;
  } else { 
    textToWrite += 'folderCourse     :: defaultCourse ';
  } 
  textToWrite += '\t :: folder containing the classes in csv files \n';

  if (document.getElementById("folderQuestions").value != ''){
    textToWrite += 'folderQuestions  :: ' + document.getElementById("folderQuestions").value;
  } else { 
    textToWrite += 'folderQuestions  :: defaultQuestions ';
  } 
  textToWrite += '\t :: folder containing the database issues in txt files \n\n';

  // random
  if (document.getElementById("randomTests").checked){
    textToWrite += 'randomTests \t :: 1 ';
  } else { 
    textToWrite += 'randomTests \t :: 0 ';
  } 
  textToWrite += '\t :: =0, questions and answers not random \n';

  // GAB
  if (document.getElementById("duplexPrinting").checked){
    textToWrite += 'duplexPrinting \t :: 1 ';
  } else { 
    textToWrite += 'duplexPrinting \t :: 0 ';
  } 
  textToWrite += '\t :: =0, printing on one side of the sheet, cc, printing double-sided \n';
  
  // Impressão 
  var form = document.getElementById("myform");  
  textToWrite += 'MCTest_sheets \t :: ' + form.elements["myform"].value;
  textToWrite += '\t :: =0 only answer sheet; =1 only questions; =2 cc \n';
  
  if (document.getElementById("template").checked){
    textToWrite += 'template \t :: 1 ';
  } else { 
    textToWrite += 'template \t :: 0 ';
  } 
  textToWrite += '\t :: =0, unsaved file with the templates *_GAB \n';
  
  // layout do gabarito
  if (document.getElementById("maxQuestQuadro").value != ''){
    textToWrite += 'maxQuestQuadro \t :: ' + document.getElementById("maxQuestQuadro").value;
  } else { 
    textToWrite += 'maxQuestQuadro \t :: 0';
  } 
  textToWrite += '\t :: maximum number of questions per answer sheet \n';

  if (document.getElementById("maxQuadrosHoz").value != ''){
    textToWrite += 'maxQuadrosHoz \t :: ' + document.getElementById("maxQuadrosHoz").value;
  } else { 
    textToWrite += 'maxQuadrosHoz \t :: 0';
  } 
  textToWrite += '\t :: maximum number of questions in horizontally \n\n';
  
  // Cabecalho 
  if (document.getElementById("title").value != ''){
    textToWrite += 'title    :: ' + document.getElementById("title").value + '\n';
  } else { 
    textToWrite += 'title    :: University ... \n';
  } 

  if (document.getElementById("course").value != ''){
    textToWrite += 'course   :: ' + document.getElementById("course").value + '\n';
  } else { 
    textToWrite += 'course   :: Course ... \n';
  } 

  if (document.getElementById("teachers").value != ''){
    textToWrite += 'teachers :: ' + document.getElementById("teachers").value + '\n';
  } else { 
    textToWrite += 'teachers :: Teachers ... \n';
  } 

  if (document.getElementById("period").value != ''){
    textToWrite += 'period   :: ' + document.getElementById("period").value + '\n';
  } else { 
    textToWrite += 'period   :: Period ... \n';
  } 

  if (document.getElementById("modality").value != ''){
    textToWrite += 'modality :: ' + document.getElementById("modality").value + '\n';
  } else { 
    textToWrite += 'modality :: Modality ... \n ';
  } 

  if (document.getElementById("date").value != ''){
    textToWrite += 'date     :: ' + document.getElementById("date").value + '\n';
  } else { 
    textToWrite += 'date     :: date ... \n';
  } 

  if (document.getElementById("logo").value != ''){
    textToWrite += 'logo     :: ' + document.getElementById("logo").value + '\n';
  } else { 
    textToWrite += 'logo     :: ufabc.eps \n ';
  } 

  if (document.getElementById("language").value != ''){
    textToWrite += 'language :: ' + document.getElementById("language").value + '\n\n';
  } else { 
    textToWrite += 'language :: English ... \n\n ';
  } 

  // Instruções
  if (document.getElementById("instructions1").value != ''){
    textToWrite += 'instructions1 :: \n' + document.getElementById("instructions1").value + '\n';
  } else { 
    textToWrite += 'instructions1 :: \n \item blá ... \n ';
  }
  
  if (document.getElementById("instructions2").value != ''){
    textToWrite += 'instructions2 :: \n' + document.getElementById("instructions2").value + '\n';
  } else { 
    textToWrite += 'instructions2 :: \n \item blá ... \n ';
  }
  
  if (document.getElementById("instructions3").value != ''){
    textToWrite += 'instructions3 :: \n' + document.getElementById("instructions3").value + '\n';
  } else { 
    textToWrite += 'instructions3 :: \n \item blá ... \n ';
  }

  textToWrite += 'endTable :: \n';
  
  return textToWrite;		    
}
		    
function saveTextAsFile() {
  var textToWrite = getCampos();
		    
  var textFileAsBlob = new Blob([textToWrite], {type:'text/plain'});
  var fileNameToSaveAs = document.getElementById("inputFileNameToSaveAs").value;

  var downloadLink = document.createElement("a");
  downloadLink.download = fileNameToSaveAs;
  downloadLink.innerHTML = "Download File";
  if (window.webkitURL != null) {
    // Chrome allows the link to be clicked
    // without actually adding it to the DOM.
    downloadLink.href = window.webkitURL.createObjectURL(textFileAsBlob);
  } else {
    // Firefox requires the link to be added to the DOM
    // before it can be clicked.
    downloadLink.href = window.URL.createObjectURL(textFileAsBlob);
    downloadLink.onclick = destroyClickedElement;
    downloadLink.style.display = "none";
    document.body.appendChild(downloadLink);
  }

  downloadLink.click();
}

function destroyClickedElement(event) {
  document.body.removeChild(event.target);
}

function loadFileAsText() {
  var fileToLoad = document.getElementById("fileToLoad").files[0];
		    
  var fileReader = new FileReader();
  fileReader.onload = function(fileLoadedEvent)  {
    var str = fileLoadedEvent.target.result;
    
    var lines = str.split('\n');
    for(var i = 0;i < lines.length;i++){
	      var s = lines[i].split('::');
	      if (s.length>1) {
          switch(s[0].trim()) {
            case 'numQE':
              document.getElementById("numQE").value = s[1].trim();
              break;
            case 'numQM':
              document.getElementById("numQM").value = s[1].trim();
              break;
            case 'numQH':
              document.getElementById("numQH").value = s[1].trim();
              break;
            case 'numQT':
              document.getElementById("numQT").value = s[1].trim();
              break;
            case 'folderCourse':
              document.getElementById("folderCourse").value = s[1].trim();
              break;
            case 'folderQuestions':
              document.getElementById("folderQuestions").value = s[1].trim();
              break;
            case 'randomTests':
              if (s[1].trim()=="1") {
                document.getElementById("randomTests").checked = true;
              } else {
                document.getElementById("randomTests").checked = false;
              }
              break;
              
            case 'duplexPrinting':
              if (s[1].trim()=="1") {
                document.getElementById("duplexPrinting").checked = true;
              } else {
                document.getElementById("duplexPrinting").checked = false;
              }
              break;
              
            case 'MCTest_sheets':
              if (s[1].trim()=="0") {
                document.forms["myform"]["sheets0"].checked=true;
              } else if (s[1].trim()=="1") {
                document.forms["myform"]["sheets1"].checked=true;
              } else if (s[1].trim()=="2") {
                document.forms["myform"]["sheets2"].checked=true;
              }
              break;

            case 'template':
              if (s[1].trim()=="1") {
                document.getElementById("template").checked = true;
              } else {
                document.getElementById("template").checked = false;
              }
              break;
              
            case 'maxQuestQuadro':
              document.getElementById("maxQuestQuadro").value = s[1].trim();
              break;  
              
            case 'maxQuadrosHoz':
              document.getElementById("maxQuadrosHoz").value = s[1].trim();
              break;   
              
              // cabeçalho
            case 'title':
              document.getElementById("title").value=s[1].trim();
              break; 

            case 'course':
              document.getElementById("course").value = s[1].trim();
              break; 

            case 'teachers':
              document.getElementById("teachers").value = s[1].trim();
              break; 

            case 'period':
              document.getElementById("period").value = s[1].trim();
              break; 

            case 'modality':
              document.getElementById("modality").value = s[1].trim();
              break; 

            case 'date':
              document.getElementById("date").value = s[1].trim();
              break; 

            case 'logo':
              document.getElementById("logo").value = s[1].trim();
              break; 
              
            case 'language':
              document.getElementById("language").value = s[1].trim();
              break; 
              
              // instruções
            case 'instructions1':
              var ss = ''; i++;
              do {
                s = lines[i].split('::');
                if (s.length<=1 && s != '') {
                  ss += s + '\n';
                }
              } while (s.length<=1 && i++ < lines.length); 
              i--;
              document.getElementById("instructions1").value = ss;
              break; 
  
            case 'instructions2':
              var ss = ''; i++;
              do {
                s = lines[i].split('::');
                if (s.length<=1 && s != '') {
                  ss += s + '\n';
                }
              } while (s.length<=1 && i++ < lines.length); 
              i--;
              document.getElementById("instructions2").value = ss;
              break; 
              
              case 'instructions3':
              var ss = ''; i++;
              do {
                s = lines[i].split('::');
                if (s.length<=1 && s != '') {
                  ss += s + '\n';
                }
              } while (s.length<=1 && i++ < lines.length); 
              i--;
              document.getElementById("instructions3").value = ss;
              break; 
                                                              
          }
        }
    }
  };
  fileReader.readAsText(fileToLoad, "UTF-8");
}		       

