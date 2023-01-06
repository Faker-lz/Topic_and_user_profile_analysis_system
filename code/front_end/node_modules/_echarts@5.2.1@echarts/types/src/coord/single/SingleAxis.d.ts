import Axis from '../Axis';
import Scale from '../../scale/Scale';
import { OptionAxisType } from '../axisCommonTypes';
import SingleAxisModel, { SingleAxisPosition } from './AxisModel';
import { LayoutOrient } from '../../util/types';
import Single from './Single';
interface SingleAxis {
    /**
     * Transform global coord to local coord,
     * i.e. let localCoord = axis.toLocalCoord(80);
     */
    toLocalCoord(coord: number): number;
    /**
     * Transform global coord to local coord,
     * i.e. let globalCoord = axis.toLocalCoord(40);
     */
    toGlobalCoord(coord: number): number;
}
declare class SingleAxis extends Axis {
    position: SingleAxisPosition;
    orient: LayoutOrient;
    reverse: boolean;
    coordinateSystem: Single;
    model: SingleAxisModel;
    constructor(dim: string, scale: Scale, coordExtent: [number, number], axisType?: OptionAxisType, position?: SingleAxisPosition);
    /**
     * Judge the orient of the axis.
     */
    isHorizontal(): boolean;
    pointToData(point: number[], clamp?: boolean): number;
}
export default SingleAxis;
