import SymbolDraw from '../../chart/helper/SymbolDraw';
import MarkerView from './MarkerView';
import SeriesModel from '../../model/Series';
import MarkPointModel from './MarkPointModel';
import GlobalModel from '../../model/Global';
import ExtensionAPI from '../../core/ExtensionAPI';
import { HashMap } from 'zrender/lib/core/util';
declare class MarkPointView extends MarkerView {
    static type: string;
    type: string;
    markerGroupMap: HashMap<SymbolDraw>;
    updateTransform(markPointModel: MarkPointModel, ecModel: GlobalModel, api: ExtensionAPI): void;
    renderSeries(seriesModel: SeriesModel, mpModel: MarkPointModel, ecModel: GlobalModel, api: ExtensionAPI): void;
}
export default MarkPointView;
