import { PathStyleProps } from 'zrender/lib/graphic/Path';
import Model from '../Model';
export default function makeStyleMapper(properties: readonly string[][], ignoreParent?: boolean): (model: Model, excludes?: readonly string[], includes?: readonly string[]) => PathStyleProps;
