import View from '../View';
import { Region } from './Region';
import { GeoResource, NameMap } from './geoTypes';
import GlobalModel from '../../model/Global';
import { ParsedModelFinder } from '../../util/model';
import GeoModel from './GeoModel';
import { resizeGeoType } from './geoCreator';
export declare const geo2DDimensions: string[];
declare class Geo extends View {
    dimensions: string[];
    type: string;
    readonly map: string;
    readonly resourceType: GeoResource['type'];
    private _nameCoordMap;
    private _regionsMap;
    private _invertLongitute;
    readonly regions: Region[];
    readonly aspectScale: number;
    model: GeoModel;
    resize: resizeGeoType;
    constructor(name: string, map: string, opt: {
        nameMap?: NameMap;
        nameProperty?: string;
        aspectScale?: number;
    });
    /**
     * Whether contain the given [lng, lat] coord.
     */
    protected _transformTo(x: number, y: number, width: number, height: number): void;
    getRegion(name: string): Region;
    getRegionByCoord(coord: number[]): Region;
    /**
     * Add geoCoord for indexing by name
     */
    addGeoCoord(name: string, geoCoord: number[]): void;
    /**
     * Get geoCoord by name
     */
    getGeoCoord(name: string): number[];
    dataToPoint(data: number[] | string, noRoam?: boolean, out?: number[]): number[];
    convertToPixel(ecModel: GlobalModel, finder: ParsedModelFinder, value: number[]): number[];
    convertFromPixel(ecModel: GlobalModel, finder: ParsedModelFinder, pixel: number[]): number[];
}
export default Geo;
