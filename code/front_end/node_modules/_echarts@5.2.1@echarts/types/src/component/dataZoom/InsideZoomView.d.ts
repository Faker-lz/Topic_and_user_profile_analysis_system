import DataZoomView from './DataZoomView';
import InsideZoomModel from './InsideZoomModel';
import GlobalModel from '../../model/Global';
import ExtensionAPI from '../../core/ExtensionAPI';
import RoamController, { RoamEventParams } from '../helper/RoamController';
import { DataZoomCoordSysMainType, DataZoomReferCoordSysInfo } from './helper';
declare class InsideZoomView extends DataZoomView {
    static type: string;
    type: string;
    /**
     * 'throttle' is used in this.dispatchAction, so we save range
     * to avoid missing some 'pan' info.
     */
    range: number[];
    render(dataZoomModel: InsideZoomModel, ecModel: GlobalModel, api: ExtensionAPI): void;
    dispose(): void;
    private _clear;
}
interface DataZoomGetRangeHandler<T extends RoamEventParams['zoom'] | RoamEventParams['scrollMove'] | RoamEventParams['pan']> {
    (coordSysInfo: DataZoomReferCoordSysInfo, coordSysMainType: DataZoomCoordSysMainType, controller: RoamController, e: T): [number, number];
}
declare const getRangeHandlers: {
    pan: DataZoomGetRangeHandler<RoamEventParams['pan']>;
    zoom: DataZoomGetRangeHandler<RoamEventParams['zoom']>;
    scrollMove: DataZoomGetRangeHandler<RoamEventParams['scrollMove']>;
} & ThisType<InsideZoomView>;
export declare type DataZoomGetRangeHandlers = typeof getRangeHandlers;
export default InsideZoomView;
