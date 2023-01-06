import LineDraw from '../../chart/helper/LineDraw';
import MarkerView from './MarkerView';
import MarkLineModel from './MarkLineModel';
import SeriesModel from '../../model/Series';
import ExtensionAPI from '../../core/ExtensionAPI';
import GlobalModel from '../../model/Global';
import { HashMap } from 'zrender/lib/core/util';
declare class MarkLineView extends MarkerView {
    static type: string;
    type: string;
    markerGroupMap: HashMap<LineDraw>;
    updateTransform(markLineModel: MarkLineModel, ecModel: GlobalModel, api: ExtensionAPI): void;
    renderSeries(seriesModel: SeriesModel, mlModel: MarkLineModel, ecModel: GlobalModel, api: ExtensionAPI): void;
}
export default MarkLineView;
