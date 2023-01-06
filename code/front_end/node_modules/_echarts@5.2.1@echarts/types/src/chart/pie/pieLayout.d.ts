import GlobalModel from '../../model/Global';
import ExtensionAPI from '../../core/ExtensionAPI';
import PieSeriesModel from './PieSeries';
import { SectorShape } from 'zrender/lib/graphic/shape/Sector';
export declare function getBasicPieLayout(seriesModel: PieSeriesModel, api: ExtensionAPI): Pick<SectorShape, 'cx' | 'cy' | 'r' | 'r0'>;
export default function pieLayout(seriesType: 'pie', ecModel: GlobalModel, api: ExtensionAPI): void;
