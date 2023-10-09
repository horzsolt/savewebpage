function listenForClicks() {
    
    document.addEventListener("click", (e) => {

        function _sendMessage(url) {
            browser.tabs.sendMessage(tabs[0].id, {
                command: "sendurl",
                content: url
            });            
        }

        if (e.target.tagName !== "BUTTON" || !e.target.closest("#popup-content")) {
            return;
        }

        browser.tabs.query({active: true, currentWindow: true})
            .then(tabs => {
                let currentTab = tabs[0];
                console.log(currentTab.url);
                //sendMessage(currentTab.url);
                browser.tabs.sendMessage(tabs[0].id, {
                    command: "sendurl",
                    content: currentTab.url
                });                
            })
            .catch(reportError);

    });
}

function reportExecuteScriptError(error) {
    console.error('Failed to execute script: ' + error.message);
    console.trace();
}
  
const inline = `
    (() => {

        console.log("starting....");

        if (window.hasRun) {
        return;
        }
        window.hasRun = true;
    
        function sendurl(url) {
            let xmlhttp = new XMLHttpRequest();
            xmlhttp.open("POST", "http://192.168.0.21");
            xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
            xmlhttp.send(JSON.stringify({"url_to_parse": url}));
        }    

        browser.runtime.onMessage.addListener((message) => {
        if (message.command === "sendurl") {
            sendurl(message.content);
        }
        });
    })();
`;
browser.tabs
    .executeScript({code: inline})
    .then(listenForClicks)
    .catch(reportExecuteScriptError);