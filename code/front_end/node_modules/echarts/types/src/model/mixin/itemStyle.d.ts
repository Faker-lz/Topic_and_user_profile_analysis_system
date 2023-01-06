import Model from '../Model';
import { ItemStyleOption } from '../../util/types';
import { PathStyleProps } from 'zrender/lib/graphic/Path';
export declare const ITEM_STYLE_KEY_MAP: string[][];
declare type ItemStyleKeys = 'fill' | 'stroke' | 'decal' | 'lineWidth' | 'opacity' | 'shadowBlur' | 'shadowOffsetX' | 'shadowOffsetY' | 'shadowColor' | 'lineDash' | 'lineDashOffset' | 'lineCap' | 'lineJoin' | 'miterLimit';
export declare type ItemStyleProps = Pick<PathStyleProps, ItemStyleKeys>;
declare class ItemStyleMixin {
    getItemStyle(this: Model, excludes?: readonly (keyof ItemStyleOption)[], includes?: readonly (keyof ItemStyleOption)[]): ItemStyleProps;
}
export { ItemStyleMixin };
