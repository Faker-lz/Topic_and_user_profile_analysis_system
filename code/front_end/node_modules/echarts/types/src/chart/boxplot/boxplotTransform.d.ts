import { DataTransformOption, ExternalDataTransform } from '../../data/helper/transform';
import { PrepareBoxplotDataOpt } from './prepareBoxplotData';
export interface BoxplotTransformOption extends DataTransformOption {
    type: 'boxplot';
    config: PrepareBoxplotDataOpt;
}
export declare const boxplotTransform: ExternalDataTransform<BoxplotTransformOption>;
