import Element, { ElementProps } from 'zrender/lib/Element';
import { CustomDisplayableOption, CustomElementOption, LooseElementProps } from './CustomSeries';
export declare function prepareShapeOrExtraTransitionFrom(mainAttr: 'shape' | 'extra', fromEl: Element, elOption: CustomElementOption, transFromProps: LooseElementProps, isInit: boolean): void;
export declare function prepareShapeOrExtraAllPropsFinal(mainAttr: 'shape' | 'extra', elOption: CustomElementOption, allProps: LooseElementProps): void;
export declare function prepareTransformTransitionFrom(el: Element, elOption: CustomElementOption, transFromProps: ElementProps, isInit: boolean): void;
export declare function prepareTransformAllPropsFinal(el: Element, elOption: CustomElementOption, allProps: ElementProps): void;
export declare function prepareStyleTransitionFrom(fromEl: Element, elOption: CustomElementOption, styleOpt: CustomDisplayableOption['style'], transFromProps: LooseElementProps, isInit: boolean): void;
