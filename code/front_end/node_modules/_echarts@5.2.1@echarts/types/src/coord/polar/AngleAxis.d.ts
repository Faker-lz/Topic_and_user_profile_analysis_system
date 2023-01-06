import Axis from '../Axis';
import Scale from '../../scale/Scale';
import Polar from './Polar';
import { AngleAxisModel } from './AxisModel';
interface AngleAxis {
    dataToAngle: Axis['dataToCoord'];
    angleToData: Axis['coordToData'];
}
declare class AngleAxis extends Axis {
    polar: Polar;
    model: AngleAxisModel;
    constructor(scale?: Scale, angleExtent?: [number, number]);
    pointToData(point: number[], clamp?: boolean): number;
    /**
     * Only be called in category axis.
     * Angle axis uses text height to decide interval
     *
     * @override
     * @return {number} Auto interval for cateogry axis tick and label
     */
    calculateCategoryInterval(): number;
}
export default AngleAxis;
