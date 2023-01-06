import ExtensionAPI from '../../core/ExtensionAPI';
import InsideZoomModel from './InsideZoomModel';
import { DataZoomGetRangeHandlers } from './InsideZoomView';
import { EChartsExtensionInstallRegisters } from '../../extension';
export declare function setViewInfoToCoordSysRecord(api: ExtensionAPI, dataZoomModel: InsideZoomModel, getRange: DataZoomGetRangeHandlers): void;
export declare function disposeCoordSysRecordIfNeeded(api: ExtensionAPI, dataZoomModel: InsideZoomModel): void;
export declare function installDataZoomRoamProcessor(registers: EChartsExtensionInstallRegisters): void;
