/// <reference path="../typings/webcomponents.d.ts" />

import { DashboardWebSocketConnectionListener, DashboardWebSocketApi, theWsApi } from '../wsApi';

export class DashboardLoggerElement extends HTMLCanvasElement {

    private textarea: HTMLTextAreaElement;

    constructor() {
        super();
    }

    createdCallback(): void {
        console.log("DashboardLoggerElement.createdCallback()");
        this.textarea = document.createElement("textarea");
        let btnClear = document.createElement("input");
        btnClear.type = "button";
        btnClear.value = "clear";
        this.appendChild(this.textarea);
        this.appendChild(btnClear);

        btnClear.addEventListener("click", (e) => {
            this.clearText();
        });

        new LoggerController(this);
    }

    clearText() {
        this.textarea.innerHTML = "";
    }

    public writeToScreen(message: string) {
        let now = new Date();
        this.textarea.innerHTML = this.textarea.innerHTML + now.toLocaleTimeString() + " : " + message;
        this.textarea.scrollTop = this.textarea.scrollHeight;
    }
}

/**
 * LoggerController
 */
class LoggerController implements DashboardWebSocketConnectionListener {

    private view: DashboardLoggerElement;

    constructor(view : DashboardLoggerElement) {
        this.view = view;
        theWsApi.addConnectionListener(this);
    }

    public onWsOpen(evt: Event) {
        this.view.writeToScreen("connected\n");
    }

    public onWsClose(evt: CloseEvent) {
        this.view.writeToScreen("disconnected\n");
    }

    public onWsMessage(evt: MessageEvent) {
        this.view.writeToScreen("response: " + evt.data + '\n');
    }

    public onWsError(evt: Event) {
        this.view.writeToScreen('error: ' + evt.returnValue + '\n');
    }
}


export function registerDashboardLoggerElement() {
    document.registerElement('dashboard-logger', DashboardLoggerElement);
}
