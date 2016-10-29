/// <reference path="../typings/jquery.d.ts" />

import { DashboardWebSocketConnectionListener, DashboardWebSocketApi, theWsApi } from '../wsApi';

/**
 * LoggerView
 */
class LoggerView {
    btnClear: JQuery;
    output: JQuery;

    constructor() {
        this.btnClear = $("#clearButton");
        this.output = $("#outputtext");

        this.btnClear.on("click", (e) => { this.clearText(); });
    }

    private clearText() {
        $("#outputtext").val("");
    }

    public writeToScreen(message: string) {
        this.output.val(this.output.val() + message);
        // $("#outputtext").scrollTop = $("#outputtext").scrollHeight;
    }
}

/**
 * LoggerController
 */
export class LoggerController implements DashboardWebSocketConnectionListener {

    private view: LoggerView;

    constructor() {
        this.view = new LoggerView();
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
