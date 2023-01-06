import ComponentView from '../../view/Component';
import AxisPointerModel from './AxisPointerModel';
import GlobalModel from '../../model/Global';
import ExtensionAPI from '../../core/ExtensionAPI';
declare class AxisPointerView extends ComponentView {
    static type: "axisPointer";
    type: "axisPointer";
    render(globalAxisPointerModel: AxisPointerModel, ecModel: GlobalModel, api: ExtensionAPI): void;
    remove(ecModel: GlobalModel, api: ExtensionAPI): void;
    dispose(ecModel: GlobalModel, api: ExtensionAPI): void;
}
export default AxisPointerView;
