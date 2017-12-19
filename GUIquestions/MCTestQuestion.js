class MCTestQuestion {
  constructor(difficulty,topic,variation,correctAnswer,question,answers) {
      this.topic = topic;
      this.variation = variation
      this.difficulty = difficulty;
      this.correctAnswer = correctAnswer
      this.question = question;
      this.answers = answers
  }
  
  strToQuestion (str) {

    var lines = str.split('\n');
    var question='';
    var answer=[];
    var countAnswers=0;
    for(var i = 0;i < lines.length;i++){
      if (i===0) { // dados gerais da questão
	var s = lines[i].split('::');

	if (s.length>3) {
	    this.difficulty     = s[0];
	    this.topic  = s[1];
	    this.variation = s[2];
	} else if (s.length==3) {
	    this.difficulty     = s[0];
	    if (s[1].length == 1) {
	      this.variation = s[1];
	    } else {
	      this.topic  = s[1];
	    }
	} else if (s.length==2) {
	    this.difficulty     = s[0];
	} else {
	  window.alert("Erro: cabeçalho não segue padrão!")
	}
    	  
	if (s.length>=2) {
	  while (lines[++i].substr(0, 3)!='A-:' & lines[i].substr(0, 3)!='A+:') {
	    question += lines[i].replace(/^\s+/,"")+'\n'; // retira espaço no início
	  }
	  i--;
	  this.question = question;
	}
      } else {
	if (lines[i].substr(0, 3)=='A-:' || lines[i].substr(0, 3)=='A+:') {
	  if (lines[i].substr(0, 3)=='A+:') {
	    this.correctAnswer = countAnswers;
	  }
	  answer = lines[i].substr(4, lines[i].length).replace(/^\s+/,"");
	  while (++i < lines.length-1 & lines[i].substr(0, 3)!='A-:' & lines[i].substr(0, 3)!='A+:') {
	    answer += lines[i].replace(/^\s+/,"")+'\n';
	  }
	  i--;
	  countAnswers++;
	  this.answers.push(answer);
	} 
      }
    }

  }

  questionToStr () {
      var str = this.difficulty+"::";
      if (this.topic!=='')
        str += this.topic+"::";
      if (this.variation!=='')
        str += this.variation+"::";
      str += "\n"+this.question;
   
      for(var i = 0;i < this.answers.length; i++){
        if (this.correctAnswer == i) {
	        str += "A+: " + this.answers[i]+"\n";
        } else {
	        str += "A-: " + this.answers[i]+"\n";
        }
      }
      return str;
  }


 questionToTex () {
     var str = '\\documentclass{article}\n\\begin{document}\n';
     
     str += "{\\bf Question:} "+this.question;

     str += "\\begin{enumerate}\n";
     
      for(var i = 0;i < this.answers.length; i++){
        if (this.correctAnswer == i) {
	        str += "\\item {\\bf " + this.answers[i]+"}\n";
        } else {
	        str += "\\item " + this.answers[i]+"\n";
        }
      }

      str += "\\end{enumerate}\n\n";
      str += '\\end{document}\n';
      return str;
 }
    
}
