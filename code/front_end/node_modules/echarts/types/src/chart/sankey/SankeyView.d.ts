import SankeySeriesModel from './SankeySeries';
import ChartView from '../../view/Chart';
import GlobalModel from '../../model/Global';
import ExtensionAPI from '../../core/ExtensionAPI';
declare class SankeyView extends ChartView {
    static readonly type = "sankey";
    readonly type = "sankey";
    private _model;
    private _focusAdjacencyDisabled;
    private _data;
    render(seriesModel: SankeySeriesModel, ecModel: GlobalModel, api: ExtensionAPI): void;
    dispose(): void;
}
export default SankeyView;
