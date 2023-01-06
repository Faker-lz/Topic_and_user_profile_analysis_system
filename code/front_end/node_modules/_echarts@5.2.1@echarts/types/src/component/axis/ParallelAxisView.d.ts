import { BrushControllerEvents } from '../helper/BrushController';
import ComponentView from '../../view/Component';
import ExtensionAPI from '../../core/ExtensionAPI';
import GlobalModel from '../../model/Global';
import ParallelAxisModel, { ParallelAreaSelectStyleProps } from '../../coord/parallel/AxisModel';
import { Payload } from '../../util/types';
import ParallelModel from '../../coord/parallel/ParallelModel';
import { ParallelAxisLayoutInfo } from '../../coord/parallel/Parallel';
declare class ParallelAxisView extends ComponentView {
    static type: string;
    readonly type: string;
    private _brushController;
    private _axisGroup;
    axisModel: ParallelAxisModel;
    api: ExtensionAPI;
    init(ecModel: GlobalModel, api: ExtensionAPI): void;
    render(axisModel: ParallelAxisModel, ecModel: GlobalModel, api: ExtensionAPI, payload: Payload): void;
    _refreshBrushController(builderOpt: Pick<ParallelAxisLayoutInfo, 'position' | 'rotation'>, areaSelectStyle: ParallelAreaSelectStyleProps, axisModel: ParallelAxisModel, coordSysModel: ParallelModel, areaWidth: ParallelAreaSelectStyleProps['width'], api: ExtensionAPI): void;
    _onBrush(eventParam: BrushControllerEvents['brush']): void;
    dispose(): void;
}
export default ParallelAxisView;
