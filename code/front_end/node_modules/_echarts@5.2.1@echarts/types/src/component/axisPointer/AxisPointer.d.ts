import { AxisBaseModel } from '../../coord/AxisBaseModel';
import ExtensionAPI from '../../core/ExtensionAPI';
import { CommonAxisPointerOption } from '../../util/types';
import Model from '../../model/Model';
export interface AxisPointer {
    /**
     * If `show` called, axisPointer must be displayed or remain its original status.
     */
    render(axisModel: AxisBaseModel, axisPointerModel: Model<CommonAxisPointerOption>, api: ExtensionAPI, forceRender?: boolean): void;
    /**
     * If `hide` called, axisPointer must be hidden.
     */
    remove(api: ExtensionAPI): void;
    dispose(api: ExtensionAPI): void;
}
