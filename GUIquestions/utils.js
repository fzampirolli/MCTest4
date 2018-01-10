document.addEventListener('DOMContentLoaded', function onDOMContentLoaded() {
    document.querySelector('#update').addEventListener('click', updatePreview);
function updatePreview() {

      document.getElementById("campoPDF").value = getCamposTex();
      document.getElementById("campoPDF").disabled = true;

      var text = document.getElementById("campoPDF").value;

      var iframe = document.querySelector('iframe');
      iframe.src = 'https://latexonline.cc/compile?text=' + encodeURIComponent(text);
    }
});


function getSelectedOption(sel) {
    var opt;
    for ( var i = 0, len = sel.options.length; i < len; i++ ) {
        opt = sel.options[i];
        if ( opt.selected === true ) {
            break;
        }
    }
    return opt;
}


function getCampos() { // pega os campos do formulário e retorna uma string no formato do MCTest
  var textToWrite;
  var text = '';
  var opt = getSelectedOption(correctAnswer);
  
  if (document.getElementById("campo0").value != '') {
       textToWrite = getSelectedOption(difficulty).value + '::'
       if (document.getElementById("topic").value != ''){
          textToWrite += document.getElementById("topic").value + '::';
       } else { text = ''} 
       if (document.getElementById("variation").value != ''){
          textToWrite += document.getElementById("variation").value + '::';
       }
       textToWrite += '\n' + document.getElementById("campo0").value+  '\n'; // enunciado da questão
  } 

  if (document.getElementById("difficulty").value != "QT") {  // pega as alternativas, se não for "QT"				   
    for(var i = 0;i < 7;i++){
      if (document.getElementById("campo"+(i+1).toString()).value != '') {
         if (opt.text == (i+1).toString()) {						   
           text = '+';
         } else { text = '-';} 			   
         textToWrite += 'A' + text + ': ' + document.getElementById("campo"+(i+1).toString()).value  + '\n';
      }		      
    }
  }
  return textToWrite;		    
}

function getCamposTex() {
   var textToWrite = getCampos();  
   const q = new MCTestQuestion('','','',0,'',[]); 
   q.strToQuestion(textToWrite);		    

   return q.questionToTex();
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
    var textFromFileLoaded = fileLoadedEvent.target.result;

    const qLoad = new MCTestQuestion('','','',0,'',[]); 
    qLoad.strToQuestion(textFromFileLoaded);
						   
    document.getElementById("campo0").value = qLoad.question;
    document.getElementById("variation").value = qLoad.variation;
    document.getElementById("topic").value = qLoad.topic;
    document.getElementById("difficulty").value = qLoad.difficulty;
    document.getElementById("correctAnswer").value = qLoad.correctAnswer+1;
						   
    for(var i = 0;i <  qLoad.answers.length;i++){
      document.getElementById("campo"+(i+1).toString()).value = qLoad.answers[i];
		      
    }
  };
  fileReader.readAsText(fileToLoad, "UTF-8");
}		       

function habilitaBtn () {
    var op = document.getElementById("difficulty").value;
    if (op == "QT") {
        document.getElementById("correctAnswer").disabled = true;
        document.getElementById("campo1").disabled = true;
        document.getElementById("campo2").disabled = true;
        document.getElementById("campo3").disabled = true;
        document.getElementById("campo4").disabled = true;
        document.getElementById("campo5").disabled = true;
        document.getElementById("campo6").disabled = true;
        document.getElementById("campo7").disabled = true;
  } else {
        document.getElementById("correctAnswer").disabled = false;
        document.getElementById("campo1").disabled = false;
        document.getElementById("campo2").disabled = false;
        document.getElementById("campo3").disabled = false;
        document.getElementById("campo4").disabled = false;
        document.getElementById("campo5").disabled = false;
        document.getElementById("campo6").disabled = false;
        document.getElementById("campo7").disabled = false;
  }
}

var habilitar = true;
		       
function habilitarAux() {
  if(habilitar & document.getElementById('simbLatex').checked) {

    EqEditor.embed('editor0','things','mini', 'en-us');
    var a0=new EqTextArea('equation1', 'campo0');
    var a1=new EqTextArea('equation2', 'campo1');
    var a2=new EqTextArea('equation3', 'campo2');
    var a3=new EqTextArea('equation4', 'campo3');
    var a4=new EqTextArea('equation5', 'campo4');
    var a5=new EqTextArea('equation6', 'campo5');
    var a6=new EqTextArea('equation7', 'campo6');
    var a7=new EqTextArea('equation7', 'campo7');
    EqEditor.add(a0,false);
    EqEditor.add(a1,false);
    EqEditor.add(a2,false);
    EqEditor.add(a3,false);
    EqEditor.add(a4,false);
    EqEditor.add(a5,false);
    EqEditor.add(a6,false);
    EqEditor.add(a7,false);

    habilitar = false;      
  }
}
	
