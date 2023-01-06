import { DataTransformOption, ExternalDataTransform } from '../../data/helper/transform';
import { DimensionLoose } from '../../util/types';
import { RawValueParserType } from '../../data/helper/dataValueHelper';
/**
 * @usage
 *
 * ```js
 * transform: {
 *     type: 'sort',
 *     config: { dimension: 'score', order: 'asc' }
 * }
 * transform: {
 *     type: 'sort',
 *     config: [
 *         { dimension: 1, order: 'asc' },
 *         { dimension: 'age', order: 'desc' }
 *     ]
 * }
 * ```
 */
export interface SortTransformOption extends DataTransformOption {
    type: 'sort';
    config: OrderExpression | OrderExpression[];
}
declare type OrderExpression = {
    dimension: DimensionLoose;
    order: 'asc' | 'desc';
    parser?: RawValueParserType;
    incomparable?: 'min' | 'max';
};
export declare const sortTransform: ExternalDataTransform<SortTransformOption>;
export {};
