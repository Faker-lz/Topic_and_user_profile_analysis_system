import ChartView from '../../view/Chart';
import TreeSeriesModel from './TreeSeries';
import GlobalModel from '../../model/Global';
import ExtensionAPI from '../../core/ExtensionAPI';
declare class TreeView extends ChartView {
    static readonly type = "tree";
    readonly type = "tree";
    private _mainGroup;
    private _controller;
    private _controllerHost;
    private _data;
    private _nodeScaleRatio;
    private _min;
    private _max;
    init(ecModel: GlobalModel, api: ExtensionAPI): void;
    render(seriesModel: TreeSeriesModel, ecModel: GlobalModel, api: ExtensionAPI): void;
    _updateViewCoordSys(seriesModel: TreeSeriesModel): void;
    _updateController(seriesModel: TreeSeriesModel, ecModel: GlobalModel, api: ExtensionAPI): void;
    _updateNodeAndLinkScale(seriesModel: TreeSeriesModel): void;
    _getNodeGlobalScale(seriesModel: TreeSeriesModel): number;
    dispose(): void;
    remove(): void;
}
export default TreeView;
