import GlobalModel from '../../model/Global';
import ExtensionAPI from '../../core/ExtensionAPI';
import { ThemeRiverSeriesOption } from './ThemeRiverSeries';
import { RectLike } from 'zrender/lib/core/BoundingRect';
export interface ThemeRiverLayoutInfo {
    rect: RectLike;
    boundaryGap: ThemeRiverSeriesOption['boundaryGap'];
}
export default function themeRiverLayout(ecModel: GlobalModel, api: ExtensionAPI): void;
