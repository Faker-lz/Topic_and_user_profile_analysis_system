import SeriesModel from '../../model/Series';
import { SeriesOption, SeriesOnPolarOptionMixin, SeriesOnCartesianOptionMixin, SeriesOnCalendarOptionMixin, SeriesOnGeoOptionMixin, SeriesOnSingleOptionMixin, SymbolOptionMixin, OptionDataValue, ItemStyleOption, SeriesLabelOption, StatesOptionMixin, SeriesEncodeOptionMixin, CallbackDataParams, DefaultEmphasisFocus } from '../../util/types';
import GlobalModel from '../../model/Global';
import SeriesData from '../../data/SeriesData';
import type { SymbolDrawItemModelOption } from '../helper/SymbolDraw';
import { BrushCommonSelectorsForSeries } from '../../component/brush/selector';
declare type ScatterDataValue = OptionDataValue | OptionDataValue[];
interface EffectScatterStatesOptionMixin {
    emphasis?: {
        focus?: DefaultEmphasisFocus;
        scale?: boolean;
    };
}
export interface EffectScatterStateOption<TCbParams = never> {
    itemStyle?: ItemStyleOption<TCbParams>;
    label?: SeriesLabelOption;
}
export interface EffectScatterDataItemOption extends SymbolOptionMixin, EffectScatterStateOption, StatesOptionMixin<EffectScatterStateOption, EffectScatterStatesOptionMixin> {
    name?: string;
    value?: ScatterDataValue;
    rippleEffect?: SymbolDrawItemModelOption['rippleEffect'];
}
export interface EffectScatterSeriesOption extends SeriesOption<EffectScatterStateOption<CallbackDataParams>, EffectScatterStatesOptionMixin>, EffectScatterStateOption<CallbackDataParams>, SeriesOnCartesianOptionMixin, SeriesOnPolarOptionMixin, SeriesOnCalendarOptionMixin, SeriesOnGeoOptionMixin, SeriesOnSingleOptionMixin, SymbolOptionMixin<CallbackDataParams>, SeriesEncodeOptionMixin {
    type?: 'effectScatter';
    coordinateSystem?: string;
    effectType?: 'ripple';
    /**
     * When to show the effect
     */
    showEffectOn?: 'render' | 'emphasis';
    clip?: boolean;
    /**
     * Ripple effect config
     */
    rippleEffect?: SymbolDrawItemModelOption['rippleEffect'];
    data?: (EffectScatterDataItemOption | ScatterDataValue)[];
}
declare class EffectScatterSeriesModel extends SeriesModel<EffectScatterSeriesOption> {
    static readonly type = "series.effectScatter";
    type: string;
    static readonly dependencies: string[];
    hasSymbolVisual: boolean;
    getInitialData(option: EffectScatterSeriesOption, ecModel: GlobalModel): SeriesData;
    brushSelector(dataIndex: number, data: SeriesData, selectors: BrushCommonSelectorsForSeries): boolean;
    static defaultOption: EffectScatterSeriesOption;
}
export default EffectScatterSeriesModel;
