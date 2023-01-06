import SymbolDraw from '../helper/SymbolDraw';
import * as graphic from '../../util/graphic';
import { ECPolyline, ECPolygon } from './poly';
import ChartView from '../../view/Chart';
import LineSeriesModel, { LineSeriesOption } from './LineSeries';
import type GlobalModel from '../../model/Global';
import type ExtensionAPI from '../../core/ExtensionAPI';
import Cartesian2D from '../../coord/cartesian/Cartesian2D';
import Polar from '../../coord/polar/Polar';
import type SeriesData from '../../data/SeriesData';
import type { Payload, DisplayState, LabelOption } from '../../util/types';
import { CoordinateSystemClipArea } from '../../coord/CoordinateSystem';
import Model from '../../model/Model';
declare type PolarArea = ReturnType<Polar['getArea']>;
declare type Cartesian2DArea = ReturnType<Cartesian2D['getArea']>;
interface EndLabelAnimationRecord {
    lastFrameIndex: number;
    originalX?: number;
    originalY?: number;
}
declare class LineView extends ChartView {
    static readonly type = "line";
    _symbolDraw: SymbolDraw;
    _lineGroup: graphic.Group;
    _coordSys: Cartesian2D | Polar;
    _endLabel: graphic.Text;
    _polyline: ECPolyline;
    _polygon: ECPolygon;
    _stackedOnPoints: ArrayLike<number>;
    _points: ArrayLike<number>;
    _step: LineSeriesOption['step'];
    _valueOrigin: LineSeriesOption['areaStyle']['origin'];
    _clipShapeForSymbol: CoordinateSystemClipArea;
    _data: SeriesData;
    init(): void;
    render(seriesModel: LineSeriesModel, ecModel: GlobalModel, api: ExtensionAPI): void;
    dispose(): void;
    highlight(seriesModel: LineSeriesModel, ecModel: GlobalModel, api: ExtensionAPI, payload: Payload): void;
    downplay(seriesModel: LineSeriesModel, ecModel: GlobalModel, api: ExtensionAPI, payload: Payload): void;
    _changePolyState(toState: DisplayState): void;
    _newPolyline(points: ArrayLike<number>): ECPolyline;
    _newPolygon(points: ArrayLike<number>, stackedOnPoints: ArrayLike<number>): ECPolygon;
    _initSymbolLabelAnimation(data: SeriesData, coordSys: Polar | Cartesian2D, clipShape: PolarArea | Cartesian2DArea): void;
    _initOrUpdateEndLabel(seriesModel: LineSeriesModel, coordSys: Cartesian2D, inheritColor: string): void;
    _endLabelOnDuring(percent: number, clipRect: graphic.Rect, data: SeriesData, animationRecord: EndLabelAnimationRecord, valueAnimation: boolean, endLabelModel: Model<LabelOption>, coordSys: Cartesian2D): void;
    /**
     * @private
     */
    _doUpdateAnimation(data: SeriesData, stackedOnPoints: ArrayLike<number>, coordSys: Cartesian2D | Polar, api: ExtensionAPI, step: LineSeriesOption['step'], valueOrigin: LineSeriesOption['areaStyle']['origin']): void;
    remove(ecModel: GlobalModel): void;
}
export default LineView;
