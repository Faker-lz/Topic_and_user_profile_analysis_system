import { ToolboxFeature, ToolboxFeatureOption } from '../featureManager';
import { ZRColor } from '../../../util/types';
import GlobalModel from '../../../model/Global';
import ExtensionAPI from '../../../core/ExtensionAPI';
export interface ToolboxSaveAsImageFeatureOption extends ToolboxFeatureOption {
    icon?: string;
    title?: string;
    type?: 'png' | 'jpg';
    backgroundColor?: ZRColor;
    connectedBackgroundColor?: ZRColor;
    name?: string;
    excludeComponents?: string[];
    pixelRatio?: number;
    lang?: string[];
}
declare class SaveAsImage extends ToolboxFeature<ToolboxSaveAsImageFeatureOption> {
    onclick(ecModel: GlobalModel, api: ExtensionAPI): void;
    static getDefaultOption(ecModel: GlobalModel): ToolboxSaveAsImageFeatureOption;
}
export default SaveAsImage;
