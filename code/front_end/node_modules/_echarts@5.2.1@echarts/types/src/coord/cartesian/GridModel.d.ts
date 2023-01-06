import ComponentModel from '../../model/Component';
import { ComponentOption, BoxLayoutOptionMixin, ZRColor, ShadowOptionMixin } from '../../util/types';
import Grid from './Grid';
import { CoordinateSystemHostModel } from '../CoordinateSystem';
export interface GridOption extends ComponentOption, BoxLayoutOptionMixin, ShadowOptionMixin {
    mainType?: 'grid';
    show?: boolean;
    containLabel?: boolean;
    backgroundColor?: ZRColor;
    borderWidth?: number;
    borderColor?: ZRColor;
    tooltip?: any;
}
declare class GridModel extends ComponentModel<GridOption> implements CoordinateSystemHostModel {
    static type: string;
    static dependencies: string[];
    static layoutMode: "box";
    coordinateSystem: Grid;
    static defaultOption: GridOption;
}
export default GridModel;
