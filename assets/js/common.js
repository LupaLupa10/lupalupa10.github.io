$(document).ready(function () {
  const publicationSections = ["abstract", "award", "bibtex"];

  // add toggle functionality to abstract, award and bibtex buttons
  publicationSections.forEach((sectionName) => {
    $(`a.${sectionName}`).click(function () {
      const container = $(this).parent().parent();

      publicationSections.forEach((otherSectionName) => {
        const selector = otherSectionName === sectionName ? `.${otherSectionName}.hidden` : `.${otherSectionName}.hidden.open`;
        container.find(selector).toggleClass("open");
      });
    });
  });
  $("a").removeClass("waves-effect waves-light");

  // bootstrap-toc
  if ($("#toc-sidebar").length) {
    // remove related publications years from the TOC
    $(".publications h2").each(function () {
      $(this).attr("data-toc-skip", "");
    });
    var navSelector = "#toc-sidebar";
    var $myNav = $(navSelector);
    Toc.init($myNav);
    $("body").scrollspy({
      target: navSelector,
    });
  }

  // add css to jupyter notebooks
  const jupyterTheme = determineComputedTheme();

  $(".jupyter-notebook-iframe-container iframe").each(function () {
    const iframeHead = $(this).contents().find("head");
    const cssLink = document.createElement("link");
    cssLink.href = "../css/jupyter.css";
    cssLink.rel = "stylesheet";
    cssLink.type = "text/css";
    iframeHead.append(cssLink);

    if (jupyterTheme === "dark") {
      $(this).bind("load", function () {
        $(this).contents().find("body").attr({
          "data-jp-theme-light": "false",
          "data-jp-theme-name": "JupyterLab Dark",
        });
      });
    }
  });

  // trigger popovers
  $('[data-toggle="popover"]').popover({
    trigger: "hover",
  });
});
