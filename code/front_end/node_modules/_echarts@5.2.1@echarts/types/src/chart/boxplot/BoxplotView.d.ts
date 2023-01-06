import ChartView from '../../view/Chart';
import BoxplotSeriesModel from './BoxplotSeries';
import GlobalModel from '../../model/Global';
import ExtensionAPI from '../../core/ExtensionAPI';
declare class BoxplotView extends ChartView {
    static type: string;
    type: string;
    private _data;
    render(seriesModel: BoxplotSeriesModel, ecModel: GlobalModel, api: ExtensionAPI): void;
    remove(ecModel: GlobalModel): void;
}
export default BoxplotView;
