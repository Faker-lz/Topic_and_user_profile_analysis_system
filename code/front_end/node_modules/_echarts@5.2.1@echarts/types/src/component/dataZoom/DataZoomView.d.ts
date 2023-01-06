import ComponentView from '../../view/Component';
import DataZoomModel from './DataZoomModel';
import GlobalModel from '../../model/Global';
import ExtensionAPI from '../../core/ExtensionAPI';
declare class DataZoomView extends ComponentView {
    static type: string;
    type: string;
    dataZoomModel: DataZoomModel;
    ecModel: GlobalModel;
    api: ExtensionAPI;
    render(dataZoomModel: DataZoomModel, ecModel: GlobalModel, api: ExtensionAPI, payload: any): void;
}
export default DataZoomView;
