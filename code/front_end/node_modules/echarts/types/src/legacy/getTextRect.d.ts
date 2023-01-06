import { Text } from '../util/graphic';
declare type TextStyleProps = Text['style'];
export declare function getTextRect(text: TextStyleProps['text'], font?: TextStyleProps['font'], align?: TextStyleProps['align'], verticalAlign?: TextStyleProps['verticalAlign'], padding?: TextStyleProps['padding'], rich?: TextStyleProps['rich'], truncate?: boolean, lineHeight?: number): import("zrender/lib/core/BoundingRect").default;
export {};
