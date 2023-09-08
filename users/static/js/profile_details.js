import {MESSAGE_TYPE, sendToastMessage} from "../../../static/js/toastinette.js";

if (document.getElementById('message')) {
    const message = document.getElementById('message').textContent.toLowerCase();
    sendToastMessage(message,MESSAGE_TYPE.SUCCESS);
}