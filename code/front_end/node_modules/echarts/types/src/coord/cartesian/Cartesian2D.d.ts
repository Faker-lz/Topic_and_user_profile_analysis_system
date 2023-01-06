import BoundingRect from 'zrender/lib/core/BoundingRect';
import Cartesian from './Cartesian';
import { ScaleDataValue } from '../../util/types';
import Axis2D from './Axis2D';
import { CoordinateSystem } from '../CoordinateSystem';
import GridModel from './GridModel';
import Grid from './Grid';
export declare const cartesian2DDimensions: string[];
declare class Cartesian2D extends Cartesian<Axis2D> implements CoordinateSystem {
    readonly type = "cartesian2d";
    readonly dimensions: string[];
    model: GridModel;
    master: Grid;
    private _transform;
    private _invTransform;
    /**
     * Calculate an affine transform matrix if two axes are time or value.
     * It's mainly for accelartion on the large time series data.
     */
    calcAffineTransform(): void;
    /**
     * Base axis will be used on stacking.
     */
    getBaseAxis(): Axis2D;
    containPoint(point: number[]): boolean;
    containData(data: ScaleDataValue[]): boolean;
    dataToPoint(data: ScaleDataValue[], clamp?: boolean, out?: number[]): number[];
    clampData(data: ScaleDataValue[], out?: number[]): number[];
    pointToData(point: number[], clamp?: boolean): number[];
    getOtherAxis(axis: Axis2D): Axis2D;
    /**
     * Get rect area of cartesian.
     * Area will have a contain function to determine if a point is in the coordinate system.
     */
    getArea(): Cartesian2DArea;
}
interface Cartesian2DArea extends BoundingRect {
}
export default Cartesian2D;
