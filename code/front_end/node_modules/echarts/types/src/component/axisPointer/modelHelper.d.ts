import Model from '../../model/Model';
import GlobalModel from '../../model/Global';
import ExtensionAPI from '../../core/ExtensionAPI';
import { AxisPointerOption } from './AxisPointerModel';
import Axis from '../../coord/Axis';
import SeriesModel from '../../model/Series';
import { CommonAxisPointerOption, Dictionary } from '../../util/types';
import { AxisBaseModel } from '../../coord/AxisBaseModel';
import ComponentModel from '../../model/Component';
import { CoordinateSystemMaster } from '../../coord/CoordinateSystem';
interface LinkGroup {
    mapper: AxisPointerOption['link'][number]['mapper'];
    /**
     * { [axisKey]: AxisInfo }
     */
    axesInfo: Dictionary<AxisInfo>;
}
interface AxisInfo {
    axis: Axis;
    key: string;
    coordSys: CoordinateSystemMaster;
    axisPointerModel: Model<CommonAxisPointerOption>;
    triggerTooltip: boolean;
    involveSeries: boolean;
    snap: boolean;
    useHandle: boolean;
    seriesModels: SeriesModel[];
    linkGroup?: LinkGroup;
    seriesDataCount?: number;
}
interface CollectionResult {
    /**
     * { [coordSysKey]: { [axisKey]: AxisInfo } }
     */
    coordSysAxesInfo: Dictionary<Dictionary<AxisInfo>>;
    /**
     * { [axisKey]: AxisInfo }
     */
    axesInfo: Dictionary<AxisInfo>;
    /**
     * { [coordSysKey]: { CoordinateSystemMaster } }
     */
    coordSysMap: Dictionary<CoordinateSystemMaster>;
    seriesInvolved: boolean;
}
export declare function collect(ecModel: GlobalModel, api: ExtensionAPI): CollectionResult;
export declare function fixValue(axisModel: AxisBaseModel): void;
export declare function getAxisInfo(axisModel: AxisBaseModel): AxisInfo;
export declare function getAxisPointerModel(axisModel: AxisBaseModel): Model<CommonAxisPointerOption>;
/**
 * @param {module:echarts/model/Model} model
 * @return {string} unique key
 */
export declare function makeKey(model: ComponentModel): string;
export {};
