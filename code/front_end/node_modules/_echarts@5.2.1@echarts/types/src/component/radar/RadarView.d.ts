import ComponentView from '../../view/Component';
import RadarModel from '../../coord/radar/RadarModel';
import GlobalModel from '../../model/Global';
import ExtensionAPI from '../../core/ExtensionAPI';
declare class RadarView extends ComponentView {
    static type: string;
    type: string;
    render(radarModel: RadarModel, ecModel: GlobalModel, api: ExtensionAPI): void;
    _buildAxes(radarModel: RadarModel): void;
    _buildSplitLineAndArea(radarModel: RadarModel): void;
}
export default RadarView;
