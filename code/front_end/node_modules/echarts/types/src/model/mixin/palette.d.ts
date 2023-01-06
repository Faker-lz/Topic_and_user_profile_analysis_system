import Model from '../Model';
import { ZRColor, PaletteOptionMixin, DecalObject } from '../../util/types';
import GlobalModel from '../Global';
interface PaletteMixin<T extends PaletteOptionMixin = PaletteOptionMixin> extends Pick<Model<T>, 'get'> {
}
declare class PaletteMixin<T extends PaletteOptionMixin = PaletteOptionMixin> {
    getColorFromPalette(this: PaletteMixin<T>, name: string, scope?: any, requestNum?: number): ZRColor;
    clearColorPalette(this: PaletteMixin<T>): void;
}
export declare function getDecalFromPalette(ecModel: GlobalModel, name: string, scope?: any, requestNum?: number): DecalObject;
export { PaletteMixin };
