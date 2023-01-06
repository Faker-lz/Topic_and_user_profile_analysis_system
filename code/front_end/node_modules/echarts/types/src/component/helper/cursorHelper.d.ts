import { ElementEvent } from 'zrender/lib/Element';
import ExtensionAPI from '../../core/ExtensionAPI';
import { CoordinateSystem } from '../../coord/CoordinateSystem';
/**
 * Avoid that: mouse click on a elements that is over geo or graph,
 * but roam is triggered.
 */
export declare function onIrrelevantElement(e: ElementEvent, api: ExtensionAPI, targetCoordSysModel: CoordinateSystem['model']): boolean;
