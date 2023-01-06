import ComponentModel from '../model/Component';
import OrdinalMeta from '../data/OrdinalMeta';
import { DimensionName, OrdinalRawValue } from '../util/types';
import { AxisBaseOption, CategoryAxisBaseOption } from './axisCommonTypes';
import { EChartsExtensionInstallRegisters } from '../extension';
declare type Constructor<T> = new (...args: any[]) => T;
export interface AxisModelExtendedInCreator {
    getCategories(rawData?: boolean): OrdinalRawValue[] | CategoryAxisBaseOption['data'];
    getOrdinalMeta(): OrdinalMeta;
}
/**
 * Generate sub axis model class
 * @param axisName 'x' 'y' 'radius' 'angle' 'parallel' ...
 */
export default function axisModelCreator<AxisOptionT extends AxisBaseOption, AxisModelCtor extends Constructor<ComponentModel<AxisOptionT>>>(registers: EChartsExtensionInstallRegisters, axisName: DimensionName, BaseAxisModelClass: AxisModelCtor, extraDefaultOption?: AxisOptionT): void;
export {};
