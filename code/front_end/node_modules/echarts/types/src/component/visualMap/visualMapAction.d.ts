import { Payload } from '../../util/types';
import GlobalModel from '../../model/Global';
export declare const visualMapActionInfo: {
    type: string;
    event: string;
    update: string;
};
export declare const visualMapActionHander: (payload: Payload, ecModel: GlobalModel) => void;
