import { ToolboxFeatureOption, ToolboxFeature } from '../featureManager';
import ExtensionAPI from '../../../core/ExtensionAPI';
import GlobalModel from '../../../model/Global';
export interface ToolboxRestoreFeatureOption extends ToolboxFeatureOption {
    icon?: string;
    title?: string;
}
declare class RestoreOption extends ToolboxFeature<ToolboxRestoreFeatureOption> {
    onclick(ecModel: GlobalModel, api: ExtensionAPI): void;
    static getDefaultOption(ecModel: GlobalModel): ToolboxRestoreFeatureOption;
}
export default RestoreOption;
