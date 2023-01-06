import Axis from '../Axis';
import Scale from '../../scale/Scale';
import { DimensionName } from '../../util/types';
import { OptionAxisType } from '../axisCommonTypes';
import AxisModel from './AxisModel';
import Parallel from './Parallel';
declare class ParallelAxis extends Axis {
    readonly axisIndex: number;
    model: AxisModel;
    coordinateSystem: Parallel;
    constructor(dim: DimensionName, scale: Scale, coordExtent: [number, number], axisType: OptionAxisType, axisIndex: number);
    isHorizontal(): boolean;
}
export default ParallelAxis;
