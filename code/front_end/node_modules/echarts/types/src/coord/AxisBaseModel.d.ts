/**
 * Base Axis Model for xAxis, yAxis, angleAxis, radiusAxis. singleAxis
 */
import { AxisBaseOptionCommon } from './axisCommonTypes';
import ComponentModel from '../model/Component';
import { AxisModelCommonMixin } from './axisModelCommonMixin';
import { AxisModelExtendedInCreator } from './axisModelCreator';
import Axis from './Axis';
export interface AxisBaseModel<T extends AxisBaseOptionCommon = AxisBaseOptionCommon> extends ComponentModel<T>, AxisModelCommonMixin<T>, AxisModelExtendedInCreator {
    axis: Axis;
}
