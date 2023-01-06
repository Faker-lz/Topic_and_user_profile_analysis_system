import * as graphic from '../../util/graphic';
import CalendarModel from '../../coord/calendar/CalendarModel';
import { CalendarParsedDateRangeInfo } from '../../coord/calendar/Calendar';
import GlobalModel from '../../model/Global';
import ExtensionAPI from '../../core/ExtensionAPI';
import { LayoutOrient, OptionDataValueDate } from '../../util/types';
import ComponentView from '../../view/Component';
import { PathStyleProps } from 'zrender/lib/graphic/Path';
import { TextStyleProps, TextProps } from 'zrender/lib/graphic/Text';
declare class CalendarView extends ComponentView {
    static type: string;
    type: string;
    /**
     * top/left line points
     */
    private _tlpoints;
    /**
     * bottom/right line points
     */
    private _blpoints;
    /**
     * first day of month
     */
    private _firstDayOfMonth;
    /**
     * first day point of month
     */
    private _firstDayPoints;
    render(calendarModel: CalendarModel, ecModel: GlobalModel, api: ExtensionAPI): void;
    _renderDayRect(calendarModel: CalendarModel, rangeData: CalendarParsedDateRangeInfo, group: graphic.Group): void;
    _renderLines(calendarModel: CalendarModel, rangeData: CalendarParsedDateRangeInfo, orient: LayoutOrient, group: graphic.Group): void;
    _getEdgesPoints(points: number[][], lineWidth: number, orient: LayoutOrient): number[][];
    _drawSplitline(points: number[][], lineStyle: PathStyleProps, group: graphic.Group): void;
    _getLinePointsOfOneWeek(calendarModel: CalendarModel, date: OptionDataValueDate, orient: LayoutOrient): number[][];
    _formatterLabel<T extends {
        nameMap: string;
    }>(formatter: string | ((params: T) => string), params: T): string;
    _yearTextPositionControl(textEl: graphic.Text, point: number[], orient: LayoutOrient, position: 'left' | 'right' | 'top' | 'bottom', margin: number): TextProps;
    _renderYearText(calendarModel: CalendarModel, rangeData: CalendarParsedDateRangeInfo, orient: LayoutOrient, group: graphic.Group): void;
    _monthTextPositionControl(point: number[], isCenter: boolean, orient: LayoutOrient, position: 'start' | 'end', margin: number): TextStyleProps;
    _renderMonthText(calendarModel: CalendarModel, orient: LayoutOrient, group: graphic.Group): void;
    _weekTextPositionControl(point: number[], orient: LayoutOrient, position: 'start' | 'end', margin: number, cellSize: number[]): TextStyleProps;
    _renderWeekText(calendarModel: CalendarModel, rangeData: CalendarParsedDateRangeInfo, orient: LayoutOrient, group: graphic.Group): void;
}
export default CalendarView;
