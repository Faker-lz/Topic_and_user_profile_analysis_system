import Axis from '../Axis';
import Scale from '../../scale/Scale';
import Polar from './Polar';
import { RadiusAxisModel } from './AxisModel';
interface RadiusAxis {
    dataToRadius: Axis['dataToCoord'];
    radiusToData: Axis['coordToData'];
}
declare class RadiusAxis extends Axis {
    polar: Polar;
    model: RadiusAxisModel;
    constructor(scale?: Scale, radiusExtent?: [number, number]);
    pointToData(point: number[], clamp?: boolean): number;
}
export default RadiusAxis;
