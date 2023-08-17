function compile(code,outputId) {
    var e = document.getElementById(outputId);
    e.contentDocument.open();
    e.contentDocument.write(code);
    e.contentDocument.close();
}
function changeSize(id,width,height){
    console.log("Changed");
    document.getElementById(id).style.width=width;
    document.getElementById(id).style.height=height;
}
function showObject(id,display){
    document.getElementById(id).style.display=display;
}
function hideObject(id){
    document.getElementById(id).style.display="none";
}
document.getElementById('file').addEventListener('keydown', function(e) {
  if (e.key == 'Tab') {
    e.preventDefault();
    var start = this.selectionStart;
    var end = this.selectionEnd;

    // set textarea value to: text before caret + tab + text after caret
    this.value = this.value.substring(0, start) +
      "\t" + this.value.substring(end);

    // put caret at right position again
    this.selectionStart =
      this.selectionEnd = start + 1;
  }
});