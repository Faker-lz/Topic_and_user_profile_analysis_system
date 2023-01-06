import AxisView from './AxisView';
import GlobalModel from '../../model/Global';
import ExtensionAPI from '../../core/ExtensionAPI';
import CartesianAxisModel from '../../coord/cartesian/AxisModel';
import { Payload } from '../../util/types';
declare class CartesianAxisView extends AxisView {
    static type: string;
    type: string;
    axisPointerClass: string;
    private _axisGroup;
    /**
     * @override
     */
    render(axisModel: CartesianAxisModel, ecModel: GlobalModel, api: ExtensionAPI, payload: Payload): void;
    remove(): void;
}
export declare class CartesianXAxisView extends CartesianAxisView {
    static type: string;
    type: string;
}
export declare class CartesianYAxisView extends CartesianAxisView {
    static type: string;
    type: string;
}
export default CartesianAxisView;
