import ChartView from '../../view/Chart';
import GlobalModel from '../../model/Global';
import ExtensionAPI from '../../core/ExtensionAPI';
import EffectScatterSeriesModel from './EffectScatterSeries';
declare class EffectScatterView extends ChartView {
    static readonly type = "effectScatter";
    readonly type = "effectScatter";
    private _symbolDraw;
    init(): void;
    render(seriesModel: EffectScatterSeriesModel, ecModel: GlobalModel, api: ExtensionAPI): void;
    _getClipShape(seriesModel: EffectScatterSeriesModel): import("../../coord/CoordinateSystem").CoordinateSystemClipArea;
    updateTransform(seriesModel: EffectScatterSeriesModel, ecModel: GlobalModel, api: ExtensionAPI): void;
    _updateGroupTransform(seriesModel: EffectScatterSeriesModel): void;
    remove(ecModel: GlobalModel, api: ExtensionAPI): void;
}
export default EffectScatterView;
