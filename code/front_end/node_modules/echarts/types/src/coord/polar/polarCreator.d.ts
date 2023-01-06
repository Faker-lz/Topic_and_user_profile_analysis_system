import Polar from './Polar';
import ExtensionAPI from '../../core/ExtensionAPI';
import GlobalModel from '../../model/Global';
declare const polarCreator: {
    dimensions: string[];
    create: (ecModel: GlobalModel, api: ExtensionAPI) => Polar[];
};
export default polarCreator;
