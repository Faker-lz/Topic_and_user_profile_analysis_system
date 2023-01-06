import Model from '../../model/Model';
import Sector from 'zrender/lib/graphic/shape/Sector';
export declare function getSectorCornerRadius(model: Model<{
    borderRadius?: string | number | (string | number)[];
}>, shape: Pick<Sector['shape'], 'r0' | 'r'>, zeroIfNull?: boolean): {
    innerCornerRadius: number;
    cornerRadius: number;
};
