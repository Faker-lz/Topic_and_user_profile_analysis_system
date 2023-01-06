import { PatternObject } from 'zrender/lib/graphic/Pattern';
import ExtensionAPI from '../core/ExtensionAPI';
import { InnerDecalObject } from './types';
/**
 * Create or update pattern image from decal options
 *
 * @param {InnerDecalObject | 'none'} decalObject decal options, 'none' if no decal
 * @return {Pattern} pattern with generated image, null if no decal
 */
export declare function createOrUpdatePatternFromDecal(decalObject: InnerDecalObject | 'none', api: ExtensionAPI): PatternObject;
