/**
 * Provide effect for line
 */
import * as graphic from '../../util/graphic';
import { createSymbol } from '../../util/symbol';
import type SeriesData from '../../data/SeriesData';
import { LineDrawSeriesScope } from './LineDraw';
export declare type ECSymbolOnEffectLine = ReturnType<typeof createSymbol> & {
    __t: number;
    __lastT: number;
    __p1: number[];
    __p2: number[];
    __cp1: number[];
};
declare class EffectLine extends graphic.Group {
    private _symbolType;
    private _period;
    private _loop;
    private _symbolScale;
    constructor(lineData: SeriesData, idx: number, seriesScope: LineDrawSeriesScope);
    createLine(lineData: SeriesData, idx: number, seriesScope: LineDrawSeriesScope): graphic.Group;
    private _updateEffectSymbol;
    private _updateEffectAnimation;
    protected _getLineLength(symbol: ECSymbolOnEffectLine): number;
    protected _updateAnimationPoints(symbol: ECSymbolOnEffectLine, points: number[][]): void;
    updateData(lineData: SeriesData, idx: number, seriesScope: LineDrawSeriesScope): void;
    protected _updateSymbolPosition(symbol: ECSymbolOnEffectLine): void;
    updateLayout(lineData: SeriesData, idx: number): void;
}
export default EffectLine;
