export * from '../core/echarts';
export * from './api';
export { ZRColor as Color, Payload } from '../util/types';
export { LinearGradientObject } from 'zrender/lib/graphic/LinearGradient';
export { RadialGradientObject } from 'zrender/lib/graphic/RadialGradient';
export { PatternObject, ImagePatternObject, SVGPatternObject } from 'zrender/lib/graphic/Pattern';
import type { ComponentOption, ECBasicOption as EChartsCoreOption } from '../util/types';
import type { AxisPointerOption } from '../component/axisPointer/AxisPointerModel';
import type { XAXisOption, YAXisOption } from '../coord/cartesian/AxisModel';
import type { AngleAxisOption, RadiusAxisOption } from '../coord/polar/AxisModel';
import type { ParallelAxisOption } from '../coord/parallel/AxisModel';
export { EChartsType as ECharts } from '../core/echarts';
export { EChartsCoreOption };
declare type Dependencies = {
    grid: XAXisOption | YAXisOption | AxisPointerOption;
    polar: AngleAxisOption | RadiusAxisOption;
    parallel: ParallelAxisOption;
};
declare type DependenciesKeys = keyof Dependencies & string;
declare type Arrayable<T> = T | T[];
declare type GetMainType<OptionUnion extends ComponentOption> = Exclude<OptionUnion['mainType'], undefined>;
declare type ExtractComponentOption<OptionUnion, ExtractMainType> = OptionUnion extends {
    mainType?: ExtractMainType;
} ? OptionUnion : never;
declare type GetDependency<DependencyOption extends ComponentOption> = {
    [key in GetMainType<DependencyOption>]?: Arrayable<ExtractComponentOption<DependencyOption, key>>;
};
declare type GetDependencies<MainType extends string> = GetDependency<Dependencies[Extract<MainType, DependenciesKeys>]>;
declare type ComposeUnitOption<OptionUnion extends ComponentOption> = CheckMainType<GetMainType<OptionUnion>> & Omit<EChartsCoreOption, 'baseOption' | 'options'> & {
    [key in GetMainType<OptionUnion>]?: Arrayable<ExtractComponentOption<OptionUnion, key>>;
} & GetDependencies<GetMainType<OptionUnion>>;
declare type CheckMainType<OptionUnionMainType extends string> = string extends OptionUnionMainType ? never : {};
export declare type ComposeOption<OptionUnion extends ComponentOption> = ComposeUnitOption<OptionUnion> & {
    baseOption?: ComposeUnitOption<OptionUnion>;
    options?: ComposeUnitOption<OptionUnion>[];
};
