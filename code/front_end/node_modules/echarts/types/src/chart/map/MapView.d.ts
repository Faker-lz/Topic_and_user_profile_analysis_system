import ChartView from '../../view/Chart';
import MapSeries from './MapSeries';
import GlobalModel from '../../model/Global';
import ExtensionAPI from '../../core/ExtensionAPI';
import { Payload } from '../../util/types';
declare class MapView extends ChartView {
    static type: "map";
    readonly type: "map";
    private _mapDraw;
    render(mapModel: MapSeries, ecModel: GlobalModel, api: ExtensionAPI, payload: Payload): void;
    remove(): void;
    dispose(): void;
    private _renderSymbols;
}
export default MapView;
