import BoundingRect from 'zrender/lib/core/BoundingRect';
import { GeoJSON } from './geoTypes';
import Element from 'zrender/lib/Element';
export declare class Region {
    readonly name: string;
    readonly type: 'geoJSON' | 'geoSVG';
    constructor(name: string);
    /**
     * Get center point in data unit. That is,
     * for GeoJSONRegion, the unit is lat/lng,
     * for GeoSVGRegion, the unit is SVG local coord.
     */
    getCenter(): number[];
}
export declare class GeoJSONRegion extends Region {
    readonly type = "geoJSON";
    readonly geometries: {
        type: 'polygon';
        exterior: number[][];
        interiors?: number[][][];
    }[];
    private _center;
    properties: GeoJSON['features'][0]['properties'];
    private _rect;
    constructor(name: string, geometries: GeoJSONRegion['geometries'], cp: GeoJSON['features'][0]['properties']['cp']);
    getBoundingRect(): BoundingRect;
    contain(coord: number[]): boolean;
    transformTo(x: number, y: number, width: number, height: number): void;
    cloneShallow(name: string): GeoJSONRegion;
    getCenter(): number[];
    setCenter(center: number[]): void;
}
export declare class GeoSVGRegion extends Region {
    readonly type = "geoSVG";
    private _center;
    private _elOnlyForCalculate;
    constructor(name: string, elOnlyForCalculate: Element);
    getCenter(): number[];
    private _calculateCenter;
}
