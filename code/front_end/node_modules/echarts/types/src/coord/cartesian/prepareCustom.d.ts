import Cartesian2D from './Cartesian2D';
export default function cartesianPrepareCustom(coordSys: Cartesian2D): {
    coordSys: {
        type: string;
        x: number;
        y: number;
        width: number;
        height: number;
    };
    api: {
        coord: (data: number[]) => number[];
        size: (dataSize: number[], dataItem: number[]) => number[];
    };
};
