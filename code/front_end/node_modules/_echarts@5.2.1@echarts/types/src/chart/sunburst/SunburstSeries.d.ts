import SeriesModel from '../../model/Series';
import { TreeNode } from '../../data/Tree';
import { SeriesOption, CircleLayoutOptionMixin, SeriesLabelOption, ItemStyleOption, OptionDataValue, CallbackDataParams, StatesOptionMixin, OptionDataItemObject, DefaultEmphasisFocus, SunburstColorByMixin } from '../../util/types';
import GlobalModel from '../../model/Global';
import SeriesData from '../../data/SeriesData';
import Model from '../../model/Model';
interface SunburstItemStyleOption<TCbParams = never> extends ItemStyleOption<TCbParams> {
    borderRadius?: (number | string)[] | number | string;
}
interface SunburstLabelOption extends Omit<SeriesLabelOption, 'rotate' | 'position'> {
    rotate?: 'radial' | 'tangential' | number;
    minAngle?: number;
    silent?: boolean;
    position?: SeriesLabelOption['position'] | 'outside';
}
interface SunburstDataParams extends CallbackDataParams {
    treePathInfo: {
        name: string;
        dataIndex: number;
        value: SunburstSeriesNodeItemOption['value'];
    }[];
}
interface SunburstStatesMixin {
    emphasis?: {
        focus?: DefaultEmphasisFocus | 'descendant' | 'ancestor';
    };
}
export interface SunburstStateOption<TCbParams = never> {
    itemStyle?: SunburstItemStyleOption<TCbParams>;
    label?: SunburstLabelOption;
}
export interface SunburstSeriesNodeItemOption extends SunburstStateOption<CallbackDataParams>, StatesOptionMixin<SunburstStateOption<CallbackDataParams>, SunburstStatesMixin>, OptionDataItemObject<OptionDataValue> {
    nodeClick?: 'rootToNode' | 'link';
    link?: string;
    target?: string;
    children?: SunburstSeriesNodeItemOption[];
    collapsed?: boolean;
    cursor?: string;
}
export interface SunburstSeriesLevelOption extends SunburstStateOption, StatesOptionMixin<SunburstStateOption, SunburstStatesMixin> {
    radius?: (number | string)[];
    /**
     * @deprecated use radius instead
     */
    r?: number | string;
    /**
     * @deprecated use radius instead
     */
    r0?: number | string;
    highlight?: {
        itemStyle?: SunburstItemStyleOption;
        label?: SunburstLabelOption;
    };
}
interface SortParam {
    dataIndex: number;
    depth: number;
    height: number;
    getValue(): number;
}
export interface SunburstSeriesOption extends SeriesOption<SunburstStateOption, SunburstStatesMixin>, SunburstStateOption, SunburstColorByMixin, CircleLayoutOptionMixin {
    type?: 'sunburst';
    clockwise?: boolean;
    startAngle?: number;
    minAngle?: number;
    /**
     * If still show when all data zero.
     */
    stillShowZeroSum?: boolean;
    /**
     * Policy of highlighting pieces when hover on one
     * Valid values: 'none' (for not downplay others), 'descendant',
     * 'ancestor', 'self'
     */
    nodeClick?: 'rootToNode' | 'link';
    renderLabelForZeroData?: boolean;
    levels?: SunburstSeriesLevelOption[];
    animationType?: 'expansion' | 'scale';
    sort?: 'desc' | 'asc' | ((a: SortParam, b: SortParam) => number);
}
interface SunburstSeriesModel {
    getFormattedLabel(dataIndex: number, state?: 'emphasis' | 'normal' | 'highlight' | 'blur' | 'select'): string;
}
declare class SunburstSeriesModel extends SeriesModel<SunburstSeriesOption> {
    static readonly type = "series.sunburst";
    readonly type = "series.sunburst";
    ignoreStyleOnData: boolean;
    private _viewRoot;
    private _levelModels;
    getInitialData(option: SunburstSeriesOption, ecModel: GlobalModel): SeriesData<Model<any>, import("../../data/SeriesData").DefaultDataVisual>;
    optionUpdated(): void;
    getDataParams(dataIndex: number): SunburstDataParams;
    getLevelModel(node: TreeNode): Model<SunburstSeriesLevelOption>;
    static defaultOption: SunburstSeriesOption;
    getViewRoot(): TreeNode;
    resetViewRoot(viewRoot?: TreeNode): void;
    enableAriaDecal(): void;
}
export default SunburstSeriesModel;
