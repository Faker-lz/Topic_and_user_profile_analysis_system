import ChartView from '../../view/Chart';
import RadarSeriesModel from './RadarSeries';
import ExtensionAPI from '../../core/ExtensionAPI';
import GlobalModel from '../../model/Global';
declare class RadarView extends ChartView {
    static type: string;
    type: string;
    private _data;
    render(seriesModel: RadarSeriesModel, ecModel: GlobalModel, api: ExtensionAPI): void;
    remove(): void;
}
export default RadarView;
