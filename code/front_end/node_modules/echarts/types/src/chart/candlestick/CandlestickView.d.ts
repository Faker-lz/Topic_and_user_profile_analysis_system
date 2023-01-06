import ChartView from '../../view/Chart';
import CandlestickSeriesModel from './CandlestickSeries';
import GlobalModel from '../../model/Global';
import ExtensionAPI from '../../core/ExtensionAPI';
import { StageHandlerProgressParams } from '../../util/types';
declare class CandlestickView extends ChartView {
    static readonly type = "candlestick";
    readonly type = "candlestick";
    private _isLargeDraw;
    private _data;
    render(seriesModel: CandlestickSeriesModel, ecModel: GlobalModel, api: ExtensionAPI): void;
    incrementalPrepareRender(seriesModel: CandlestickSeriesModel, ecModel: GlobalModel, api: ExtensionAPI): void;
    incrementalRender(params: StageHandlerProgressParams, seriesModel: CandlestickSeriesModel, ecModel: GlobalModel, api: ExtensionAPI): void;
    _updateDrawMode(seriesModel: CandlestickSeriesModel): void;
    _renderNormal(seriesModel: CandlestickSeriesModel): void;
    _renderLarge(seriesModel: CandlestickSeriesModel): void;
    _incrementalRenderNormal(params: StageHandlerProgressParams, seriesModel: CandlestickSeriesModel): void;
    _incrementalRenderLarge(params: StageHandlerProgressParams, seriesModel: CandlestickSeriesModel): void;
    remove(ecModel: GlobalModel): void;
    _clear(): void;
}
export default CandlestickView;
