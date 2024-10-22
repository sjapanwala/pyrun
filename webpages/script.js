document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({ behavior: 'smooth' });
    });
});

function copyToClipboard() {
    const codeText = document.getElementById("install-code").innerText;
    const tempTextArea = document.createElement("textarea");
    tempTextArea.value = codeText;
    document.body.appendChild(tempTextArea);
    tempTextArea.select();
    document.execCommand("copy");
    document.body.removeChild(tempTextArea);
    const copyButton = document.querySelector(".copy-btn");
    copyButton.innerText = "✅";
    setTimeout(() => {
        copyButton.innerText = "Copy";
    }, 2000);
}
