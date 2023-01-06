import ComponentModel from '../../model/Component';
import Calendar from './Calendar';
import { ComponentOption, BoxLayoutOptionMixin, LayoutOrient, LineStyleOption, ItemStyleOption, LabelOption, OptionDataValueDate } from '../../util/types';
import GlobalModel from '../../model/Global';
import Model from '../../model/Model';
export interface CalendarMonthLabelFormatterCallbackParams {
    nameMap: string;
    yyyy: string;
    yy: string;
    /**
     * Month string. With 0 prefix.
     */
    MM: string;
    /**
     * Month number
     */
    M: number;
}
export interface CalendarYearLabelFormatterCallbackParams {
    nameMap: string;
    /**
     * Start year
     */
    start: string;
    /**
     * End year
     */
    end: string;
}
export interface CalendarOption extends ComponentOption, BoxLayoutOptionMixin {
    mainType?: 'calendar';
    cellSize?: number | 'auto' | (number | 'auto')[];
    orient?: LayoutOrient;
    splitLine?: {
        show?: boolean;
        lineStyle?: LineStyleOption;
    };
    itemStyle?: ItemStyleOption;
    /**
     * // one year
     * range: 2017
     * // one month
     * range: '2017-02'
     * //  a range
     * range: ['2017-01-02', '2017-02-23']
     * // note: they will be identified as ['2017-01-01', '2017-02-01']
     * range: ['2017-01', '2017-02']
     */
    range?: OptionDataValueDate | (OptionDataValueDate)[];
    dayLabel?: Omit<LabelOption, 'position'> & {
        /**
         * First day of week.
         */
        firstDay?: number;
        /**
         * Margin between day label and axis line.
         * Can be percent string of cell size.
         */
        margin?: number | string;
        /**
         * Position of week, at the beginning or end of the range.
         */
        position?: 'start' | 'end';
        /**
         * Week text content, defaults to 'en'; It supports Chinese, English, and custom; index 0 always means Sunday
         * en: shortcut to English  ['S', 'M', 'T', 'W', 'T', 'F', 'S']
         * cn: shortcut to Chinese ['日', '一', '二', '三', '四', '五', '六']
         */
        nameMap?: 'en' | 'cn' | string[];
    };
    monthLabel?: Omit<LabelOption, 'position'> & {
        /**
         * Margin between month label and axis line.
         */
        margin?: number;
        /**
         * Position of month label, at the beginning or end of the range.
         */
        position?: 'start' | 'end';
        /**
         * Month text content, defaults to 'en'; It supports Chinese, English, and custom; Index 0 always means Jan;
         */
        nameMap?: 'en' | 'cn' | string[];
        formatter?: string | ((params: CalendarMonthLabelFormatterCallbackParams) => string);
    };
    yearLabel?: Omit<LabelOption, 'position'> & {
        /**
         * Margin between year label and axis line.
         */
        margin?: number;
        /**
         * Position of year label, at the beginning or end of the range.
         */
        position?: 'top' | 'bottom' | 'left' | 'right';
        formatter?: string | ((params: CalendarYearLabelFormatterCallbackParams) => string);
    };
}
declare class CalendarModel extends ComponentModel<CalendarOption> {
    static type: string;
    type: string;
    coordinateSystem: Calendar;
    /**
     * @override
     */
    init(option: CalendarOption, parentModel: Model, ecModel: GlobalModel): void;
    /**
     * @override
     */
    mergeOption(option: CalendarOption): void;
    getCellSize(): (number | "auto")[];
    static defaultOption: CalendarOption;
}
export default CalendarModel;
