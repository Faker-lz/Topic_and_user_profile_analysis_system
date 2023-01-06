import SeriesData from '../../data/SeriesData';
import Graph from '../../data/Graph';
import { OptionSourceDataOriginal, GraphEdgeItemObject, OptionDataValue, OptionDataItemObject } from '../../util/types';
import SeriesModel from '../../model/Series';
export default function createGraphFromNodeEdge(nodes: OptionSourceDataOriginal<OptionDataValue, OptionDataItemObject<OptionDataValue>>, edges: OptionSourceDataOriginal<OptionDataValue, GraphEdgeItemObject<OptionDataValue>>, seriesModel: SeriesModel, directed: boolean, beforeLink: (nodeData: SeriesData, edgeData: SeriesData) => void): Graph;
