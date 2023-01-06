import { Payload } from '../../util/types';
import { EChartsExtensionInstallRegisters } from '../../extension';
export interface TreeExpandAndCollapsePayload extends Payload {
    dataIndex: number;
}
export declare function installTreeAction(registers: EChartsExtensionInstallRegisters): void;
