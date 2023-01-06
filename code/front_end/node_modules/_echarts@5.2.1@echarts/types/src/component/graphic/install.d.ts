import { ComponentOption, BoxLayoutOptionMixin, Dictionary, ZRStyleProps, OptionId, CommonTooltipOption } from '../../util/types';
import Element, { ElementTextConfig } from 'zrender/lib/Element';
import Displayable from 'zrender/lib/graphic/Displayable';
import { PathProps } from 'zrender/lib/graphic/Path';
import { ImageStyleProps } from 'zrender/lib/graphic/Image';
import { TextStyleProps } from 'zrender/lib/graphic/Text';
import { EChartsExtensionInstallRegisters } from '../../extension';
declare const TRANSFORM_PROPS: {
    readonly x: 1;
    readonly y: 1;
    readonly scaleX: 1;
    readonly scaleY: 1;
    readonly originX: 1;
    readonly originY: 1;
    readonly rotation: 1;
};
declare type TransformProp = keyof typeof TRANSFORM_PROPS;
interface GraphicComponentBaseElementOption extends Partial<Pick<Element, TransformProp | 'silent' | 'ignore' | 'draggable' | 'textConfig' | 'onclick' | 'ondblclick' | 'onmouseover' | 'onmouseout' | 'onmousemove' | 'onmousewheel' | 'onmousedown' | 'onmouseup' | 'oncontextmenu' | 'ondrag' | 'ondragstart' | 'ondragend' | 'ondragenter' | 'ondragleave' | 'ondragover' | 'ondrop'>>, 
/**
 * left/right/top/bottom: (like 12, '22%', 'center', default undefined)
 * If left/rigth is set, shape.x/shape.cx/position will not be used.
 * If top/bottom is set, shape.y/shape.cy/position will not be used.
 * This mechanism is useful when you want to position a group/element
 * against the right side or the center of this container.
 */
Partial<Pick<BoxLayoutOptionMixin, 'left' | 'right' | 'top' | 'bottom'>> {
    /**
     * element type, mandatory.
     * Only can be omit if call setOption not at the first time and perform merge.
     */
    type?: string;
    id?: OptionId;
    name?: string;
    parentId?: OptionId;
    parentOption?: GraphicComponentElementOption;
    children?: GraphicComponentElementOption[];
    hv?: [boolean, boolean];
    /**
     * bounding: (enum: 'all' (default) | 'raw')
     * Specify how to calculate boundingRect when locating.
     * 'all': Get uioned and transformed boundingRect
     *     from both itself and its descendants.
     *     This mode simplies confining a group of elements in the bounding
     *     of their ancester container (e.g., using 'right: 0').
     * 'raw': Only use the boundingRect of itself and before transformed.
     *     This mode is similar to css behavior, which is useful when you
     *     want an element to be able to overflow its container. (Consider
     *     a rotated circle needs to be located in a corner.)
     */
    bounding?: 'raw' | 'all';
    /**
     * info: custom info. enables user to mount some info on elements and use them
     * in event handlers. Update them only when user specified, otherwise, remain.
     */
    info?: GraphicExtraElementInfo;
    textContent?: GraphicComponentTextOption;
    textConfig?: ElementTextConfig;
    $action?: 'merge' | 'replace' | 'remove';
    tooltip?: CommonTooltipOption<unknown>;
}
interface GraphicComponentDisplayableOption extends GraphicComponentBaseElementOption, Partial<Pick<Displayable, 'zlevel' | 'z' | 'z2' | 'invisible' | 'cursor'>> {
    style?: ZRStyleProps;
}
interface GraphicComponentGroupOption extends GraphicComponentBaseElementOption {
    type?: 'group';
    /**
     * width/height: (can only be pixel value, default 0)
     * Only be used to specify contianer(group) size, if needed. And
     * can not be percentage value (like '33%'). See the reason in the
     * layout algorithm below.
     */
    width?: number;
    height?: number;
    children: GraphicComponentElementOption[];
}
export interface GraphicComponentZRPathOption extends GraphicComponentDisplayableOption {
    shape?: PathProps['shape'];
}
export interface GraphicComponentImageOption extends GraphicComponentDisplayableOption {
    type?: 'image';
    style?: ImageStyleProps;
}
interface GraphicComponentTextOption extends Omit<GraphicComponentDisplayableOption, 'textContent' | 'textConfig'> {
    type?: 'text';
    style?: TextStyleProps;
}
declare type GraphicComponentElementOption = GraphicComponentGroupOption | GraphicComponentZRPathOption | GraphicComponentImageOption | GraphicComponentTextOption;
declare type GraphicExtraElementInfo = Dictionary<unknown>;
export declare type GraphicComponentLooseOption = (GraphicComponentOption | GraphicComponentElementOption) & {
    mainType?: 'graphic';
};
export interface GraphicComponentOption extends ComponentOption {
    elements?: GraphicComponentElementOption[];
}
export declare function install(registers: EChartsExtensionInstallRegisters): void;
export {};
