import ChartView from '../../view/Chart';
import ThemeRiverSeriesModel from './ThemeRiverSeries';
import GlobalModel from '../../model/Global';
import ExtensionAPI from '../../core/ExtensionAPI';
declare class ThemeRiverView extends ChartView {
    static readonly type = "themeRiver";
    readonly type = "themeRiver";
    private _layersSeries;
    private _layers;
    render(seriesModel: ThemeRiverSeriesModel, ecModel: GlobalModel, api: ExtensionAPI): void;
}
export default ThemeRiverView;
