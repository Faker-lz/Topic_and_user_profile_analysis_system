import SeriesData from '../../data/SeriesData';
import { OptionSourceData, EncodeDefaulter } from '../../util/types';
import SeriesModel from '../../model/Series';
/**
 * Caution: there are side effects to `sourceManager` in this method.
 * Should better only be called in `Series['getInitialData']`.
 */
declare function createSeriesData(sourceRaw: OptionSourceData | null | undefined, seriesModel: SeriesModel, opt?: {
    generateCoord?: string;
    useEncodeDefaulter?: boolean | EncodeDefaulter;
    createInvertedIndices?: boolean;
}): SeriesData;
export default createSeriesData;
