function compile(id) {
    const code = document.getElementById(id).value;
    console.log(code);
    document.getElementById("output").innerHTML = code;
}