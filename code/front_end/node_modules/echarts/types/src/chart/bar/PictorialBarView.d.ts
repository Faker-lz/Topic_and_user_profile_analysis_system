import ChartView from '../../view/Chart';
import PictorialBarSeriesModel from './PictorialBarSeries';
import ExtensionAPI from '../../core/ExtensionAPI';
import GlobalModel from '../../model/Global';
declare class PictorialBarView extends ChartView {
    static type: string;
    readonly type: string;
    private _data;
    render(seriesModel: PictorialBarSeriesModel, ecModel: GlobalModel, api: ExtensionAPI): import("../../util/types").ViewRootGroup;
    remove(ecModel: GlobalModel, api: ExtensionAPI): void;
}
export default PictorialBarView;
