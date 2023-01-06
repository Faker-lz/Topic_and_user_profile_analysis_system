import * as graphic from '../../util/graphic';
import { createSymbol } from '../../util/symbol';
import IncrementalDisplayable from 'zrender/lib/graphic/IncrementalDisplayable';
import SeriesData from '../../data/SeriesData';
import { PathProps } from 'zrender/lib/graphic/Path';
import PathProxy from 'zrender/lib/core/PathProxy';
import { StageHandlerProgressParams } from '../../util/types';
import { CoordinateSystemClipArea } from '../../coord/CoordinateSystem';
declare class LargeSymbolPathShape {
    points: ArrayLike<number>;
    size: number[];
}
declare type LargeSymbolPathProps = PathProps & {
    shape?: Partial<LargeSymbolPathShape>;
    startIndex?: number;
    endIndex?: number;
};
declare type ECSymbol = ReturnType<typeof createSymbol>;
declare class LargeSymbolPath extends graphic.Path<LargeSymbolPathProps> {
    shape: LargeSymbolPathShape;
    symbolProxy: ECSymbol;
    softClipShape: CoordinateSystemClipArea;
    startIndex: number;
    endIndex: number;
    private _ctx;
    constructor(opts?: LargeSymbolPathProps);
    getDefaultShape(): LargeSymbolPathShape;
    setColor: ECSymbol['setColor'];
    buildPath(path: PathProxy | CanvasRenderingContext2D, shape: LargeSymbolPathShape): void;
    afterBrush(): void;
    findDataIndex(x: number, y: number): number;
}
interface UpdateOpt {
    clipShape?: CoordinateSystemClipArea;
}
declare class LargeSymbolDraw {
    group: graphic.Group;
    _incremental: IncrementalDisplayable;
    isPersistent(): boolean;
    /**
     * Update symbols draw by new data
     */
    updateData(data: SeriesData, opt?: UpdateOpt): void;
    updateLayout(data: SeriesData): void;
    incrementalPrepareUpdate(data: SeriesData): void;
    incrementalUpdate(taskParams: StageHandlerProgressParams, data: SeriesData, opt: UpdateOpt): void;
    _setCommon(symbolEl: LargeSymbolPath, data: SeriesData, isIncremental: boolean, opt: UpdateOpt): void;
    remove(): void;
    _clearIncremental(): void;
}
export default LargeSymbolDraw;
