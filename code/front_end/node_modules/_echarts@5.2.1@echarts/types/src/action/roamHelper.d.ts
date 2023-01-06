import View from '../coord/View';
import { Payload } from '../util/types';
export interface RoamPaylod extends Payload {
    dx: number;
    dy: number;
    zoom: number;
    originX: number;
    originY: number;
}
export declare function updateCenterAndZoom(view: View, payload: RoamPaylod, zoomLimit?: {
    min?: number;
    max?: number;
}): {
    center: number[];
    zoom: number;
};
