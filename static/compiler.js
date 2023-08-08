function compile(id,outputId) {
    const code = document.getElementById(id).value;
    var e = document.getElementById(outputId);
    e.contentDocument.open();
    e.contentDocument.write(code);
    e.contentDocument.close();
}
function showObject(id,display){
    document.getElementById(id).style.display=display;
}
function hideObject(id){
    document.getElementById(id).style.display="none";
}