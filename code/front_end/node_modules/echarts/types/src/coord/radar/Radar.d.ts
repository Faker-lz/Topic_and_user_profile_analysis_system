import IndicatorAxis from './IndicatorAxis';
import { CoordinateSystemMaster, CoordinateSystem } from '../CoordinateSystem';
import RadarModel from './RadarModel';
import GlobalModel from '../../model/Global';
import ExtensionAPI from '../../core/ExtensionAPI';
import { ScaleDataValue } from '../../util/types';
import { ParsedModelFinder } from '../../util/model';
declare class Radar implements CoordinateSystem, CoordinateSystemMaster {
    readonly type: 'radar';
    /**
     *
     * Radar dimensions
     */
    readonly dimensions: string[];
    cx: number;
    cy: number;
    r: number;
    r0: number;
    startAngle: number;
    private _model;
    private _indicatorAxes;
    constructor(radarModel: RadarModel, ecModel: GlobalModel, api: ExtensionAPI);
    getIndicatorAxes(): IndicatorAxis[];
    dataToPoint(value: ScaleDataValue, indicatorIndex: number): number[];
    coordToPoint(coord: number, indicatorIndex: number): number[];
    pointToData(pt: number[]): number[];
    resize(radarModel: RadarModel, api: ExtensionAPI): void;
    update(ecModel: GlobalModel, api: ExtensionAPI): void;
    convertToPixel(ecModel: GlobalModel, finder: ParsedModelFinder, value: ScaleDataValue[]): never;
    convertFromPixel(ecModel: GlobalModel, finder: ParsedModelFinder, pixel: number[]): never;
    containPoint(point: number[]): boolean;
    /**
     * Radar dimensions is based on the data
     */
    static dimensions: string[];
    static create(ecModel: GlobalModel, api: ExtensionAPI): Radar[];
}
export default Radar;
