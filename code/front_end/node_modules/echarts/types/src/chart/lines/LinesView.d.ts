import LineDraw from '../helper/LineDraw';
import LargeLineDraw from '../helper/LargeLineDraw';
import ChartView from '../../view/Chart';
import LinesSeriesModel from './LinesSeries';
import GlobalModel from '../../model/Global';
import ExtensionAPI from '../../core/ExtensionAPI';
import { StageHandlerProgressParams } from '../../util/types';
import SeriesData from '../../data/SeriesData';
declare class LinesView extends ChartView {
    static readonly type = "lines";
    readonly type = "lines";
    private _lastZlevel;
    private _finished;
    private _lineDraw;
    private _hasEffet;
    private _isPolyline;
    private _isLargeDraw;
    render(seriesModel: LinesSeriesModel, ecModel: GlobalModel, api: ExtensionAPI): void;
    incrementalPrepareRender(seriesModel: LinesSeriesModel, ecModel: GlobalModel, api: ExtensionAPI): void;
    incrementalRender(taskParams: StageHandlerProgressParams, seriesModel: LinesSeriesModel, ecModel: GlobalModel): void;
    updateTransform(seriesModel: LinesSeriesModel, ecModel: GlobalModel, api: ExtensionAPI): {
        readonly update: true;
    };
    _updateLineDraw(data: SeriesData, seriesModel: LinesSeriesModel): LineDraw | LargeLineDraw;
    private _showEffect;
    _clearLayer(api: ExtensionAPI): void;
    remove(ecModel: GlobalModel, api: ExtensionAPI): void;
    dispose(ecModel: GlobalModel, api: ExtensionAPI): void;
}
export default LinesView;
