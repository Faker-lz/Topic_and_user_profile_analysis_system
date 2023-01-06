import * as graphic from '../../util/graphic';
import { TreeNode } from '../../data/Tree';
import SunburstSeriesModel from './SunburstSeries';
import GlobalModel from '../../model/Global';
import ExtensionAPI from '../../core/ExtensionAPI';
/**
 * Sunburstce of Sunburst including Sector, Label, LabelLine
 */
declare class SunburstPiece extends graphic.Sector {
    node: TreeNode;
    private _seriesModel;
    private _ecModel;
    constructor(node: TreeNode, seriesModel: SunburstSeriesModel, ecModel: GlobalModel, api: ExtensionAPI);
    updateData(firstCreate: boolean, node: TreeNode, seriesModel: SunburstSeriesModel, ecModel: GlobalModel, api: ExtensionAPI): void;
    _updateLabel(seriesModel: SunburstSeriesModel): void;
}
export default SunburstPiece;
