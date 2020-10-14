window.addEventListener("load", () => {
    const canvas = document.querySelector("#canvas");
    const ctx = canvas.getContext("2d");

    const height = 500;
    const width = 500;
    canvas.height = height;
    canvas.width = width;

    let painting = false;

    function startPos(){
        painting = true;
    }

    function donePos(){
        painting = false;
        ctx.beginPath();
    }

    function paint(e){
        if(!painting){
            return;
        }
        ctx.lineWidth = 25;
        ctx.lineCap = "round";
        ctx.lineTo(e.clientX - 10, e.clientY - 70);
        ctx.stroke();
        ctx.beginPath();
        ctx.moveTo(e.clientX - 10, e.clientY - 70);
    }

    canvas.addEventListener("mousedown", startPos);
    canvas.addEventListener("mouseup", donePos);
    canvas.addEventListener("mousemove", paint);
});

function sendImage() {
    const canvas = document.querySelector("#canvas");
    const dataURL = canvas.toDataURL();
    var checkBoxValue = document.getElementById("alphabet").checked;
    var alpha1number0 = "0";
    if(checkBoxValue == true) {
        alpha1number0 = "1";
    }
    $.ajax({
        url: "/",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify(alpha1number0 + dataURL),
        success: function(response){
            addText(response);
        }
    })
}

function addText(txt) {
    var textBox = document.getElementById("txtbx");
    textBox.value = textBox.value + txt;
}

function clearCanvas(){
    const canvas = document.querySelector("#canvas");
    const ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height)
}