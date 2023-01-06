import ComponentModel from '../../model/Component';
import { AxisModelExtendedInCreator } from '../axisModelCreator';
import { AxisModelCommonMixin } from '../axisModelCommonMixin';
import Axis2D from './Axis2D';
import { AxisBaseOption } from '../axisCommonTypes';
import GridModel from './GridModel';
import { AxisBaseModel } from '../AxisBaseModel';
import { OrdinalSortInfo } from '../../util/types';
export declare type CartesianAxisPosition = 'top' | 'bottom' | 'left' | 'right';
export declare type CartesianAxisOption = AxisBaseOption & {
    gridIndex?: number;
    gridId?: string;
    position?: CartesianAxisPosition;
    offset?: number;
    categorySortInfo?: OrdinalSortInfo;
};
export declare type XAXisOption = CartesianAxisOption & {
    mainType?: 'xAxis';
};
export declare type YAXisOption = CartesianAxisOption & {
    mainType?: 'yAxis';
};
export declare class CartesianAxisModel extends ComponentModel<CartesianAxisOption> implements AxisBaseModel<CartesianAxisOption> {
    static type: string;
    axis: Axis2D;
    getCoordSysModel(): GridModel;
}
export interface CartesianAxisModel extends AxisModelCommonMixin<CartesianAxisOption>, AxisModelExtendedInCreator {
}
export default CartesianAxisModel;
