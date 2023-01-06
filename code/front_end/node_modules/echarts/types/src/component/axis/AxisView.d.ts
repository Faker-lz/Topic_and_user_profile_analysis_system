import ComponentView from '../../view/Component';
import { AxisBaseModel } from '../../coord/AxisBaseModel';
import GlobalModel from '../../model/Global';
import ExtensionAPI from '../../core/ExtensionAPI';
import { Payload } from '../../util/types';
import type BaseAxisPointer from '../axisPointer/BaseAxisPointer';
interface AxisPointerConstructor {
    new (): BaseAxisPointer;
}
/**
 * Base class of AxisView.
 */
declare class AxisView extends ComponentView {
    static type: string;
    type: string;
    /**
     * @private
     */
    private _axisPointer;
    /**
     * @protected
     */
    axisPointerClass: string;
    /**
     * @override
     */
    render(axisModel: AxisBaseModel, ecModel: GlobalModel, api: ExtensionAPI, payload: Payload): void;
    /**
     * Action handler.
     */
    updateAxisPointer(axisModel: AxisBaseModel, ecModel: GlobalModel, api: ExtensionAPI, payload: Payload): void;
    /**
     * @override
     */
    remove(ecModel: GlobalModel, api: ExtensionAPI): void;
    /**
     * @override
     */
    dispose(ecModel: GlobalModel, api: ExtensionAPI): void;
    private _doUpdateAxisPointerClass;
    private _disposeAxisPointer;
    static registerAxisPointerClass(type: string, clazz: AxisPointerConstructor): void;
    static getAxisPointerClass(type: string): AxisPointerConstructor;
}
export default AxisView;
