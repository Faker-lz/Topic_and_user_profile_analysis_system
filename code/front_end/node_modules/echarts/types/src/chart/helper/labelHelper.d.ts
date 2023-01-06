import SeriesData from '../../data/SeriesData';
import { InterpolatableValue } from '../../util/types';
/**
 * @return label string. Not null/undefined
 */
export declare function getDefaultLabel(data: SeriesData, dataIndex: number): string;
export declare function getDefaultInterpolatedLabel(data: SeriesData, interpolatedValue: InterpolatableValue): string;
