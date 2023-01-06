import SymbolDraw from '../helper/SymbolDraw';
import LargeSymbolDraw from '../helper/LargeSymbolDraw';
import ChartView from '../../view/Chart';
import ScatterSeriesModel from './ScatterSeries';
import GlobalModel from '../../model/Global';
import ExtensionAPI from '../../core/ExtensionAPI';
import SeriesData from '../../data/SeriesData';
import { TaskProgressParams } from '../../core/task';
declare class ScatterView extends ChartView {
    static readonly type = "scatter";
    type: string;
    _finished: boolean;
    _isLargeDraw: boolean;
    _symbolDraw: SymbolDraw | LargeSymbolDraw;
    render(seriesModel: ScatterSeriesModel, ecModel: GlobalModel, api: ExtensionAPI): void;
    incrementalPrepareRender(seriesModel: ScatterSeriesModel, ecModel: GlobalModel, api: ExtensionAPI): void;
    incrementalRender(taskParams: TaskProgressParams, seriesModel: ScatterSeriesModel, ecModel: GlobalModel): void;
    updateTransform(seriesModel: ScatterSeriesModel, ecModel: GlobalModel, api: ExtensionAPI): void | {
        update: true;
    };
    _getClipShape(seriesModel: ScatterSeriesModel): import("../../coord/CoordinateSystem").CoordinateSystemClipArea;
    _updateSymbolDraw(data: SeriesData, seriesModel: ScatterSeriesModel): SymbolDraw | LargeSymbolDraw;
    remove(ecModel: GlobalModel, api: ExtensionAPI): void;
    dispose(): void;
}
export default ScatterView;
