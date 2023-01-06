import SeriesModel from '../../model/Series';
import { SeriesOption, SeriesOnCartesianOptionMixin, SeriesOnGeoOptionMixin, ItemStyleOption, SeriesLabelOption, OptionDataValue, StatesOptionMixin, SeriesEncodeOptionMixin, SeriesOnCalendarOptionMixin, DefaultStatesMixinEmpasis, CallbackDataParams } from '../../util/types';
import GlobalModel from '../../model/Global';
import SeriesData from '../../data/SeriesData';
import type Geo from '../../coord/geo/Geo';
import type Cartesian2D from '../../coord/cartesian/Cartesian2D';
import type Calendar from '../../coord/calendar/Calendar';
declare type HeatmapDataValue = OptionDataValue[];
export interface HeatmapStateOption<TCbParams = never> {
    itemStyle?: ItemStyleOption<TCbParams>;
    label?: SeriesLabelOption;
}
interface FunnelStatesMixin {
    emphasis?: DefaultStatesMixinEmpasis;
}
export interface HeatmapDataItemOption extends HeatmapStateOption, StatesOptionMixin<HeatmapStateOption, FunnelStatesMixin> {
    value: HeatmapDataValue;
}
export interface HeatmapSeriesOption extends SeriesOption<HeatmapStateOption<CallbackDataParams>, FunnelStatesMixin>, HeatmapStateOption<CallbackDataParams>, SeriesOnCartesianOptionMixin, SeriesOnGeoOptionMixin, SeriesOnCalendarOptionMixin, SeriesEncodeOptionMixin {
    type?: 'heatmap';
    coordinateSystem?: 'cartesian2d' | 'geo' | 'calendar';
    blurSize?: number;
    pointSize?: number;
    maxOpacity?: number;
    minOpacity?: number;
    data?: (HeatmapDataItemOption | HeatmapDataValue)[];
}
declare class HeatmapSeriesModel extends SeriesModel<HeatmapSeriesOption> {
    static readonly type = "series.heatmap";
    readonly type = "series.heatmap";
    static readonly dependencies: string[];
    coordinateSystem: Cartesian2D | Geo | Calendar;
    getInitialData(option: HeatmapSeriesOption, ecModel: GlobalModel): SeriesData;
    preventIncremental(): boolean;
    static defaultOption: HeatmapSeriesOption;
}
export default HeatmapSeriesModel;
