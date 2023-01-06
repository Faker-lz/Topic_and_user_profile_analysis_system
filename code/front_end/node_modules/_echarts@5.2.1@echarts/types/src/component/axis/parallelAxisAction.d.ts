import { Payload } from '../../util/types';
import { EChartsExtensionInstallRegisters } from '../../extension';
export interface ParallelAxisExpandPayload extends Payload {
    axisExpandWindow?: number[];
}
export declare function installParallelActions(registers: EChartsExtensionInstallRegisters): void;
