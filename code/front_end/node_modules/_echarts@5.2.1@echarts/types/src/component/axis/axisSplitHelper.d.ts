import * as graphic from '../../util/graphic';
import GridModel from '../../coord/cartesian/GridModel';
import type SingleAxisView from './SingleAxisView';
import type CartesianAxisView from './CartesianAxisView';
import type SingleAxisModel from '../../coord/single/AxisModel';
import type CartesianAxisModel from '../../coord/cartesian/AxisModel';
export declare function rectCoordAxisBuildSplitArea(axisView: SingleAxisView | CartesianAxisView, axisGroup: graphic.Group, axisModel: SingleAxisModel | CartesianAxisModel, gridModel: GridModel | SingleAxisModel): void;
export declare function rectCoordAxisHandleRemove(axisView: SingleAxisView | CartesianAxisView): void;
