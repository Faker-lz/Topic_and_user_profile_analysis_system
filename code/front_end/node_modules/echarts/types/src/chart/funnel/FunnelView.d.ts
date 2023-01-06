import ChartView from '../../view/Chart';
import FunnelSeriesModel from './FunnelSeries';
import GlobalModel from '../../model/Global';
import ExtensionAPI from '../../core/ExtensionAPI';
declare class FunnelView extends ChartView {
    static type: "funnel";
    type: "funnel";
    private _data;
    ignoreLabelLineUpdate: boolean;
    render(seriesModel: FunnelSeriesModel, ecModel: GlobalModel, api: ExtensionAPI): void;
    remove(): void;
    dispose(): void;
}
export default FunnelView;
