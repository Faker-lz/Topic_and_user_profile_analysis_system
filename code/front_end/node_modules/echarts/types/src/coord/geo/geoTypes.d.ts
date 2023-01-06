import BoundingRect from 'zrender/lib/core/BoundingRect';
import { HashMap } from 'zrender/lib/core/util';
import { Group } from '../../util/graphic';
import { Region } from './Region';
export declare type GeoSVGSourceInput = string | Document | SVGElement;
export declare type GeoJSONSourceInput = string | GeoJSON | GeoJSONCompressed;
export interface NameMap {
    [regionName: string]: string;
}
export interface GeoSpecialAreas {
    [areaName: string]: {
        left: number;
        top: number;
        width?: number;
        height?: number;
    };
}
export interface GeoJSON extends GeoJSONFeatureCollection<GeoJSONGeometry> {
}
export interface GeoJSONCompressed extends GeoJSONFeatureCollection<GeoJSONGeometryCompressed> {
    UTF8Encoding?: boolean;
    UTF8Scale?: number;
}
interface GeoJSONFeatureCollection<G> {
    type: 'FeatureCollection';
    features: GeoJSONFeature<G>[];
}
interface GeoJSONFeature<G = GeoJSONGeometry> {
    type: 'Feature';
    id?: string | number;
    properties: {
        name?: string;
        cp?: number[];
        [key: string]: any;
    };
    geometry: G;
}
declare type GeoJSONGeometry = GeoJSONGeometryPoint | GeoJSONGeometryMultiPoint | GeoJSONGeometryLineString | GeoJSONGeometryMultiLineString | GeoJSONGeometryPolygon | GeoJSONGeometryMultiPolygon;
declare type GeoJSONGeometryCompressed = GeoJSONGeometryPoint | GeoJSONGeometryMultiPoint | GeoJSONGeometryLineString | GeoJSONGeometryMultiLineString | GeoJSONGeometryPolygonCompressed | GeoJSONGeometryMultiPolygonCompressed;
interface GeoJSONGeometryPoint {
    type: 'Point';
    coordinates: number[];
}
interface GeoJSONGeometryMultiPoint {
    type: 'MultiPoint';
    coordinates: number[][];
}
interface GeoJSONGeometryLineString {
    type: 'LineString';
    coordinates: number[][];
}
interface GeoJSONGeometryMultiLineString {
    type: 'MultiLineString';
    coordinates: number[][][];
}
export interface GeoJSONGeometryPolygon {
    type: 'Polygon';
    coordinates: number[][][];
}
interface GeoJSONGeometryPolygonCompressed {
    type: 'Polygon';
    coordinates: string[];
    encodeOffsets: number[][];
}
export interface GeoJSONGeometryMultiPolygon {
    type: 'MultiPolygon';
    coordinates: number[][][][];
}
interface GeoJSONGeometryMultiPolygonCompressed {
    type: 'MultiPolygon';
    coordinates: string[][];
    encodeOffsets: number[][][];
}
export interface GeoResource {
    readonly type: 'geoJSON' | 'geoSVG';
    load(nameMap: NameMap, nameProperty: string): {
        boundingRect: BoundingRect;
        regions: Region[];
        regionsMap: HashMap<Region>;
    };
}
export interface GeoSVGGraphicRoot extends Group {
    isGeoSVGGraphicRoot: boolean;
}
export {};
