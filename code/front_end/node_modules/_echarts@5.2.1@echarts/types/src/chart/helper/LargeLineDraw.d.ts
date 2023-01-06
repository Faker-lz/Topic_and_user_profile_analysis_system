import * as graphic from '../../util/graphic';
import IncrementalDisplayable from 'zrender/lib/graphic/IncrementalDisplayable';
import { PathProps } from 'zrender/lib/graphic/Path';
import SeriesData from '../../data/SeriesData';
import { StageHandlerProgressParams, LineStyleOption } from '../../util/types';
import Model from '../../model/Model';
declare class LargeLinesPathShape {
    polyline: boolean;
    curveness: number;
    segs: ArrayLike<number>;
}
interface LargeLinesPathProps extends PathProps {
    shape?: Partial<LargeLinesPathShape>;
}
interface LargeLinesCommonOption {
    polyline?: boolean;
    lineStyle?: LineStyleOption & {
        curveness?: number;
    };
}
/**
 * Data which can support large lines.
 */
declare type LargeLinesData = SeriesData<Model<LargeLinesCommonOption> & {
    seriesIndex?: number;
}>;
declare class LargeLinesPath extends graphic.Path {
    shape: LargeLinesPathShape;
    __startIndex: number;
    constructor(opts?: LargeLinesPathProps);
    getDefaultStyle(): {
        stroke: string;
        fill: string;
    };
    getDefaultShape(): LargeLinesPathShape;
    buildPath(ctx: CanvasRenderingContext2D, shape: LargeLinesPathShape): void;
    findDataIndex(x: number, y: number): number;
}
declare class LargeLineDraw {
    group: graphic.Group;
    _incremental?: IncrementalDisplayable;
    isPersistent(): boolean;
    /**
     * Update symbols draw by new data
     */
    updateData(data: LargeLinesData): void;
    /**
     * @override
     */
    incrementalPrepareUpdate(data: LargeLinesData): void;
    /**
     * @override
     */
    incrementalUpdate(taskParams: StageHandlerProgressParams, data: LargeLinesData): void;
    /**
     * @override
     */
    remove(): void;
    _setCommon(lineEl: LargeLinesPath, data: LargeLinesData, isIncremental?: boolean): void;
    _clearIncremental(): void;
}
export default LargeLineDraw;
