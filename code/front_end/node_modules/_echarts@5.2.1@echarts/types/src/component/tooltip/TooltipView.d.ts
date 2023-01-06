import * as formatUtil from '../../util/format';
import ComponentView from '../../view/Component';
import { CallbackDataParams, CommonTooltipOption } from '../../util/types';
import GlobalModel from '../../model/Global';
import ExtensionAPI from '../../core/ExtensionAPI';
import TooltipModel, { TooltipOption } from './TooltipModel';
import { ECData } from '../../util/innerStore';
import { DataByCoordSys } from '../axisPointer/axisTrigger';
interface ShowTipPayload {
    type?: 'showTip';
    from?: string;
    tooltip?: ECData['tooltipConfig']['option'];
    dataByCoordSys?: DataByCoordSys[];
    tooltipOption?: CommonTooltipOption<TooltipCallbackDataParams | TooltipCallbackDataParams[]>;
    seriesIndex?: number;
    dataIndex?: number;
    name?: string;
    x?: number;
    y?: number;
    position?: TooltipOption['position'];
    dispatchAction?: ExtensionAPI['dispatchAction'];
}
interface HideTipPayload {
    type?: 'hideTip';
    from?: string;
    dispatchAction?: ExtensionAPI['dispatchAction'];
}
declare type TooltipCallbackDataParams = CallbackDataParams & {
    axisDim?: string;
    axisIndex?: number;
    axisType?: string;
    axisId?: string;
    axisValue?: string | number;
    axisValueLabel?: string;
    marker?: formatUtil.TooltipMarker;
};
declare class TooltipView extends ComponentView {
    static type: "tooltip";
    type: "tooltip";
    private _renderMode;
    private _tooltipModel;
    private _ecModel;
    private _api;
    private _alwaysShowContent;
    private _tooltipContent;
    private _refreshUpdateTimeout;
    private _lastX;
    private _lastY;
    private _ticket;
    private _showTimout;
    private _lastDataByCoordSys;
    private _cbParamsList;
    private _updatePosition;
    init(ecModel: GlobalModel, api: ExtensionAPI): void;
    render(tooltipModel: TooltipModel, ecModel: GlobalModel, api: ExtensionAPI): void;
    private _initGlobalListener;
    private _keepShow;
    /**
     * Show tip manually by
     * dispatchAction({
     *     type: 'showTip',
     *     x: 10,
     *     y: 10
     * });
     * Or
     * dispatchAction({
     *      type: 'showTip',
     *      seriesIndex: 0,
     *      dataIndex or dataIndexInside or name
     * });
     *
     *  TODO Batch
     */
    manuallyShowTip(tooltipModel: TooltipModel, ecModel: GlobalModel, api: ExtensionAPI, payload: ShowTipPayload): void;
    manuallyHideTip(tooltipModel: TooltipModel, ecModel: GlobalModel, api: ExtensionAPI, payload: HideTipPayload): void;
    private _manuallyAxisShowTip;
    private _tryShow;
    private _showOrMove;
    private _showAxisTooltip;
    private _showSeriesItemTooltip;
    private _showComponentItemTooltip;
    private _showTooltipContent;
    private _getNearestPoint;
    private _doUpdatePosition;
    private _updateContentNotChangedOnAxis;
    private _hide;
    dispose(ecModel: GlobalModel, api: ExtensionAPI): void;
}
export default TooltipView;
