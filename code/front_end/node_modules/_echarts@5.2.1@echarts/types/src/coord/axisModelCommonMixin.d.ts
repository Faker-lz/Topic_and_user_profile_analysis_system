import Model from '../model/Model';
import Axis from './Axis';
import { AxisBaseOption } from './axisCommonTypes';
import { CoordinateSystemHostModel } from './CoordinateSystem';
interface AxisModelCommonMixin<Opt extends AxisBaseOption> extends Pick<Model<Opt>, 'option'> {
    axis: Axis;
}
declare class AxisModelCommonMixin<Opt extends AxisBaseOption> {
    getNeedCrossZero(): boolean;
    /**
     * Should be implemented by each axis model if necessary.
     * @return coordinate system model
     */
    getCoordSysModel(): CoordinateSystemHostModel;
}
export { AxisModelCommonMixin };
