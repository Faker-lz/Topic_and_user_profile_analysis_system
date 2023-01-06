import Axis from '../Axis';
import Scale from '../../scale/Scale';
import { OptionAxisType } from '../axisCommonTypes';
import { AxisBaseModel } from '../AxisBaseModel';
import { InnerIndicatorAxisOption } from './RadarModel';
declare class IndicatorAxis extends Axis {
    type: OptionAxisType;
    angle: number;
    name: string;
    model: AxisBaseModel<InnerIndicatorAxisOption>;
    constructor(dim: string, scale: Scale, radiusExtent?: [number, number]);
}
export default IndicatorAxis;
