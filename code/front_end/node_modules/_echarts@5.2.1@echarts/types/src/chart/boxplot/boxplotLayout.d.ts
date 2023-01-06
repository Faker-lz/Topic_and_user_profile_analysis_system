import type GlobalModel from '../../model/Global';
export interface BoxplotItemLayout {
    ends: number[][];
    initBaseline: number;
}
export default function boxplotLayout(ecModel: GlobalModel): void;
