import BaseAxisPointer, { AxisPointerElementOptions } from './BaseAxisPointer';
import { ScaleDataValue, VerticalAlign, CommonAxisPointerOption } from '../../util/types';
import ExtensionAPI from '../../core/ExtensionAPI';
import SingleAxisModel from '../../coord/single/AxisModel';
import Model from '../../model/Model';
declare type AxisPointerModel = Model<CommonAxisPointerOption>;
declare class SingleAxisPointer extends BaseAxisPointer {
    /**
     * @override
     */
    makeElOption(elOption: AxisPointerElementOptions, value: ScaleDataValue, axisModel: SingleAxisModel, axisPointerModel: AxisPointerModel, api: ExtensionAPI): void;
    /**
     * @override
     */
    getHandleTransform(value: ScaleDataValue, axisModel: SingleAxisModel, axisPointerModel: AxisPointerModel): {
        x: number;
        y: number;
        rotation: number;
    };
    /**
     * @override
     */
    updateHandleTransform(transform: {
        x: number;
        y: number;
        rotation: number;
    }, delta: number[], axisModel: SingleAxisModel, axisPointerModel: AxisPointerModel): {
        x: number;
        y: number;
        rotation: number;
        cursorPoint: number[];
        tooltipOption: {
            verticalAlign: VerticalAlign;
        };
    };
}
export default SingleAxisPointer;
