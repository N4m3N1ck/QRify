function compile(id) {
    const code = document.getElementById(id).value;
    var e = document.getElementById("output");
    e.contentDocument.open();
    e.contentDocument.write(code);
    e.contentDocument.close();
}
function showObject(id){
    document.getElementById(id).style.display="inline-block";
}
function hideObject(id){
    document.getElementById(id).style.display="none";
}
function hideIfEmpty(id,idToHide){
    if(document.getElementById(id).value === ""){
        hideObject(idToHide);
    }else{
        showObject(idToHide);
    }
}