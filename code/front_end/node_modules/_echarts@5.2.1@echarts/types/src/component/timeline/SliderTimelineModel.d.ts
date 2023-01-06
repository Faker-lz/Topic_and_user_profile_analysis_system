import TimelineModel, { TimelineOption } from './TimelineModel';
import { DataFormatMixin } from '../../model/mixin/dataFormat';
import SeriesData from '../../data/SeriesData';
export interface SliderTimelineOption extends TimelineOption {
}
declare class SliderTimelineModel extends TimelineModel {
    static type: string;
    type: string;
    /**
     * @protected
     */
    static defaultOption: SliderTimelineOption;
}
interface SliderTimelineModel extends DataFormatMixin {
    getData(): SeriesData<SliderTimelineModel>;
}
export default SliderTimelineModel;
