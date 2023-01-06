import SeriesModel from '../../model/Series';
import SeriesData from '../../data/SeriesData';
import { MarkerStatisticType, MarkerPositionOption } from './MarkerModel';
import Axis from '../../coord/Axis';
import { CoordinateSystem } from '../../coord/CoordinateSystem';
import { ScaleDataValue, ParsedValue, DimensionName } from '../../util/types';
import SeriesDimensionDefine from '../../data/SeriesDimensionDefine';
interface MarkerAxisInfo {
    valueDataDim: DimensionName;
    valueAxis: Axis;
    baseAxis: Axis;
    baseDataDim: DimensionName;
}
export declare type MarkerDimValueGetter<TMarkerItemOption> = (item: TMarkerItemOption, dimName: string, dataIndex: number, dimIndex: number) => ParsedValue;
/**
 * Transform markPoint data item to format used in List by do the following
 * 1. Calculate statistic like `max`, `min`, `average`
 * 2. Convert `item.xAxis`, `item.yAxis` to `item.coord` array
 */
export declare function dataTransform(seriesModel: SeriesModel, item: MarkerPositionOption): MarkerPositionOption;
export declare function getAxisInfo(item: MarkerPositionOption, data: SeriesData, coordSys: CoordinateSystem, seriesModel: SeriesModel): MarkerAxisInfo;
/**
 * Filter data which is out of coordinateSystem range
 * [dataFilter description]
 */
export declare function dataFilter(coordSys: CoordinateSystem & {
    containData?(data: ScaleDataValue[]): boolean;
}, item: MarkerPositionOption): boolean;
export declare function createMarkerDimValueGetter(inCoordSys: boolean, dims: SeriesDimensionDefine[]): MarkerDimValueGetter<MarkerPositionOption>;
export declare function numCalculate(data: SeriesData, valueDataDim: string, type: MarkerStatisticType): number;
export {};
