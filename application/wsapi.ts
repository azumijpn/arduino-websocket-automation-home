export interface DashboardWebSocketConnectionListener {
    onWsOpen(evt: Event): void;
    onWsClose(evt: CloseEvent): void;
    onWsError(evt: Event): void;
    onWsMessage(evt: MessageEvent): void;
}

export interface DashboardWebSocketTemperatureListener {
    onTemperature(temperature: number, time: number): void;
}

/**
 * DashboardWebSocketApi
 */
export class DashboardWebSocketApi {
    private ws: WebSocket = null;
    private connectionListeners: Array<DashboardWebSocketConnectionListener> = [];
    private temperatureListeners: Array<DashboardWebSocketTemperatureListener> = [];

    constructor() {
    }

    public connect(url: string) {
        this.ws = new WebSocket(url);
        this.ws.onopen = (evt: Event) => { this.onWsOpen(evt); };
        this.ws.onclose = (evt: CloseEvent) => { this.onWsClose(evt); };
        this.ws.onmessage = (evt: MessageEvent) => { this.onWsMessage(evt); };
        this.ws.onerror = (evt: Event) => { this.onWsError(evt); };
    }

    public close() {
        this.ws.close();
    }

    public addConnectionListener(listener: DashboardWebSocketConnectionListener) {
        this.connectionListeners.push(listener);
    }

    public addTemperatureListener(listener: DashboardWebSocketTemperatureListener) {
        this.temperatureListeners.push(listener);
    }

    public setTemperature(t: number) {
        let obj = { 'msg': 'setTemperature', 'temperature': t };
        let frame: string = JSON.stringify(obj);
        this.send(frame);
    }

    private sendTemperature(temperature: number, time: number) {
        this.temperatureListeners.forEach((l) => {
            l.onTemperature(temperature, time);
        });
    }

    private onWsOpen(evt: Event) {
        this.connectionListeners.forEach((l) => {
            l.onWsOpen(evt);
        });
    }

    private onWsClose(evt: CloseEvent) {
        this.ws = null;
        this.connectionListeners.forEach((l) => {
            l.onWsClose(evt);
        });
    }

    private onWsError(evt: Event) {
        this.connectionListeners.forEach((l) => {
            l.onWsError(evt);
        });
        this.close()
    }

    private onWsMessage(evt: MessageEvent) {
        this.connectionListeners.forEach((l) => {
            l.onWsMessage(evt);
        });
        let obj: any = JSON.parse(evt.data);
        switch (obj.msg) {
            case "temperature":
                this.onTemperature(obj);
                break;

            default:
                console.error("Unknonw message : " + obj.msg);
                break;
        }
    }

    private onTemperature(obj: any) {
        let temperature: number = Number(obj.temperature);
        let time: number = Number(obj.time);
        if (!isNaN(temperature) && !isNaN(time)) {
            this.sendTemperature(temperature, time);
        }
    }

    private send(data: string) {
        this.ws.send(data);
    }
}

export let theWsApi: DashboardWebSocketApi = new DashboardWebSocketApi();
