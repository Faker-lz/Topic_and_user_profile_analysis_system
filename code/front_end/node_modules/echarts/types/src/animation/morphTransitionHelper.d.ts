import { Path } from '../util/graphic';
import SeriesModel from '../model/Series';
import Element, { ElementAnimateConfig } from 'zrender/lib/Element';
import { UniversalTransitionOption } from '../util/types';
declare type DescendentPaths = Path[];
export declare function applyMorphAnimation(from: DescendentPaths | DescendentPaths[], to: DescendentPaths | DescendentPaths[], divideShape: UniversalTransitionOption['divideShape'], seriesModel: SeriesModel, dataIndex: number, animateOtherProps: (fromIndividual: Path, toIndividual: Path, rawFrom: Path, rawTo: Path, animationCfg: ElementAnimateConfig) => void): void;
export declare function getPathList(elements: Element): DescendentPaths;
export declare function getPathList(elements: Element[]): DescendentPaths[];
export {};
