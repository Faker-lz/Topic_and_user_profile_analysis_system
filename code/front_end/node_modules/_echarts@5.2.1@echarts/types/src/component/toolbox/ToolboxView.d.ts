import ComponentView from '../../view/Component';
import ToolboxModel from './ToolboxModel';
import GlobalModel from '../../model/Global';
import ExtensionAPI from '../../core/ExtensionAPI';
import { Dictionary, Payload } from '../../util/types';
import { ToolboxFeature, ToolboxFeatureOption, UserDefinedToolboxFeature } from './featureManager';
declare class ToolboxView extends ComponentView {
    static type: "toolbox";
    _features: Dictionary<ToolboxFeature | UserDefinedToolboxFeature>;
    _featureNames: string[];
    render(toolboxModel: ToolboxModel, ecModel: GlobalModel, api: ExtensionAPI, payload: Payload & {
        newTitle?: ToolboxFeatureOption['title'];
    }): void;
    updateView(toolboxModel: ToolboxModel, ecModel: GlobalModel, api: ExtensionAPI, payload: unknown): void;
    remove(ecModel: GlobalModel, api: ExtensionAPI): void;
    dispose(ecModel: GlobalModel, api: ExtensionAPI): void;
}
export default ToolboxView;
