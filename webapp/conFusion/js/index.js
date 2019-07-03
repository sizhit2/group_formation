function addinputFields(){
    var number = document.getElementById("project").value;

    for (i=0;i<number;i++){

        var input = document.createElement("input");
        input.type = "text";
        container.appendChild(input);
        container.appendChild(document.createElement("br"));
    }
}