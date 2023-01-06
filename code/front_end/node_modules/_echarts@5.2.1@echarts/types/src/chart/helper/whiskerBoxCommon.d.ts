import type { SeriesOption, SeriesOnCartesianOptionMixin, LayoutOrient } from '../../util/types';
import type GlobalModel from '../../model/Global';
import type SeriesModel from '../../model/Series';
import type SeriesData from '../../data/SeriesData';
import type Axis2D from '../../coord/cartesian/Axis2D';
import { CoordDimensionDefinition } from '../../data/helper/createDimensions';
interface CommonOption extends SeriesOption, SeriesOnCartesianOptionMixin {
    layout?: LayoutOrient;
}
interface WhiskerBoxCommonMixin<Opts extends CommonOption> extends SeriesModel<Opts> {
}
declare class WhiskerBoxCommonMixin<Opts extends CommonOption> {
    /**
     * @private
     * @type {string}
     */
    _baseAxisDim: string;
    defaultValueDimensions: CoordDimensionDefinition['dimsDef'];
    /**
     * @override
     */
    getInitialData(option: Opts, ecModel: GlobalModel): SeriesData;
    /**
     * If horizontal, base axis is x, otherwise y.
     * @override
     */
    getBaseAxis(): Axis2D;
}
export { WhiskerBoxCommonMixin };
