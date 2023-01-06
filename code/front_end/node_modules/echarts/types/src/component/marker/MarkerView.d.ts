import ComponentView from '../../view/Component';
import { HashMap } from 'zrender/lib/core/util';
import MarkerModel from './MarkerModel';
import GlobalModel from '../../model/Global';
import ExtensionAPI from '../../core/ExtensionAPI';
import SeriesModel from '../../model/Series';
import Group from 'zrender/lib/graphic/Group';
interface MarkerDraw {
    group: Group;
}
declare abstract class MarkerView extends ComponentView {
    static type: string;
    type: string;
    /**
     * Markline grouped by series
     */
    markerGroupMap: HashMap<MarkerDraw>;
    init(): void;
    render(markerModel: MarkerModel, ecModel: GlobalModel, api: ExtensionAPI): void;
    markKeep(drawGroup: MarkerDraw): void;
    blurSeries(seriesModelList: SeriesModel[]): void;
    abstract renderSeries(seriesModel: SeriesModel, markerModel: MarkerModel, ecModel: GlobalModel, api: ExtensionAPI): void;
}
export default MarkerView;
