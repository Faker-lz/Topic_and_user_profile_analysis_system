import { ComponentOption, CircleLayoutOptionMixin } from '../../util/types';
import ComponentModel from '../../model/Component';
import Polar from './Polar';
import { AngleAxisModel, RadiusAxisModel } from './AxisModel';
export interface PolarOption extends ComponentOption, CircleLayoutOptionMixin {
    mainType?: 'polar';
}
declare class PolarModel extends ComponentModel<PolarOption> {
    static type: "polar";
    type: "polar";
    static dependencies: string[];
    coordinateSystem: Polar;
    findAxisModel(axisType: 'angleAxis'): AngleAxisModel;
    findAxisModel(axisType: 'radiusAxis'): RadiusAxisModel;
    static defaultOption: PolarOption;
}
export default PolarModel;
