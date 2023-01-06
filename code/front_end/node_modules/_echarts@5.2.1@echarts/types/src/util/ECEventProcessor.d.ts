import { EventProcessor, EventQuery } from 'zrender/lib/core/Eventful';
import { ECActionEvent, NormalizedEventQuery, ECElementEvent } from './types';
import ComponentModel from '../model/Component';
import ComponentView from '../view/Component';
import ChartView from '../view/Chart';
import Element from 'zrender/lib/Element';
/**
 * Usage of query:
 * `chart.on('click', query, handler);`
 * The `query` can be:
 * + The component type query string, only `mainType` or `mainType.subType`,
 *   like: 'xAxis', 'series', 'xAxis.category' or 'series.line'.
 * + The component query object, like:
 *   `{seriesIndex: 2}`, `{seriesName: 'xx'}`, `{seriesId: 'some'}`,
 *   `{xAxisIndex: 2}`, `{xAxisName: 'xx'}`, `{xAxisId: 'some'}`.
 * + The data query object, like:
 *   `{dataIndex: 123}`, `{dataType: 'link'}`, `{name: 'some'}`.
 * + The other query object (cmponent customized query), like:
 *   `{element: 'some'}` (only available in custom series).
 *
 * Caveat: If a prop in the `query` object is `null/undefined`, it is the
 * same as there is no such prop in the `query` object.
 */
export declare class ECEventProcessor implements EventProcessor {
    eventInfo: {
        targetEl: Element;
        packedEvent: ECActionEvent | ECElementEvent;
        model: ComponentModel;
        view: ComponentView | ChartView;
    };
    normalizeQuery(query: EventQuery): NormalizedEventQuery;
    filter(eventType: string, query: NormalizedEventQuery): boolean;
    afterTrigger(): void;
}
