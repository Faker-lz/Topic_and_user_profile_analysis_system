import ComponentView from '../../view/Component';
import GlobalModel from '../../model/Global';
import ExtensionAPI from '../../core/ExtensionAPI';
import GeoModel from '../../coord/geo/GeoModel';
import { Payload } from '../../util/types';
import Element from 'zrender/lib/Element';
declare class GeoView extends ComponentView {
    static type: "geo";
    readonly type: "geo";
    private _mapDraw;
    private _api;
    private _model;
    focusBlurEnabled: boolean;
    init(ecModel: GlobalModel, api: ExtensionAPI): void;
    render(geoModel: GeoModel, ecModel: GlobalModel, api: ExtensionAPI, payload: Payload): void;
    private _handleRegionClick;
    updateSelectStatus(model: GeoModel, ecModel: GlobalModel, api: ExtensionAPI): void;
    findHighDownDispatchers(name: string): Element[];
    dispose(): void;
}
export default GeoView;
