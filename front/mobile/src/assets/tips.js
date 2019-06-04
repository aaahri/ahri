export default function msg(val, color) {
    let tips;
    if (document.getElementById("msg")) {
        tips = document.getElementById("msg");
    } else {
        tips = document.createElement("div");
        tips.setAttribute("id", "msg");
    }
    tips.style.width = "90%";
    tips.style.height = "50px";
    tips.style.position = "fixed";
    tips.style.zIndex = "99999";
    tips.style.top = "-60px";
    tips.style.left = "5%";
    // tips.style.transform = "translateX(-300px)";
    tips.style.background = "#191919";
    tips.style.borderRadius = "6px";
    tips.style.lineHeight = "50px";
    tips.style.textAlign = "center";
    tips.style.transition = "1s";
    document.body.appendChild(tips);
    tips.style.color = color;
    tips.innerText = val;
    let t = -60;
    let timer1 = window.setInterval(function () {
        if (t < 20) {
            tips.style.top = t + "px";
        } else {
            window.clearInterval(timer1);
        }
        t += 3;
    }, 1);
    let timer = window.setTimeout(function () {
        let h = 20;
        let timer2 = window.setInterval(function () {
            if (h >= -60) {
                tips.style.top = h + "px";
            } else {
                window.clearInterval(timer2);
            }
            h -= 3;
        }, 1);
        window.clearTimeout(timer);
    }, 5000);
}