import * as graphic from '../../util/graphic';
import ChartView from '../../view/Chart';
import HeatmapSeriesModel from './HeatmapSeries';
import type GlobalModel from '../../model/Global';
import type ExtensionAPI from '../../core/ExtensionAPI';
import type VisualMapModel from '../../component/visualMap/VisualMapModel';
import { CoordinateSystem } from '../../coord/CoordinateSystem';
import { StageHandlerProgressParams } from '../../util/types';
interface GeoLikeCoordSys extends CoordinateSystem {
    dimensions: ['lng', 'lat'];
    getViewRect(): graphic.BoundingRect;
}
declare class HeatmapView extends ChartView {
    static readonly type = "heatmap";
    readonly type = "heatmap";
    private _incrementalDisplayable;
    private _hmLayer;
    render(seriesModel: HeatmapSeriesModel, ecModel: GlobalModel, api: ExtensionAPI): void;
    incrementalPrepareRender(seriesModel: HeatmapSeriesModel, ecModel: GlobalModel, api: ExtensionAPI): void;
    incrementalRender(params: StageHandlerProgressParams, seriesModel: HeatmapSeriesModel, ecModel: GlobalModel, api: ExtensionAPI): void;
    _renderOnCartesianAndCalendar(seriesModel: HeatmapSeriesModel, api: ExtensionAPI, start: number, end: number, incremental?: boolean): void;
    _renderOnGeo(geo: GeoLikeCoordSys, seriesModel: HeatmapSeriesModel, visualMapModel: VisualMapModel, api: ExtensionAPI): void;
}
export default HeatmapView;
