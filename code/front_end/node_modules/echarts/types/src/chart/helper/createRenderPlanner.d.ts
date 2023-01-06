import SeriesModel from '../../model/Series';
import { StageHandlerPlanReturn } from '../../util/types';
/**
 * @return {string} If large mode changed, return string 'reset';
 */
export default function createRenderPlanner(): (seriesModel: SeriesModel) => StageHandlerPlanReturn;
