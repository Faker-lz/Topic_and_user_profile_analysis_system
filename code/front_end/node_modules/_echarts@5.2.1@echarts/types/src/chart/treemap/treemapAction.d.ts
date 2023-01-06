import { Payload } from '../../util/types';
import { TreeNode } from '../../data/Tree';
import { RectLike } from 'zrender/lib/core/BoundingRect';
import { EChartsExtensionInstallRegisters } from '../../extension';
export interface TreemapZoomToNodePayload extends Payload {
    type: 'treemapZoomToNode';
}
export interface TreemapRenderPayload extends Payload {
    type: 'treemapRender';
    rootRect?: RectLike;
}
export interface TreemapMovePayload extends Payload {
    type: 'treemapMove';
    rootRect?: RectLike;
}
export interface TreemapRootToNodePayload extends Payload {
    type: 'treemapRootToNode';
    targetNode?: TreeNode | string;
    targetNodeId?: string;
    direction?: 'rollUp' | 'drillDown';
}
export declare function installTreemapAction(registers: EChartsExtensionInstallRegisters): void;
