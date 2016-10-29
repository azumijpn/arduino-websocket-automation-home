/// <reference path="../typings/jquery.d.ts" />

import { DashboardWebSocketConnectionListener, DashboardWebSocketApi, theWsApi } from '../wsApi';

interface ConnectionViewListener
{
    connect() : void;
    disconnect() : void;
}

/**
 * ConnectionView
 */
class ConnectionView {;
    listener: ConnectionViewListener
    btnConnect: JQuery;
    btnDisconnect: JQuery;

    constructor(listener: ConnectionViewListener) {
        this.listener = listener;
        this.btnConnect = $("#connectButton");
        this.btnDisconnect = $("#disconnectButton");

        this.btnConnect.on("click", (e) => { this.listener.connect(); });
        this.btnDisconnect.on("click", (e) => { this.listener.disconnect(); });

        this.setStateDisconnected();
    }

    public setStateConnected() {
        this.btnConnect.prop("disabled", true);
        this.btnDisconnect.prop("disabled", false);
    }

    public setStateDisconnected() {
        this.btnConnect.prop("disabled", false);
        this.btnDisconnect.prop("disabled", true);
    }
}

/**
 * ConnectionController
 */
export class ConnectionController implements DashboardWebSocketConnectionListener, ConnectionViewListener {

    private view: ConnectionView;

    constructor() {
        this.view = new ConnectionView(this);
        theWsApi.addConnectionListener(this);
    }

    public connect() {
        theWsApi.connect("ws://localhost:8000/");
    }

    public disconnect() {
        theWsApi.close();
    }

    public onWsOpen(evt: Event) {
        this.view.setStateConnected();
    }

    public onWsClose(evt: CloseEvent) {
        this.view.setStateDisconnected();
    }

    public onWsMessage(evt: MessageEvent) {
    }

    public onWsError(evt: Event) {
        this.view.setStateDisconnected();
    }
}