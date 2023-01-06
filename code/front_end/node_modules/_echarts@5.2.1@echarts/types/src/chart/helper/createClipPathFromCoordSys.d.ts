import * as graphic from '../../util/graphic';
import SeriesModel from '../../model/Series';
import { SeriesOption } from '../../util/types';
import type Cartesian2D from '../../coord/cartesian/Cartesian2D';
import type Polar from '../../coord/polar/Polar';
import { CoordinateSystem } from '../../coord/CoordinateSystem';
declare type SeriesModelWithLineWidth = SeriesModel<SeriesOption & {
    lineStyle?: {
        width?: number;
    };
}>;
declare function createGridClipPath(cartesian: Cartesian2D, hasAnimation: boolean, seriesModel: SeriesModelWithLineWidth, done?: () => void, during?: (percent: number, clipRect: graphic.Rect) => void): graphic.Rect;
declare function createPolarClipPath(polar: Polar, hasAnimation: boolean, seriesModel: SeriesModelWithLineWidth): graphic.Sector;
declare function createClipPath(coordSys: CoordinateSystem, hasAnimation: boolean, seriesModel: SeriesModelWithLineWidth, done?: () => void, during?: (percent: number) => void): graphic.Rect | graphic.Sector;
export { createGridClipPath, createPolarClipPath, createClipPath };
