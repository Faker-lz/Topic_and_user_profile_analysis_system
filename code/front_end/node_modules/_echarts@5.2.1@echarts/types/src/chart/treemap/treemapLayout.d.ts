import { RectLike } from 'zrender/lib/core/BoundingRect';
import TreemapSeriesModel from './TreemapSeries';
import GlobalModel from '../../model/Global';
import ExtensionAPI from '../../core/ExtensionAPI';
import { TreeNode } from '../../data/Tree';
import { TreemapRenderPayload, TreemapMovePayload, TreemapZoomToNodePayload } from './treemapAction';
export interface TreemapLayoutNode extends TreeNode {
    parentNode: TreemapLayoutNode;
    children: TreemapLayoutNode[];
    viewChildren: TreemapLayoutNode[];
}
export interface TreemapItemLayout extends RectLike {
    area: number;
    isLeafRoot: boolean;
    dataExtent: [number, number];
    borderWidth: number;
    upperHeight: number;
    upperLabelHeight: number;
    isInView: boolean;
    invisible: boolean;
    isAboveViewRoot: boolean;
}
declare const _default: {
    seriesType: string;
    reset: (seriesModel: TreemapSeriesModel, ecModel: GlobalModel, api: ExtensionAPI, payload?: TreemapZoomToNodePayload | TreemapRenderPayload | TreemapMovePayload) => void;
};
/**
 * @public
 */
export default _default;
