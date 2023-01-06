import Geo from './Geo';
import { GeoOption, RegoinOption } from './GeoModel';
import { MapSeriesOption } from '../../chart/map/MapSeries';
import ExtensionAPI from '../../core/ExtensionAPI';
import { CoordinateSystemCreator } from '../CoordinateSystem';
import { NameMap } from './geoTypes';
import GlobalModel from '../../model/Global';
import ComponentModel from '../../model/Component';
export declare type resizeGeoType = typeof resizeGeo;
/**
 * Resize method bound to the geo
 */
declare function resizeGeo(this: Geo, geoModel: ComponentModel<GeoOption | MapSeriesOption>, api: ExtensionAPI): void;
declare class GeoCreator implements CoordinateSystemCreator {
    dimensions: string[];
    create(ecModel: GlobalModel, api: ExtensionAPI): Geo[];
    /**
     * Fill given regions array
     */
    getFilledRegions(originRegionArr: RegoinOption[], mapName: string, nameMap: NameMap, nameProperty: string): RegoinOption[];
}
declare const geoCreator: GeoCreator;
export default geoCreator;
