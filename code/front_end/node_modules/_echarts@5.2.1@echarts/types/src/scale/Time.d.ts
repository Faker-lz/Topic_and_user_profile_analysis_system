import { TimeUnit } from '../util/time';
import IntervalScale from './Interval';
import { TimeScaleTick } from '../util/types';
import { TimeAxisLabelFormatterOption } from '../coord/axisCommonTypes';
import { LocaleOption } from '../core/locale';
import Model from '../model/Model';
declare type TimeScaleSetting = {
    locale: Model<LocaleOption>;
    useUTC: boolean;
};
declare class TimeScale extends IntervalScale<TimeScaleSetting> {
    static type: string;
    readonly type = "time";
    _approxInterval: number;
    _minLevelUnit: TimeUnit;
    constructor(settings?: TimeScaleSetting);
    /**
     * Get label is mainly for other components like dataZoom, tooltip.
     */
    getLabel(tick: TimeScaleTick): string;
    getFormattedLabel(tick: TimeScaleTick, idx: number, labelFormatter: TimeAxisLabelFormatterOption): string;
    /**
     * @override
     * @param expandToNicedExtent Whether expand the ticks to niced extent.
     */
    getTicks(expandToNicedExtent?: boolean): TimeScaleTick[];
    niceExtent(opt?: {
        splitNumber?: number;
        fixMin?: boolean;
        fixMax?: boolean;
        minInterval?: number;
        maxInterval?: number;
    }): void;
    niceTicks(approxTickNum: number, minInterval: number, maxInterval: number): void;
    parse(val: number | string | Date): number;
    contain(val: number): boolean;
    normalize(val: number): number;
    scale(val: number): number;
}
export default TimeScale;
