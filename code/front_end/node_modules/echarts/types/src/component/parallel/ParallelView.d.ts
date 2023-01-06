import GlobalModel from '../../model/Global';
import ParallelModel from '../../coord/parallel/ParallelModel';
import ExtensionAPI from '../../core/ExtensionAPI';
import ComponentView from '../../view/Component';
import { ParallelAxisExpandPayload } from '../axis/parallelAxisAction';
declare class ParallelView extends ComponentView {
    static type: string;
    readonly type: string;
    _model: ParallelModel;
    private _api;
    _mouseDownPoint: number[];
    private _handlers;
    render(parallelModel: ParallelModel, ecModel: GlobalModel, api: ExtensionAPI): void;
    dispose(ecModel: GlobalModel, api: ExtensionAPI): void;
    /**
     * @internal
     * @param {Object} [opt] If null, cancle the last action triggering for debounce.
     */
    _throttledDispatchExpand(this: ParallelView, opt: Omit<ParallelAxisExpandPayload, 'type'>): void;
    /**
     * @internal
     */
    _dispatchExpand(opt: Omit<ParallelAxisExpandPayload, 'type'>): void;
}
export default ParallelView;
