import { ConnectionController } from './components/connection.ts'
import { LoggerController } from './components/logger.ts'
import { TemperatureController } from './components/temperature.ts'

$(function () {
    new ConnectionController();
    new TemperatureController();
    new LoggerController();
});
