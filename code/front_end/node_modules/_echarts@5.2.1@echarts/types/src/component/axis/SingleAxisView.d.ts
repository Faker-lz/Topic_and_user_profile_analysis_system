import AxisView from './AxisView';
import SingleAxisModel from '../../coord/single/AxisModel';
import GlobalModel from '../../model/Global';
import ExtensionAPI from '../../core/ExtensionAPI';
import { Payload } from '../../util/types';
declare class SingleAxisView extends AxisView {
    static readonly type = "singleAxis";
    readonly type = "singleAxis";
    private _axisGroup;
    axisPointerClass: string;
    render(axisModel: SingleAxisModel, ecModel: GlobalModel, api: ExtensionAPI, payload: Payload): void;
    remove(): void;
}
export default SingleAxisView;
