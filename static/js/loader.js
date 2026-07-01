const headlines = [
    "Loading breaking news...",
    "Fetching latest headlines...",
    "Updating world news feed...",
    "Loading top stories...",
    "Preparing today's updates..."
];

const headlineElement = document.getElementById("loaderHeadline");

let current = 0;

function rotateHeadline(){
    headlineElement.textContent = headlines[current];
    current++;

    if(current >= headlines.length){
        current = 0;
    }
}

rotateHeadline();
setInterval(rotateHeadline,1500);

window.addEventListener("load", () => {
    setTimeout(() => {
        document.getElementById("newsLoader").classList.add("hide");
    },2000);
});