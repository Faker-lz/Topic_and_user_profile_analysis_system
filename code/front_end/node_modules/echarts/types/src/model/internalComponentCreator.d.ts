import GlobalModel from './Global';
import { ComponentOption, ComponentMainType } from '../util/types';
interface InternalOptionCreator {
    (ecModel: GlobalModel): ComponentOption[];
}
export declare function registerInternalOptionCreator(mainType: ComponentMainType, creator: InternalOptionCreator): void;
export declare function concatInternalOptions(ecModel: GlobalModel, mainType: ComponentMainType, newCmptOptionList: ComponentOption[]): ComponentOption[];
export {};
