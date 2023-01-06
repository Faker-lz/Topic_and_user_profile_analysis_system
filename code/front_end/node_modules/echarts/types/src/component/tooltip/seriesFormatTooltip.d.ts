import SeriesModel from '../../model/Series';
import { TooltipMarkupSection } from './tooltipMarkup';
export declare function defaultSeriesFormatTooltip(opt: {
    series: SeriesModel;
    dataIndex: number;
    multipleSeries: boolean;
}): TooltipMarkupSection;
