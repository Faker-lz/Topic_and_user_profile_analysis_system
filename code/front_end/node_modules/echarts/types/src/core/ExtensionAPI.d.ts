import { EChartsType } from './echarts';
import type { CoordinateSystemMaster } from '../coord/CoordinateSystem';
import type Element from 'zrender/lib/Element';
import type ComponentModel from '../model/Component';
import type ComponentView from '../view/Component';
import type ChartView from '../view/Chart';
import type SeriesModel from '../model/Series';
import type GlobalModel from '../model/Global';
declare const availableMethods: (keyof EChartsType)[];
interface ExtensionAPI extends Pick<EChartsType, (typeof availableMethods)[number]> {
}
declare abstract class ExtensionAPI {
    constructor(ecInstance: EChartsType);
    abstract getCoordinateSystems(): CoordinateSystemMaster[];
    abstract getComponentByElement(el: Element): ComponentModel;
    abstract enterEmphasis(el: Element, highlightDigit?: number): void;
    abstract leaveEmphasis(el: Element, highlightDigit?: number): void;
    abstract enterSelect(el: Element): void;
    abstract leaveSelect(el: Element): void;
    abstract enterBlur(el: Element): void;
    abstract leaveBlur(el: Element): void;
    abstract getViewOfComponentModel(componentModel: ComponentModel): ComponentView;
    abstract getViewOfSeriesModel(seriesModel: SeriesModel): ChartView;
    abstract getModel(): GlobalModel;
}
export default ExtensionAPI;
