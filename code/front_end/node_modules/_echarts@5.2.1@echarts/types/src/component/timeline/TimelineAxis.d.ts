import Axis from '../../coord/Axis';
import Scale from '../../scale/Scale';
import TimelineModel from './TimelineModel';
import { LabelOption } from '../../util/types';
import Model from '../../model/Model';
/**
 * Extend axis 2d
 */
declare class TimelineAxis extends Axis {
    type: 'category' | 'time' | 'value';
    model: TimelineModel;
    constructor(dim: string, scale: Scale, coordExtent: [number, number], axisType: 'category' | 'time' | 'value');
    /**
     * @override
     */
    getLabelModel(): Model<LabelOption>;
    /**
     * @override
     */
    isHorizontal(): boolean;
}
export default TimelineAxis;
