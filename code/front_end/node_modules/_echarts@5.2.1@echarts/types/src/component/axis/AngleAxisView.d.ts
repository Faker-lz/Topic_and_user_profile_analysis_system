import AxisView from './AxisView';
import { AngleAxisModel } from '../../coord/polar/AxisModel';
import GlobalModel from '../../model/Global';
declare class AngleAxisView extends AxisView {
    static readonly type = "angleAxis";
    readonly type = "angleAxis";
    axisPointerClass: string;
    render(angleAxisModel: AngleAxisModel, ecModel: GlobalModel): void;
}
export default AngleAxisView;
