import * as graphic from '../../util/graphic';
import type { LineDrawSeriesScope } from './LineDraw';
import type SeriesData from '../../data/SeriesData';
declare class Polyline extends graphic.Group {
    constructor(lineData: SeriesData, idx: number, seriesScope: LineDrawSeriesScope);
    private _createPolyline;
    updateData(lineData: SeriesData, idx: number, seriesScope: LineDrawSeriesScope): void;
    _updateCommonStl(lineData: SeriesData, idx: number, seriesScope: LineDrawSeriesScope): void;
    updateLayout(lineData: SeriesData, idx: number): void;
}
export default Polyline;
