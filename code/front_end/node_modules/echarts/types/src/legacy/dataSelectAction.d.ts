import Eventful from 'zrender/lib/core/Eventful';
import type { EChartsType, registerAction } from '../core/echarts';
import ExtensionAPI from '../core/ExtensionAPI';
export declare function createLegacyDataSelectAction(seriesType: string, ecRegisterAction: typeof registerAction): void;
export declare function handleLegacySelectEvents(messageCenter: Eventful, ecIns: EChartsType, api: ExtensionAPI): void;
