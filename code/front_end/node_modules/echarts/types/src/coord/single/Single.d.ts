/**
 * Single coordinates system.
 */
import SingleAxis from './SingleAxis';
import { CoordinateSystem, CoordinateSystemMaster } from '../CoordinateSystem';
import GlobalModel from '../../model/Global';
import ExtensionAPI from '../../core/ExtensionAPI';
import BoundingRect from 'zrender/lib/core/BoundingRect';
import SingleAxisModel from './AxisModel';
import { ParsedModelFinder } from '../../util/model';
import { ScaleDataValue } from '../../util/types';
export declare const singleDimensions: string[];
/**
 * Create a single coordinates system.
 */
declare class Single implements CoordinateSystem, CoordinateSystemMaster {
    readonly type = "single";
    readonly dimension = "single";
    /**
     * Add it just for draw tooltip.
     */
    readonly dimensions: string[];
    name: string;
    axisPointerEnabled: boolean;
    model: SingleAxisModel;
    private _axis;
    private _rect;
    constructor(axisModel: SingleAxisModel, ecModel: GlobalModel, api: ExtensionAPI);
    /**
     * Initialize single coordinate system.
     */
    _init(axisModel: SingleAxisModel, ecModel: GlobalModel, api: ExtensionAPI): void;
    /**
     * Update axis scale after data processed
     */
    update(ecModel: GlobalModel, api: ExtensionAPI): void;
    /**
     * Resize the single coordinate system.
     */
    resize(axisModel: SingleAxisModel, api: ExtensionAPI): void;
    getRect(): BoundingRect;
    private _adjustAxis;
    private _updateAxisTransform;
    /**
     * Get axis.
     */
    getAxis(): SingleAxis;
    /**
     * Get axis, add it just for draw tooltip.
     */
    getBaseAxis(): SingleAxis;
    getAxes(): SingleAxis[];
    getTooltipAxes(): {
        baseAxes: SingleAxis[];
        otherAxes: SingleAxis[];
    };
    /**
     * If contain point.
     */
    containPoint(point: number[]): boolean;
    pointToData(point: number[]): number[];
    /**
     * Convert the series data to concrete point.
     * Can be [val] | val
     */
    dataToPoint(val: ScaleDataValue | ScaleDataValue[]): number[];
    convertToPixel(ecModel: GlobalModel, finder: ParsedModelFinder, value: ScaleDataValue[]): number[];
    convertFromPixel(ecModel: GlobalModel, finder: ParsedModelFinder, pixel: number[]): number[];
}
export default Single;
