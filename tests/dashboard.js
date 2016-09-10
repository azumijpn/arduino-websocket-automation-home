/// <reference path="jquery.d.ts" />
var c;
var ws;
/**
 * DashboadView
 */
var DashboadView = (function () {
    function DashboadView() {
        this.btnConnect = $("#connectButton");
        this.btnDisconnect = $("#disconnectButton");
        this.btnSend = $("#sendButton");
        this.btnClear = $("#clearButton");
        this.text = $("#inputtext");
        this.output = $("#outputtext");
        this.setStateDisconnected();
    }
    DashboadView.prototype.setStateConnected = function () {
        this.btnConnect.prop("disabled", true);
        this.btnDisconnect.prop("disabled", false);
    };
    DashboadView.prototype.setStateDisconnected = function () {
        this.btnConnect.prop("disabled", false);
        this.btnDisconnect.prop("disabled", true);
    };
    DashboadView.prototype.clearText = function () {
        $("#outputtext").val("");
    };
    DashboadView.prototype.getText = function () {
        return this.text.val();
    };
    DashboadView.prototype.writeToScreen = function (message) {
        this.output.val(this.output.val() + message);
        // $("#outputtext").scrollTop = $("#outputtext").scrollHeight;
    };
    return DashboadView;
}());
/**
 * DashboadController
 */
var DashboadController = (function () {
    function DashboadController() {
        var _this = this;
        this.view = new DashboadView();
        this.view.btnConnect.on("click", function (e) { _this.connect(); });
        this.view.btnDisconnect.on("click", function (e) { _this.disconnect(); });
        this.view.btnClear.on("click", function (e) { _this.view.clearText(); });
        this.view.btnSend.on("click", function (e) { _this.sendText(); });
    }
    DashboadController.prototype.connect = function () {
        init_ws("ws://localhost:8000/");
    };
    DashboadController.prototype.disconnect = function () {
        ws.close();
    };
    DashboadController.prototype.sendText = function () {
        this.view.writeToScreen("sending...\n");
        //this.view.writeToScreen("sending" + this.view.getText() + "\n");
        ws.send(this.view.getText());
    };
    DashboadController.prototype.onWsOpen = function (evt) {
        this.view.writeToScreen("connected\n");
        this.view.setStateConnected();
    };
    DashboadController.prototype.onWsClose = function (evt) {
        this.view.writeToScreen("disconnected\n");
        this.view.setStateDisconnected();
    };
    DashboadController.prototype.onWsMessage = function (evt) {
        this.view.writeToScreen("response: " + evt.data + '\n');
    };
    DashboadController.prototype.onWsError = function (evt) {
        this.view.writeToScreen('error: ' + evt.returnValue + '\n');
        ws.close();
        this.view.setStateDisconnected();
    };
    return DashboadController;
}());
function init_ws(url) {
    ws = new WebSocket("ws://localhost:8000/");
    ws.onopen = function (evt) {
        c.onWsOpen(evt);
    };
    ws.onclose = function (evt) {
        c.onWsClose(evt);
    };
    ws.onmessage = function (evt) {
        c.onWsMessage(evt);
    };
    ws.onerror = function (evt) {
        c.onWsError(evt);
    };
}
$(function () {
    c = new DashboadController();
});
