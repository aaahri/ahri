export default function loading(dom) {
    let tips = document.createElement("div");
    tips.setAttribute("id", "a_loading");
    tips.style.background = "#333c";
    tips.style.position = "absolute";
    tips.style.zIndex = "99999";
    tips.style.top = "0";
    tips.style.left = "0";
    tips.style.right = "0";
    tips.style.bottom = "0";
    tips.style.margin = "8px";
    tips.style.borderRadius = "4px";
    tips.style.display = "flex";
    tips.style.justifyContent = "center";
    tips.style.alignItems = "center";
    let span = document.createElement("span");
    span.setAttribute("class", "a_load iconfont ahriloading");
    span.style.color = "#fff";
    span.style.fontSize = "30px";
    tips.appendChild(span);
    dom.appendChild(tips);
    return tips;
}