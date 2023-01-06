import Displayable from 'zrender/lib/graphic/Displayable';
import { ImageStyleProps } from 'zrender/lib/graphic/Image';
import { PathProps, PathStyleProps } from 'zrender/lib/graphic/Path';
import { ZRenderType } from 'zrender/lib/zrender';
import { BarGridLayoutOptionForCustomSeries, BarGridLayoutResult } from '../../layout/barGrid';
import { BlurScope, CallbackDataParams, Dictionary, DimensionLoose, ItemStyleOption, LabelOption, OptionDataValue, OrdinalRawValue, ParsedValue, SeriesDataType, SeriesEncodeOptionMixin, SeriesOnCalendarOptionMixin, SeriesOnCartesianOptionMixin, SeriesOnGeoOptionMixin, SeriesOnPolarOptionMixin, SeriesOnSingleOptionMixin, SeriesOption, TextCommonOption, ZRStyleProps } from '../../util/types';
import Element, { ElementProps } from 'zrender/lib/Element';
import SeriesData, { DefaultDataVisual } from '../../data/SeriesData';
import GlobalModel from '../../model/Global';
import { CoordinateSystem } from '../../coord/CoordinateSystem';
import SeriesModel from '../../model/Series';
import { Arc, BezierCurve, Circle, CompoundPath, Ellipse, Line, Polygon, Polyline, Rect, Ring, Sector } from '../../util/graphic';
import { TextStyleProps } from 'zrender/lib/graphic/Text';
export interface LooseElementProps extends ElementProps {
    style?: ZRStyleProps;
    shape?: Dictionary<unknown>;
}
export declare type CustomExtraElementInfo = Dictionary<unknown>;
export declare const TRANSFORM_PROPS: {
    readonly x: 1;
    readonly y: 1;
    readonly scaleX: 1;
    readonly scaleY: 1;
    readonly originX: 1;
    readonly originY: 1;
    readonly rotation: 1;
};
export declare type TransformProp = keyof typeof TRANSFORM_PROPS;
export declare const STYLE_VISUAL_TYPE: {
    readonly color: "fill";
    readonly borderColor: "stroke";
};
export declare type StyleVisualProps = keyof typeof STYLE_VISUAL_TYPE;
export declare const NON_STYLE_VISUAL_PROPS: {
    readonly symbol: 1;
    readonly symbolSize: 1;
    readonly symbolKeepAspect: 1;
    readonly legendIcon: 1;
    readonly visualMeta: 1;
    readonly liftZ: 1;
    readonly decal: 1;
};
export declare type NonStyleVisualProps = keyof typeof NON_STYLE_VISUAL_PROPS;
export declare type TransitionAnyOption = {
    transition?: TransitionAnyProps;
    enterFrom?: Dictionary<unknown>;
    leaveTo?: Dictionary<unknown>;
};
declare type TransitionAnyProps = string | string[];
declare type TransitionTransformOption = {
    transition?: ElementRootTransitionProp | ElementRootTransitionProp[];
    enterFrom?: Dictionary<unknown>;
    leaveTo?: Dictionary<unknown>;
};
declare type ElementRootTransitionProp = TransformProp | 'shape' | 'extra' | 'style';
declare type ShapeMorphingOption = {
    /**
     * If do shape morphing animation when type is changed.
     * Only available on path.
     */
    morph?: boolean;
};
export interface CustomBaseDuringAPI {
    setTransform(key: TransformProp, val: number): this;
    getTransform(key: TransformProp): number;
    setExtra(key: string, val: unknown): this;
    getExtra(key: string): unknown;
}
export interface CustomDuringAPI<StyleOpt extends any = any, ShapeOpt extends any = any> extends CustomBaseDuringAPI {
    setShape<T extends keyof ShapeOpt>(key: T, val: ShapeOpt[T]): this;
    getShape<T extends keyof ShapeOpt>(key: T): ShapeOpt[T];
    setStyle<T extends keyof StyleOpt>(key: T, val: StyleOpt[T]): this;
    getStyle<T extends keyof StyleOpt>(key: T): StyleOpt[T];
}
export interface CustomBaseElementOption extends Partial<Pick<Element, TransformProp | 'silent' | 'ignore' | 'textConfig'>>, TransitionTransformOption {
    type: string;
    id?: string;
    name?: string;
    info?: CustomExtraElementInfo;
    textContent?: CustomTextOption | false;
    clipPath?: CustomBaseZRPathOption | false;
    extra?: Dictionary<unknown> & TransitionAnyOption;
    during?(params: CustomBaseDuringAPI): void;
}
export interface CustomDisplayableOption extends CustomBaseElementOption, Partial<Pick<Displayable, 'zlevel' | 'z' | 'z2' | 'invisible'>> {
    style?: ZRStyleProps & TransitionAnyOption;
    during?(params: CustomDuringAPI): void;
    /**
     * @deprecated
     */
    styleEmphasis?: ZRStyleProps | false;
    emphasis?: CustomDisplayableOptionOnState;
    blur?: CustomDisplayableOptionOnState;
    select?: CustomDisplayableOptionOnState;
}
export interface CustomDisplayableOptionOnState extends Partial<Pick<Displayable, TransformProp | 'textConfig' | 'z2'>> {
    style?: (ZRStyleProps & TransitionAnyOption) | false;
    during?(params: CustomDuringAPI): void;
}
export interface CustomGroupOption extends CustomBaseElementOption {
    type: 'group';
    width?: number;
    height?: number;
    diffChildrenByName?: boolean;
    children: CustomElementOption[];
    $mergeChildren?: false | 'byName' | 'byIndex';
}
export interface CustomBaseZRPathOption<T extends PathProps['shape'] = PathProps['shape']> extends CustomDisplayableOption, ShapeMorphingOption {
    autoBatch?: boolean;
    shape?: T & TransitionAnyOption;
    style?: PathProps['style'];
    during?(params: CustomDuringAPI<PathStyleProps, T>): void;
}
interface BuiltinShapes {
    circle: Partial<Circle['shape']>;
    rect: Partial<Rect['shape']>;
    sector: Partial<Sector['shape']>;
    polygon: Partial<Polygon['shape']>;
    polyline: Partial<Polyline['shape']>;
    line: Partial<Line['shape']>;
    arc: Partial<Arc['shape']>;
    bezierCurve: Partial<BezierCurve['shape']>;
    ring: Partial<Ring['shape']>;
    ellipse: Partial<Ellipse['shape']>;
    compoundPath: Partial<CompoundPath['shape']>;
}
interface CustomSVGPathShapeOption {
    pathData?: string;
    d?: string;
    layout?: 'center' | 'cover';
    x?: number;
    y?: number;
    width?: number;
    height?: number;
}
export interface CustomSVGPathOption extends CustomBaseZRPathOption<CustomSVGPathShapeOption> {
    type: 'path';
}
interface CustomBuitinPathOption<T extends keyof BuiltinShapes> extends CustomBaseZRPathOption<BuiltinShapes[T]> {
    type: T;
}
declare type CreateCustomBuitinPathOption<T extends keyof BuiltinShapes> = T extends any ? CustomBuitinPathOption<T> : never;
export declare type CustomPathOption = CreateCustomBuitinPathOption<keyof BuiltinShapes> | CustomSVGPathOption;
export interface CustomImageOptionOnState extends CustomDisplayableOptionOnState {
    style?: ImageStyleProps & TransitionAnyOption;
}
export interface CustomImageOption extends CustomDisplayableOption {
    type: 'image';
    style?: ImageStyleProps & TransitionAnyOption;
    emphasis?: CustomImageOptionOnState;
    blur?: CustomImageOptionOnState;
    select?: CustomImageOptionOnState;
}
export interface CustomTextOptionOnState extends CustomDisplayableOptionOnState {
    style?: TextStyleProps & TransitionAnyOption;
}
export interface CustomTextOption extends CustomDisplayableOption {
    type: 'text';
    style?: TextStyleProps & TransitionAnyOption;
    emphasis?: CustomTextOptionOnState;
    blur?: CustomTextOptionOnState;
    select?: CustomTextOptionOnState;
}
export declare type CustomElementOption = CustomPathOption | CustomImageOption | CustomTextOption | CustomGroupOption;
export declare type CustomRootElementOption = CustomElementOption & {
    focus?: 'none' | 'self' | 'series' | ArrayLike<number>;
    blurScope?: BlurScope;
};
export declare type CustomElementOptionOnState = CustomDisplayableOptionOnState | CustomImageOptionOnState;
export interface CustomSeriesRenderItemAPI extends CustomSeriesRenderItemCoordinateSystemAPI {
    getWidth(): number;
    getHeight(): number;
    getZr(): ZRenderType;
    getDevicePixelRatio(): number;
    value(dim: DimensionLoose, dataIndexInside?: number): ParsedValue;
    ordinalRawValue(dim: DimensionLoose, dataIndexInside?: number): ParsedValue | OrdinalRawValue;
    /**
     * @deprecated
     */
    style(userProps?: ZRStyleProps, dataIndexInside?: number): ZRStyleProps;
    /**
     * @deprecated
     */
    styleEmphasis(userProps?: ZRStyleProps, dataIndexInside?: number): ZRStyleProps;
    visual<VT extends NonStyleVisualProps | StyleVisualProps>(visualType: VT, dataIndexInside?: number): VT extends NonStyleVisualProps ? DefaultDataVisual[VT] : VT extends StyleVisualProps ? PathStyleProps[typeof STYLE_VISUAL_TYPE[VT]] : void;
    barLayout(opt: BarGridLayoutOptionForCustomSeries): BarGridLayoutResult;
    currentSeriesIndices(): number[];
    font(opt: Pick<TextCommonOption, 'fontStyle' | 'fontWeight' | 'fontSize' | 'fontFamily'>): string;
}
export interface CustomSeriesRenderItemParamsCoordSys {
    type: string;
}
export interface CustomSeriesRenderItemCoordinateSystemAPI {
    coord(data: OptionDataValue | OptionDataValue[], clamp?: boolean): number[];
    size?(dataSize: OptionDataValue | OptionDataValue[], dataItem?: OptionDataValue | OptionDataValue[]): number | number[];
}
export declare type WrapEncodeDefRet = Dictionary<number[]>;
export interface CustomSeriesRenderItemParams {
    context: Dictionary<unknown>;
    dataIndex: number;
    seriesId: string;
    seriesName: string;
    seriesIndex: number;
    coordSys: CustomSeriesRenderItemParamsCoordSys;
    encode: WrapEncodeDefRet;
    dataIndexInside: number;
    dataInsideLength: number;
    actionType?: string;
}
export declare type CustomSeriesRenderItemReturn = CustomRootElementOption | undefined | null;
export declare type CustomSeriesRenderItem = (params: CustomSeriesRenderItemParams, api: CustomSeriesRenderItemAPI) => CustomSeriesRenderItemReturn;
export interface CustomSeriesOption extends SeriesOption<unknown>, // don't support StateOption in custom series.
SeriesEncodeOptionMixin, SeriesOnCartesianOptionMixin, SeriesOnPolarOptionMixin, SeriesOnSingleOptionMixin, SeriesOnGeoOptionMixin, SeriesOnCalendarOptionMixin {
    type?: 'custom';
    coordinateSystem?: string | 'none';
    renderItem?: CustomSeriesRenderItem;
    /**
     * @deprecated
     */
    itemStyle?: ItemStyleOption;
    /**
     * @deprecated
     */
    label?: LabelOption;
    /**
     * @deprecated
     */
    emphasis?: {
        /**
         * @deprecated
         */
        itemStyle?: ItemStyleOption;
        /**
         * @deprecated
         */
        label?: LabelOption;
    };
    clip?: boolean;
}
export declare const customInnerStore: (hostObj: Element<ElementProps>) => {
    info: CustomExtraElementInfo;
    customPathData: string;
    customGraphicType: string;
    customImagePath: CustomImageOption['style']['image'];
    txConZ2Set: number;
    leaveToProps: ElementProps;
    option: CustomElementOption;
    userDuring: CustomBaseElementOption['during'];
};
export default class CustomSeriesModel extends SeriesModel<CustomSeriesOption> {
    static type: string;
    readonly type: string;
    static dependencies: string[];
    currentZLevel: number;
    currentZ: number;
    static defaultOption: CustomSeriesOption;
    optionUpdated(): void;
    getInitialData(option: CustomSeriesOption, ecModel: GlobalModel): SeriesData;
    getDataParams(dataIndex: number, dataType?: SeriesDataType, el?: Element): CallbackDataParams & {
        info: CustomExtraElementInfo;
    };
}
export declare type PrepareCustomInfo = (coordSys: CoordinateSystem) => {
    coordSys: CustomSeriesRenderItemParamsCoordSys;
    api: CustomSeriesRenderItemCoordinateSystemAPI;
};
export {};
