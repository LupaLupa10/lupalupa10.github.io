// create element for copy button in code blocks
const excludedLanguages = [
  "language-chartjs",
  "language-diff2html",
  "language-echarts",
  "language-geojson",
  "language-mermaid",
  "language-plotly",
  "language-vega_lite",
];

const codeBlocks = document.querySelectorAll("pre");

const renderCopyButtonContent = (button, iconClass, label) => {
  button.innerHTML = `<i class="${iconClass}"></i><span>${label}</span>`;
};

const getCodeElement = (codeBlock) => codeBlock.querySelector("pre:not(.lineno)") || codeBlock.querySelector("code");

const isCopyableCodeBlock = (codeBlock) => {
  const codeElement = codeBlock.querySelector("code");
  if (!codeElement) {
    return false;
  }

  return !excludedLanguages.some((languageClass) => codeElement.classList.contains(languageClass));
};

codeBlocks.forEach(function (codeBlock) {
  const codeElement = getCodeElement(codeBlock);
  if (!codeElement || !isCopyableCodeBlock(codeBlock)) {
    return;
  }

  // create copy button
  const copyButton = document.createElement("button");
  copyButton.className = "copy";
  copyButton.type = "button";
  copyButton.setAttribute("aria-label", "Copy code to clipboard");
  renderCopyButtonContent(copyButton, "fa-solid fa-clipboard", "Copy");

  // get code from code block and copy to clipboard
  copyButton.addEventListener("click", async function () {
    if (!window.navigator.clipboard) {
      return;
    }

    const code = codeElement.innerText.trim();
    await window.navigator.clipboard.writeText(code);
    renderCopyButtonContent(copyButton, "fa-solid fa-clipboard-check", "Copied");

    setTimeout(function () {
      renderCopyButtonContent(copyButton, "fa-solid fa-clipboard", "Copy");
    }, 3000);
  });

  // create wrapper div
  const wrapper = document.createElement("div");
  wrapper.className = "code-display-wrapper";

  // add copy button and code block to wrapper div
  const parent = codeBlock.parentElement;
  parent.insertBefore(wrapper, codeBlock);
  wrapper.append(codeBlock);
  wrapper.append(copyButton);
});
