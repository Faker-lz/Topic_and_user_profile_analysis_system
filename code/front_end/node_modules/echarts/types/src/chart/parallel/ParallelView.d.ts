import ChartView from '../../view/Chart';
import ParallelSeriesModel from './ParallelSeries';
import GlobalModel from '../../model/Global';
import ExtensionAPI from '../../core/ExtensionAPI';
import { StageHandlerProgressParams, Payload } from '../../util/types';
declare class ParallelView extends ChartView {
    static type: string;
    type: string;
    private _dataGroup;
    private _data;
    private _initialized;
    init(): void;
    /**
     * @override
     */
    render(seriesModel: ParallelSeriesModel, ecModel: GlobalModel, api: ExtensionAPI, payload: Payload): void;
    incrementalPrepareRender(seriesModel: ParallelSeriesModel, ecModel: GlobalModel, api: ExtensionAPI): void;
    incrementalRender(taskParams: StageHandlerProgressParams, seriesModel: ParallelSeriesModel, ecModel: GlobalModel): void;
    remove(): void;
}
export default ParallelView;
