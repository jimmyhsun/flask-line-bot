function ShowAnswer()
    {document.getElementById("AnswerBox").innerHTML='3'}

// function add() {
//         var a = parseInt(document.getElementById('a').value);
//         var b = parseInt(document.getElementById('b').value);
//         document.getElementById('result').value =  a+b ;
//     }


function abc() {
        var c = parseInt(document.getElementById('c').value);
        var d = parseInt(document.getElementById('d').value);
        var e = parseInt(document.getElementById('e').value);
        var f = parseInt(document.getElementById('f').value);
        var g = parseInt(document.getElementById('g').value);
        var h = parseInt(document.getElementById('h').value);
        var i = parseInt(document.getElementById('i').value);
        var j = parseInt(document.getElementById('j').value);
        var k = parseInt(document.getElementById('k').value);
        var l = parseInt(document.getElementById('l').value);
        if (isNaN(l)){l=0}
        if (isNaN(k)){k=0}
        if (isNaN(j)){j=0}
        if (isNaN(i)){i=0}
        if (isNaN(h)){h=0}
        if (isNaN(g)){g=0}
        if (isNaN(f)){f=0}
        if (isNaN(e)){e=0}
        if (isNaN(c)){c=0}
        if (isNaN(d)){d=0}
        var total = c*30 + d*40 +e*40+f*40+g*30+h*30+i*30+j*30+k*30+l*30
        document.getElementById('result_one').innerHTML =  total ;
        document.getElementById('result_two').innerHTML =  c*300+d*300+e*300+f*400+g*300+h*300+i*300+j*300+k*300+l*300;
    }
