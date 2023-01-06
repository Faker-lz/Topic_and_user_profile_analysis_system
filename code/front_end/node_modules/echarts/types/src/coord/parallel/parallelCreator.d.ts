import GlobalModel from '../../model/Global';
import ExtensionAPI from '../../core/ExtensionAPI';
import { CoordinateSystemMaster } from '../CoordinateSystem';
declare function createParallelCoordSys(ecModel: GlobalModel, api: ExtensionAPI): CoordinateSystemMaster[];
declare const parallelCoordSysCreator: {
    create: typeof createParallelCoordSys;
};
export default parallelCoordSysCreator;
