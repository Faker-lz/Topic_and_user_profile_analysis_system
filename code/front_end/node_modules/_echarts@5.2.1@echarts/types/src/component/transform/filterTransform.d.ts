import { DataTransformOption, ExternalDataTransform } from '../../data/helper/transform';
import { ConditionalExpressionOption } from '../../util/conditionalExpression';
export interface FilterTransformOption extends DataTransformOption {
    type: 'filter';
    config: ConditionalExpressionOption;
}
export declare const filterTransform: ExternalDataTransform<FilterTransformOption>;
