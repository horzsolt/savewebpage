"use strict";

function listenForClicks() {

    var input = document.getElementById("sendurl_tags");

    input.addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            event.preventDefault();
            document.getElementById("send_btn").click();
        }
    });

    document.addEventListener("click", (e) => {

        function sendMessageToTabs(tabs) {
            
            let _tags = document.getElementById("sendurl_tags").value;
            let _url= document.getElementById("targeturl").value;
            browser.tabs
                .sendMessage(tabs[0].id, {
                    command: "sendurl",
                    content: tabs[0].url,
                    tags: _tags,
                    url: _url,
                 })
                .then((response) => {
                    browser.notifications.create("cakeNotification", {
                        type: "basic",
                        iconUrl: browser.runtime.getURL("icons/cake-96.png"),
                        title: response.response,
                        message: response.response,
                    });
                })
                .catch(reportExecuteScriptError);
        }

        if (e.target.tagName !== "BUTTON" || !e.target.closest("#popup-content")) {
            return;
        }

        browser.tabs
            .query({currentWindow: true, active: true})
            .then(sendMessageToTabs)
            .catch(reportExecuteScriptError);

    });
}

function reportExecuteScriptError(error) {
    console.log(error);
    console.error('Failed to execute script: ' + error.message);
}
  
const inline = `
    (() => {

        if (window.hasRun) {
            return;
        }
        window.hasRun = true;

        function doPost(body, url) {
            var xhr = new XMLHttpRequest;
            var response = "error";

            xhr.open("POST", url, false);
            xhr.setRequestHeader('Content-type', 'application/json; charset=utf-8');

            xhr.send(body);
            return xhr.responseText;
        };

        browser.runtime.onMessage.addListener((message) => {
            let result = "";
            if (message.command === "sendurl") {
                
                let response = "";
                let json = JSON.stringify({"url_to_parse": encodeURIComponent(message.content), "tags": message.tags});
                let url = message.url;
    
                result = doPost(json, url);
                return Promise.resolve({ response: result });
            }
        });
    })();
`;

browser.tabs
    .executeScript({code: inline})
    .then(listenForClicks)
    .catch(reportExecuteScriptError);
