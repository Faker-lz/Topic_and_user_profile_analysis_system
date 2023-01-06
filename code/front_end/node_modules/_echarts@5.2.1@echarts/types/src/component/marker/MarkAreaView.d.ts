import * as graphic from '../../util/graphic';
import MarkerView from './MarkerView';
import { HashMap } from 'zrender/lib/core/util';
import MarkAreaModel from './MarkAreaModel';
import SeriesModel from '../../model/Series';
import GlobalModel from '../../model/Global';
import ExtensionAPI from '../../core/ExtensionAPI';
interface MarkAreaDrawGroup {
    group: graphic.Group;
}
declare class MarkAreaView extends MarkerView {
    static type: string;
    type: string;
    markerGroupMap: HashMap<MarkAreaDrawGroup>;
    updateTransform(markAreaModel: MarkAreaModel, ecModel: GlobalModel, api: ExtensionAPI): void;
    renderSeries(seriesModel: SeriesModel, maModel: MarkAreaModel, ecModel: GlobalModel, api: ExtensionAPI): void;
}
export default MarkAreaView;
