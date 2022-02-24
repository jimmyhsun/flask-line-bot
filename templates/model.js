function ShowAnswer()
    {document.getElementById("AnswerBox").innerHTML='3'}

function add() {
        var a = parseInt(document.getElementById('a').value);
        var b = parseInt(document.getElementById('b').value);
        document.getElementById('result').value =  a+b ;
    }


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
        var total = c*10 + d*10 +e*20+f*20+g*10+h*30+i*20+j*5+k*10+l*20
        document.getElementById('result_one').innerHTML =  total ;
        document.getElementById('result_two').innerHTML =  c*210+d*8+e*194+f*192+g*154+h*202+i*199+j*180+k*226+l*221;
    }
