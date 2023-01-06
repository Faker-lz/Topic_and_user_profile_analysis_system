import Eventful from 'zrender/lib/core/Eventful';
import SeriesModel from '../model/Series';
import GlobalModel from '../model/Global';
import { EChartsType } from './echarts';
import ExtensionAPI from './ExtensionAPI';
import { ModelFinderIdQuery, ModelFinderIndexQuery } from '../util/model';
import { DimensionLoose } from '../util/types';
export interface UpdateLifecycleTransitionSeriesFinder {
    seriesIndex?: ModelFinderIndexQuery;
    seriesId?: ModelFinderIdQuery;
    dimension: DimensionLoose;
}
export interface UpdateLifecycleTransitionItem {
    from?: UpdateLifecycleTransitionSeriesFinder | UpdateLifecycleTransitionSeriesFinder[];
    to: UpdateLifecycleTransitionSeriesFinder | UpdateLifecycleTransitionSeriesFinder[];
}
export declare type UpdateLifecycleTransitionOpt = UpdateLifecycleTransitionItem | UpdateLifecycleTransitionItem[];
export interface UpdateLifecycleParams {
    updatedSeries?: SeriesModel[];
    /**
     * If this update is from setOption and option is changed.
     */
    optionChanged?: boolean;
    seriesTransition?: UpdateLifecycleTransitionOpt;
}
interface LifecycleEvents {
    'afterinit': [EChartsType];
    'series:beforeupdate': [GlobalModel, ExtensionAPI, UpdateLifecycleParams];
    'series:layoutlabels': [GlobalModel, ExtensionAPI, UpdateLifecycleParams];
    'series:transition': [GlobalModel, ExtensionAPI, UpdateLifecycleParams];
    'series:afterupdate': [GlobalModel, ExtensionAPI, UpdateLifecycleParams];
    'afterupdate': [GlobalModel, ExtensionAPI];
}
declare const lifecycle: Eventful<{
    afterinit: (args_0: EChartsType) => boolean | void;
    'series:beforeupdate': (args_0: GlobalModel, args_1: ExtensionAPI, args_2: UpdateLifecycleParams) => boolean | void;
    'series:layoutlabels': (args_0: GlobalModel, args_1: ExtensionAPI, args_2: UpdateLifecycleParams) => boolean | void;
    'series:transition': (args_0: GlobalModel, args_1: ExtensionAPI, args_2: UpdateLifecycleParams) => boolean | void;
    'series:afterupdate': (args_0: GlobalModel, args_1: ExtensionAPI, args_2: UpdateLifecycleParams) => boolean | void;
    afterupdate: (args_0: GlobalModel, args_1: ExtensionAPI) => boolean | void;
}>;
export default lifecycle;
export { LifecycleEvents };
